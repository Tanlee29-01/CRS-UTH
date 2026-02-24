from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.course import Course
from app.models.department import Department
from app.models.meeting_time import MeetingTime
from app.models.section import Section
from app.models.term import Term
from app.schemas.catalog import (
    CourseRead,
    DepartmentRead,
    MeetingTimeRead,
    SectionRead,
    TermRead,
)


router = APIRouter()


@router.get("/departments", response_model=list[DepartmentRead])
def list_departments(db: Session = Depends(get_db)):
    return db.execute(select(Department)).scalars().all()


@router.get("/courses", response_model=list[CourseRead])
def list_courses(db: Session = Depends(get_db)):
    return db.execute(select(Course).where(Course.active.is_(True))).scalars().all()


@router.get("/terms", response_model=list[TermRead])
def list_terms(db: Session = Depends(get_db)):
    return db.execute(select(Term)).scalars().all()


@router.get("/sections", response_model=list[SectionRead])
def list_sections(
    term_id: int | None = None,
    course_id: int | None = None,
    db: Session = Depends(get_db),
):
    stmt = select(Section)
    if term_id is not None:
        stmt = stmt.where(Section.term_id == term_id)
    if course_id is not None:
        stmt = stmt.where(Section.course_id == course_id)
    return db.execute(stmt).scalars().all()


@router.get("/sections/{section_id}/meeting-times", response_model=list[MeetingTimeRead])
def list_meeting_times(section_id: int, db: Session = Depends(get_db)):
    return (
        db.execute(select(MeetingTime).where(MeetingTime.section_id == section_id))
        .scalars()
        .all()
    )
