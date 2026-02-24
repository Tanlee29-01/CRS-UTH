import csv
from io import StringIO

from fastapi import APIRouter, Depends, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import require_role
from app.db.session import get_db
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.section import Section
from app.models.student import Student


router = APIRouter()


@router.get("/instructor/sections/{section_id}/roster", response_model=list[dict])
def section_roster(
    section_id: int,
    db: Session = Depends(get_db),
    _role=Depends(require_role("instructor", "admin", "registrar")),
):
    rows = (
        db.execute(
            select(Enrollment, Student, Course)
            .join(Section, Enrollment.section_id == Section.id)
            .join(Student, Enrollment.student_id == Student.id)
            .join(Course, Section.course_id == Course.id)
            .where(Enrollment.section_id == section_id, Enrollment.status == "enrolled")
        )
        .all()
    )
    return [
        {
            "enrollment_id": e.id,
            "student_id": s.id,
            "student_number": s.student_number,
            "major": s.major,
            "gpa": s.gpa,
            "course_code": c.code,
        }
        for (e, s, c) in rows
    ]


@router.get("/instructor/sections/{section_id}/roster.csv")
def section_roster_csv(
    section_id: int,
    db: Session = Depends(get_db),
    _role=Depends(require_role("instructor", "admin", "registrar")),
):
    rows = (
        db.execute(
            select(Enrollment, Student, Course)
            .join(Section, Enrollment.section_id == Section.id)
            .join(Student, Enrollment.student_id == Student.id)
            .join(Course, Section.course_id == Course.id)
            .where(Enrollment.section_id == section_id, Enrollment.status == "enrolled")
        )
        .all()
    )

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["student_number", "major", "gpa", "course_code"])
    for e, s, c in rows:
        writer.writerow([s.student_number, s.major, s.gpa, c.code])

    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=roster_{section_id}.csv"},
    )
