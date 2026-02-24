import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import require_role
from app.db.session import get_db
from app.models.course import Course
from app.models.department import Department
from app.models.enrollment import Enrollment
from app.models.meeting_time import MeetingTime
from app.models.rule import Rule
from app.models.section import Section
from app.models.program import Program
from app.models.program_requirement import ProgramRequirement
from app.models.student import Student
from app.models.student_program import StudentProgram
from app.models.term import Term
from app.models.waitlist import WaitlistEntry
from app.schemas.catalog import (
    CourseCreate,
    CourseRead,
    DepartmentCreate,
    DepartmentRead,
    MeetingTimeCreate,
    MeetingTimeRead,
    SectionCreate,
    SectionRead,
    TermCreate,
    TermRead,
)
from app.schemas.rule import RuleCreate, RuleRead
from app.schemas.student import StudentRead, StudentUpdate
from app.schemas.program import (
    ProgramCreate,
    ProgramRead,
    ProgramRequirementCreate,
    ProgramRequirementRead,
    StudentProgramCreate,
)
from app.services.csv_import import (
    import_courses,
    import_departments,
    import_sections,
    import_terms,
)


router = APIRouter()


@router.post("/admin/departments", response_model=DepartmentRead)
def create_department(
    payload: DepartmentCreate,
    db: Session = Depends(get_db),
    _role=Depends(require_role("admin", "registrar")),
):
    dep = Department(**payload.model_dump())
    db.add(dep)
    db.commit()
    db.refresh(dep)
    return dep


@router.post("/admin/courses", response_model=CourseRead)
def create_course(
    payload: CourseCreate,
    db: Session = Depends(get_db),
    _role=Depends(require_role("admin", "registrar")),
):
    course = Course(**payload.model_dump())
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


@router.post("/admin/terms", response_model=TermRead)
def create_term(
    payload: TermCreate,
    db: Session = Depends(get_db),
    _role=Depends(require_role("admin", "registrar")),
):
    term = Term(**payload.model_dump())
    db.add(term)
    db.commit()
    db.refresh(term)
    return term


@router.post("/admin/sections", response_model=SectionRead)
def create_section(
    payload: SectionCreate,
    db: Session = Depends(get_db),
    _role=Depends(require_role("admin", "registrar")),
):
    section = Section(**payload.model_dump())
    db.add(section)
    db.commit()
    db.refresh(section)
    return section


@router.post("/admin/meeting-times", response_model=MeetingTimeRead)
def create_meeting_time(
    payload: MeetingTimeCreate,
    db: Session = Depends(get_db),
    _role=Depends(require_role("admin", "registrar")),
):
    meeting = MeetingTime(**payload.model_dump())
    db.add(meeting)
    db.commit()
    db.refresh(meeting)
    return meeting


@router.post("/admin/rules", response_model=RuleRead)
def create_rule(
    payload: RuleCreate,
    db: Session = Depends(get_db),
    _role=Depends(require_role("admin", "registrar")),
):
    try:
        json.loads(payload.rule_data or "{}")
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid rule_data JSON")

    rule = Rule(**payload.model_dump())
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule


@router.get("/admin/rules", response_model=list[RuleRead])
def list_rules(
    db: Session = Depends(get_db),
    _role=Depends(require_role("admin", "registrar")),
):
    return db.execute(select(Rule)).scalars().all()


@router.delete("/admin/rules/{rule_id}", response_model=dict)
def delete_rule(
    rule_id: int,
    db: Session = Depends(get_db),
    _role=Depends(require_role("admin", "registrar")),
):
    rule = db.execute(select(Rule).where(Rule.id == rule_id)).scalar_one_or_none()
    if not rule:
        return {"status": "not_found"}
    db.delete(rule)
    db.commit()
    return {"status": "deleted", "rule_id": rule_id}


@router.get("/admin/enrollments", response_model=list[dict])
def list_enrollments(
    db: Session = Depends(get_db),
    _role=Depends(require_role("admin", "registrar")),
):
    rows = db.execute(select(Enrollment)).scalars().all()
    return [
        {
            "id": e.id,
            "student_id": e.student_id,
            "section_id": e.section_id,
            "status": e.status,
        }
        for e in rows
    ]


@router.get("/admin/reports/sections", response_model=list[dict])
def report_sections(
    term_id: int | None = None,
    course_id: int | None = None,
    db: Session = Depends(get_db),
    _role=Depends(require_role("admin", "registrar")),
):
    stmt = select(Section)
    if term_id is not None:
        stmt = stmt.where(Section.term_id == term_id)
    if course_id is not None:
        stmt = stmt.where(Section.course_id == course_id)
    sections = db.execute(stmt).scalars().all()
    results = []
    for s in sections:
        enrolled = (
            db.execute(
                select(func.count())
                .select_from(Enrollment)
                .where(Enrollment.section_id == s.id, Enrollment.status == "enrolled")
            ).scalar_one()
        )
        waitlisted = (
            db.execute(
                select(func.count())
                .select_from(WaitlistEntry)
                .where(WaitlistEntry.section_id == s.id)
            ).scalar_one()
        )
        utilization = (enrolled / s.capacity * 100.0) if s.capacity else 0.0
        results.append(
            {
                "section_id": s.id,
                "course_id": s.course_id,
                "term_id": s.term_id,
                "capacity": s.capacity,
                "enrolled": enrolled,
                "waitlisted": waitlisted,
                "utilization": round(utilization, 1),
            }
        )
    return results


@router.get("/admin/students", response_model=list[StudentRead])
def list_students(
    db: Session = Depends(get_db),
    _role=Depends(require_role("admin", "registrar")),
):
    return db.execute(select(Student)).scalars().all()


@router.patch("/admin/students/{student_id}", response_model=StudentRead)
def update_student(
    student_id: int,
    payload: StudentUpdate,
    db: Session = Depends(get_db),
    _role=Depends(require_role("admin", "registrar")),
):
    student = db.execute(select(Student).where(Student.id == student_id)).scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(student, field, value)
    db.commit()
    db.refresh(student)
    return student


@router.post("/admin/programs", response_model=ProgramRead)
def create_program(
    payload: ProgramCreate,
    db: Session = Depends(get_db),
    _role=Depends(require_role("admin", "registrar")),
):
    program = Program(**payload.model_dump())
    db.add(program)
    db.commit()
    db.refresh(program)
    return program


@router.post("/admin/program-requirements", response_model=ProgramRequirementRead)
def create_program_requirement(
    payload: ProgramRequirementCreate,
    db: Session = Depends(get_db),
    _role=Depends(require_role("admin", "registrar")),
):
    req = ProgramRequirement(**payload.model_dump())
    db.add(req)
    db.commit()
    db.refresh(req)
    return req


@router.post("/admin/student-programs", response_model=dict)
def assign_student_program(
    payload: StudentProgramCreate,
    db: Session = Depends(get_db),
    _role=Depends(require_role("admin", "registrar")),
):
    db.add(StudentProgram(**payload.model_dump()))
    db.commit()
    return {"status": "assigned"}


@router.post("/admin/import/departments", response_model=dict)
def import_departments_csv(
    payload: dict,
    db: Session = Depends(get_db),
    _role=Depends(require_role("admin", "registrar")),
):
    return import_departments(db, payload.get("csv", ""))


@router.post("/admin/import/courses", response_model=dict)
def import_courses_csv(
    payload: dict,
    db: Session = Depends(get_db),
    _role=Depends(require_role("admin", "registrar")),
):
    return import_courses(db, payload.get("csv", ""))


@router.post("/admin/import/terms", response_model=dict)
def import_terms_csv(
    payload: dict,
    db: Session = Depends(get_db),
    _role=Depends(require_role("admin", "registrar")),
):
    return import_terms(db, payload.get("csv", ""))


@router.post("/admin/import/sections", response_model=dict)
def import_sections_csv(
    payload: dict,
    db: Session = Depends(get_db),
    _role=Depends(require_role("admin", "registrar")),
):
    return import_sections(db, payload.get("csv", ""))


@router.post("/admin/enrollments/{enrollment_id}/complete", response_model=dict)
def complete_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db),
    _role=Depends(require_role("admin", "registrar")),
):
    enrollment = db.execute(select(Enrollment).where(Enrollment.id == enrollment_id)).scalar_one_or_none()
    if not enrollment:
        return {"status": "not_found"}
    enrollment.status = "completed"
    db.commit()
    return {"status": "completed", "enrollment_id": enrollment_id}
