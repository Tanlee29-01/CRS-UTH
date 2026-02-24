from datetime import date, time

from sqlalchemy import select

from app.db.session import SessionLocal
from app.core.security import hash_password
from app.models.course import Course
from app.models.department import Department
from app.models.meeting_time import MeetingTime
from app.models.section import Section
from app.models.student import Student
from app.models.term import Term
from app.models.user import User


def seed():
    db = SessionLocal()
    try:
        existing = db.execute(select(Department).limit(1)).scalar_one_or_none()

        if not existing:
            cs = Department(code="CS", name="Computer Science")
            math = Department(code="MATH", name="Mathematics")
            db.add_all([cs, math])
            db.flush()
        else:
            cs = db.execute(select(Department).where(Department.code == "CS")).scalar_one()
            math = db.execute(select(Department).where(Department.code == "MATH")).scalar_one()

        if not db.execute(select(Course).limit(1)).scalar_one_or_none():
            courses = [
                Course(
                    code="CS101",
                    title="Intro to Programming",
                    description="Foundations of programming in Python.",
                    credits_min=3,
                    credits_max=3,
                    level=100,
                    department_id=cs.id,
                    active=True,
                ),
                Course(
                    code="CS201",
                    title="Data Structures",
                    description="Arrays, lists, trees, and graphs.",
                    credits_min=3,
                    credits_max=3,
                    level=200,
                    department_id=cs.id,
                    active=True,
                ),
                Course(
                    code="MATH101",
                    title="Calculus I",
                    description="Limits, derivatives, and integrals.",
                    credits_min=4,
                    credits_max=4,
                    level=100,
                    department_id=math.id,
                    active=True,
                ),
            ]
            db.add_all(courses)
            db.flush()
        else:
            courses = db.execute(select(Course).order_by(Course.id)).scalars().all()

        term = db.execute(select(Term).where(Term.code == "2026SP")).scalar_one_or_none()
        if not term:
            term = Term(
                code="2026SP",
                name="Spring 2026",
                start_date=date(2026, 1, 12),
                end_date=date(2026, 5, 15),
                registration_open=date(2026, 1, 2),
                registration_close=date(2026, 2, 15),
                add_drop_deadline=date(2026, 2, 1),
            )
            db.add(term)
            db.flush()

        sections = db.execute(select(Section).where(Section.term_id == term.id)).scalars().all()
        if not sections:
            sections = [
                Section(
                    term_id=term.id,
                    course_id=courses[0].id,
                    section_number="001",
                    capacity=30,
                    waitlist_capacity=5,
                    delivery_mode="in_person",
                    location="Bldg A 101",
                    status="open",
                ),
                Section(
                    term_id=term.id,
                    course_id=courses[1].id,
                    section_number="001",
                    capacity=25,
                    waitlist_capacity=5,
                    delivery_mode="hybrid",
                    location="Bldg A 210",
                    status="open",
                ),
                Section(
                    term_id=term.id,
                    course_id=courses[2].id,
                    section_number="001",
                    capacity=35,
                    waitlist_capacity=0,
                    delivery_mode="in_person",
                    location="Bldg B 111",
                    status="open",
                ),
            ]
            db.add_all(sections)
            db.flush()

        if not db.execute(select(MeetingTime).limit(1)).scalar_one_or_none():
            meetings = [
                MeetingTime(
                    section_id=sections[0].id,
                    day_of_week="Mon",
                    start_time=time(9, 0),
                    end_time=time(10, 15),
                ),
                MeetingTime(
                    section_id=sections[0].id,
                    day_of_week="Wed",
                    start_time=time(9, 0),
                    end_time=time(10, 15),
                ),
                MeetingTime(
                    section_id=sections[1].id,
                    day_of_week="Tue",
                    start_time=time(11, 0),
                    end_time=time(12, 15),
                ),
                MeetingTime(
                    section_id=sections[1].id,
                    day_of_week="Thu",
                    start_time=time(11, 0),
                    end_time=time(12, 15),
                ),
                MeetingTime(
                    section_id=sections[2].id,
                    day_of_week="Mon",
                    start_time=time(14, 0),
                    end_time=time(15, 30),
                ),
                MeetingTime(
                    section_id=sections[2].id,
                    day_of_week="Wed",
                    start_time=time(14, 0),
                    end_time=time(15, 30),
                ),
            ]
            db.add_all(meetings)

        if not db.execute(select(User).where(User.email == "admin@example.com")).scalar_one_or_none():
            admin = User(
                email="admin@example.com",
                password_hash=hash_password("AdminPass123!"),
                role="admin",
            )
            db.add(admin)
            db.flush()

        if not db.execute(select(User).where(User.email == "student@example.com")).scalar_one_or_none():
            student_user = User(
                email="student@example.com",
                password_hash=hash_password("StudentPass123!"),
                role="student",
            )
            db.add(student_user)
            db.flush()
            db.add(
                Student(
                    user_id=student_user.id,
                    student_number=f"S{student_user.id:06d}",
                    major="Computer Science",
                    gpa=3.2,
                    holds="",
                )
            )

        db.commit()
        print("Seed data inserted.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
