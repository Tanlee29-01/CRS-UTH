from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
import json

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_student, require_role
from app.core.config import settings
from app.db.session import get_db
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.meeting_time import MeetingTime
from app.models.rule import Rule
from app.models.section import Section
from app.models.notification import Notification
from app.models.waitlist import WaitlistEntry
from app.schemas.enrollment import EnrollmentRead, WaitlistRead
from app.models.student import Student


router = APIRouter()


@router.get("/me/enrollments", response_model=list[EnrollmentRead])
def my_enrollments(
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student),
):
    enrollments = (
        db.execute(
            select(Enrollment).where(
                Enrollment.student_id == student.id, Enrollment.status == "enrolled"
            )
        )
        .scalars()
        .all()
    )
    return enrollments


@router.post("/sections/{section_id}/enroll", response_model=EnrollmentRead)
def enroll_in_section(
    section_id: int,
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student),
    _role=Depends(require_role("student")),
):
    section = db.execute(select(Section).where(Section.id == section_id)).scalar_one_or_none()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    course = db.execute(select(Course).where(Course.id == section.course_id)).scalar_one()
    rules = (
        db.execute(
            select(Rule).where(
                Rule.active.is_(True),
                (Rule.course_id == course.id) | (Rule.course_id.is_(None)),
            )
        )
        .scalars()
        .all()
    )

    for rule in rules:
        try:
            data = json.loads(rule.rule_data or "{}")
        except json.JSONDecodeError:
            continue

        course_codes = data.get("course_codes", [])
        if not course_codes:
            continue

        if rule.rule_type == "prereq":
            completed = db.execute(
                select(Enrollment)
                .join(Section, Enrollment.section_id == Section.id)
                .join(Course, Section.course_id == Course.id)
                .where(
                    Enrollment.student_id == student.id,
                    Enrollment.status == "completed",
                    Course.code.in_(course_codes),
                )
            ).scalar_one_or_none()
            if not completed:
                raise HTTPException(
                    status_code=409,
                    detail=f"Prerequisite not met: {', '.join(course_codes)}",
                )

        if rule.rule_type == "coreq":
            coreq = db.execute(
                select(Enrollment)
                .join(Section, Enrollment.section_id == Section.id)
                .join(Course, Section.course_id == Course.id)
                .where(
                    Enrollment.student_id == student.id,
                    Enrollment.status == "enrolled",
                    Section.term_id == section.term_id,
                    Course.code.in_(course_codes),
                )
            ).scalar_one_or_none()
            if not coreq:
                raise HTTPException(
                    status_code=409,
                    detail=f"Corequisite required: {', '.join(course_codes)}",
                )

    term_enrollments = (
        db.execute(
            select(Enrollment)
            .join(Section, Enrollment.section_id == Section.id)
            .where(
                Enrollment.student_id == student.id,
                Enrollment.status == "enrolled",
                Section.term_id == section.term_id,
            )
        )
        .scalars()
        .all()
    )

    if term_enrollments:
        current_credits = (
            db.execute(
                select(func.coalesce(func.sum(Course.credits_max), 0))
                .select_from(Enrollment)
                .join(Section, Enrollment.section_id == Section.id)
                .join(Course, Section.course_id == Course.id)
                .where(
                    Enrollment.student_id == student.id,
                    Enrollment.status == "enrolled",
                    Section.term_id == section.term_id,
                )
            )
        ).scalar_one()
    else:
        current_credits = 0

    next_credits = current_credits + course.credits_max
    if next_credits > settings.max_credits_per_term:
        raise HTTPException(
            status_code=409,
            detail=f"Credit limit exceeded: {next_credits}/{settings.max_credits_per_term}",
        )

    new_times = (
        db.execute(select(MeetingTime).where(MeetingTime.section_id == section.id))
        .scalars()
        .all()
    )
    if new_times and term_enrollments:
        enrolled_section_ids = [e.section_id for e in term_enrollments]
        existing_times = (
            db.execute(
                select(MeetingTime).where(MeetingTime.section_id.in_(enrolled_section_ids))
            )
            .scalars()
            .all()
        )
        for nt in new_times:
            for et in existing_times:
                if nt.day_of_week != et.day_of_week:
                    continue
                if nt.start_time < et.end_time and et.start_time < nt.end_time:
                    raise HTTPException(
                        status_code=409,
                        detail="Time conflict with existing schedule",
                    )

    existing = db.execute(
        select(Enrollment).where(
            Enrollment.section_id == section_id,
            Enrollment.student_id == student.id,
            Enrollment.status == "enrolled",
        )
    ).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=409, detail="Already enrolled")

    enrolled_count = db.execute(
        select(func.count()).select_from(Enrollment).where(
            Enrollment.section_id == section_id, Enrollment.status == "enrolled"
        )
    ).scalar_one()

    if enrolled_count >= section.capacity:
        if section.waitlist_capacity <= 0:
            raise HTTPException(status_code=409, detail="Section full")

        wait_count = db.execute(
            select(func.count()).select_from(WaitlistEntry).where(
                WaitlistEntry.section_id == section_id
            )
        ).scalar_one()
        if wait_count >= section.waitlist_capacity:
            raise HTTPException(status_code=409, detail="Waitlist full")

        position = (
            db.execute(
                select(func.max(WaitlistEntry.position)).where(
                    WaitlistEntry.section_id == section_id
                )
            ).scalar_one()
            or 0
        )
        entry = WaitlistEntry(
            student_id=student.id, section_id=section_id, position=position + 1
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED,
            detail=f"Added to waitlist at position {entry.position}",
        )

    enrollment = Enrollment(student_id=student.id, section_id=section_id, status="enrolled")
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment


@router.post("/cart/validate", response_model=dict)
def validate_cart(
    payload: dict,
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student),
    _role=Depends(require_role("student")),
):
    section_ids = payload.get("section_ids") or []
    if not isinstance(section_ids, list):
        raise HTTPException(status_code=400, detail="section_ids must be a list")

    errors = []
    sections = (
        db.execute(select(Section).where(Section.id.in_(section_ids))).scalars().all()
        if section_ids
        else []
    )

    term_ids = {s.term_id for s in sections}
    if len(term_ids) > 1:
        errors.append("Cart must be within a single term")

    enrolled_sections = (
        db.execute(
            select(Section)
            .join(Enrollment, Enrollment.section_id == Section.id)
            .where(
                Enrollment.student_id == student.id,
                Enrollment.status == "enrolled",
            )
        )
        .scalars()
        .all()
    )

    all_sections = enrolled_sections + sections
    total_credits = 0
    for s in all_sections:
        course = db.execute(select(Course).where(Course.id == s.course_id)).scalar_one()
        total_credits += course.credits_max

    if total_credits > settings.max_credits_per_term:
        errors.append(
            f"Credit limit exceeded: {total_credits}/{settings.max_credits_per_term}"
        )

    all_section_ids = [s.id for s in all_sections]
    if all_section_ids:
        times = (
            db.execute(select(MeetingTime).where(MeetingTime.section_id.in_(all_section_ids)))
            .scalars()
            .all()
        )
        for i in range(len(times)):
            for j in range(i + 1, len(times)):
                a = times[i]
                b = times[j]
                if a.section_id == b.section_id:
                    continue
                if a.day_of_week != b.day_of_week:
                    continue
                if a.start_time < b.end_time and b.start_time < a.end_time:
                    errors.append("Time conflict detected in cart/schedule")
                    i = len(times)
                    break

    for s in sections:
        course = db.execute(select(Course).where(Course.id == s.course_id)).scalar_one()
        rules = (
            db.execute(
                select(Rule).where(
                    Rule.active.is_(True),
                    (Rule.course_id == course.id) | (Rule.course_id.is_(None)),
                )
            )
            .scalars()
            .all()
        )
        for rule in rules:
            try:
                data = json.loads(rule.rule_data or "{}")
            except json.JSONDecodeError:
                continue
            course_codes = data.get("course_codes", [])
            if not course_codes:
                continue
            if rule.rule_type == "prereq":
                completed = db.execute(
                    select(Enrollment)
                    .join(Section, Enrollment.section_id == Section.id)
                    .join(Course, Section.course_id == Course.id)
                    .where(
                        Enrollment.student_id == student.id,
                        Enrollment.status == "completed",
                        Course.code.in_(course_codes),
                    )
                ).scalar_one_or_none()
                if not completed:
                    errors.append(f"Prerequisite not met: {', '.join(course_codes)}")
            if rule.rule_type == "coreq":
                coreq = db.execute(
                    select(Enrollment)
                    .join(Section, Enrollment.section_id == Section.id)
                    .join(Course, Section.course_id == Course.id)
                    .where(
                        Enrollment.student_id == student.id,
                        Enrollment.status == "enrolled",
                        Section.term_id == s.term_id,
                        Course.code.in_(course_codes),
                    )
                ).scalar_one_or_none()
                if not coreq:
                    errors.append(f"Corequisite required: {', '.join(course_codes)}")

    return {"ok": len(errors) == 0, "errors": errors}


@router.post("/billing/estimate", response_model=dict)
def estimate_billing(
    payload: dict,
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student),
    _role=Depends(require_role("student")),
):
    section_ids = payload.get("section_ids") or []
    sections = (
        db.execute(select(Section).where(Section.id.in_(section_ids))).scalars().all()
        if section_ids
        else []
    )
    credits = 0
    for s in sections:
        course = db.execute(select(Course).where(Course.id == s.course_id)).scalar_one()
        credits += course.credits_max
    return {"credits": credits, "rate": settings.credit_rate, "total": credits * settings.credit_rate}


@router.post("/sections/{section_id}/drop", response_model=EnrollmentRead)
def drop_section(
    section_id: int,
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student),
    _role=Depends(require_role("student")),
):
    enrollment = db.execute(
        select(Enrollment).where(
            Enrollment.section_id == section_id,
            Enrollment.student_id == student.id,
            Enrollment.status == "enrolled",
        )
    ).scalar_one_or_none()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    enrollment.status = "dropped"
    enrollment.dropped_at = datetime.utcnow()
    db.commit()

    promote = db.execute(
        select(WaitlistEntry)
        .where(WaitlistEntry.section_id == section_id)
        .order_by(WaitlistEntry.position.asc())
        .limit(1)
    ).scalar_one_or_none()

    if promote:
        enrolled_count = db.execute(
            select(func.count()).select_from(Enrollment).where(
                Enrollment.section_id == section_id, Enrollment.status == "enrolled"
            )
        ).scalar_one()

        section = db.execute(select(Section).where(Section.id == section_id)).scalar_one()
        if enrolled_count < section.capacity:
            db.add(
                Enrollment(
                    student_id=promote.student_id,
                    section_id=section_id,
                    status="enrolled",
                    enrolled_at=datetime.utcnow(),
                )
            )
            db.add(
                Notification(
                    user_id=db.execute(
                        select(Student.user_id).where(Student.id == promote.student_id)
                    ).scalar_one(),
                    title="Waitlist Promotion",
                    body=f"You have been enrolled in section {section_id}.",
                )
            )
            db.delete(promote)
            db.commit()

    db.refresh(enrollment)
    return enrollment


@router.get("/sections/{section_id}/waitlist", response_model=list[WaitlistRead])
def list_waitlist(
    section_id: int,
    db: Session = Depends(get_db),
    _role=Depends(require_role("admin", "registrar", "instructor")),
):
    entries = (
        db.execute(
            select(WaitlistEntry)
            .where(WaitlistEntry.section_id == section_id)
            .order_by(WaitlistEntry.position.asc())
        )
        .scalars()
        .all()
    )
    return entries
