import csv
from io import StringIO

from sqlalchemy.orm import Session

from app.models.course import Course
from app.models.department import Department
from app.models.section import Section
from app.models.term import Term


def import_departments(db: Session, csv_text: str) -> dict:
    reader = csv.DictReader(StringIO(csv_text))
    created = 0
    for row in reader:
        code = (row.get("code") or "").strip()
        name = (row.get("name") or "").strip()
        if not code or not name:
            continue
        exists = db.query(Department).filter(Department.code == code).first()
        if exists:
            continue
        db.add(Department(code=code, name=name))
        created += 1
    db.commit()
    return {"created": created}


def import_courses(db: Session, csv_text: str) -> dict:
    reader = csv.DictReader(StringIO(csv_text))
    created = 0
    for row in reader:
        code = (row.get("code") or "").strip()
        title = (row.get("title") or "").strip()
        description = (row.get("description") or "").strip()
        credits_min = int(row.get("credits_min") or 3)
        credits_max = int(row.get("credits_max") or credits_min)
        level = int(row.get("level") or 100)
        department_code = (row.get("department_code") or "").strip()
        if not code or not title or not department_code:
            continue
        department = db.query(Department).filter(Department.code == department_code).first()
        if not department:
            continue
        exists = db.query(Course).filter(Course.code == code).first()
        if exists:
            continue
        db.add(
            Course(
                code=code,
                title=title,
                description=description,
                credits_min=credits_min,
                credits_max=credits_max,
                level=level,
                department_id=department.id,
                active=True,
            )
        )
        created += 1
    db.commit()
    return {"created": created}


def import_terms(db: Session, csv_text: str) -> dict:
    reader = csv.DictReader(StringIO(csv_text))
    created = 0
    for row in reader:
        code = (row.get("code") or "").strip()
        name = (row.get("name") or "").strip()
        start_date = row.get("start_date")
        end_date = row.get("end_date")
        registration_open = row.get("registration_open")
        registration_close = row.get("registration_close")
        add_drop_deadline = row.get("add_drop_deadline")
        if not code or not name:
            continue
        exists = db.query(Term).filter(Term.code == code).first()
        if exists:
            continue
        db.add(
            Term(
                code=code,
                name=name,
                start_date=start_date,
                end_date=end_date,
                registration_open=registration_open,
                registration_close=registration_close,
                add_drop_deadline=add_drop_deadline,
            )
        )
        created += 1
    db.commit()
    return {"created": created}


def import_sections(db: Session, csv_text: str) -> dict:
    reader = csv.DictReader(StringIO(csv_text))
    created = 0
    for row in reader:
        term_code = (row.get("term_code") or "").strip()
        course_code = (row.get("course_code") or "").strip()
        section_number = (row.get("section_number") or "").strip()
        capacity = int(row.get("capacity") or 30)
        waitlist_capacity = int(row.get("waitlist_capacity") or 0)
        delivery_mode = (row.get("delivery_mode") or "in_person").strip()
        location = (row.get("location") or "").strip()
        status = (row.get("status") or "open").strip()
        if not term_code or not course_code or not section_number:
            continue
        term = db.query(Term).filter(Term.code == term_code).first()
        course = db.query(Course).filter(Course.code == course_code).first()
        if not term or not course:
            continue
        exists = (
            db.query(Section)
            .filter(
                Section.term_id == term.id,
                Section.course_id == course.id,
                Section.section_number == section_number,
            )
            .first()
        )
        if exists:
            continue
        db.add(
            Section(
                term_id=term.id,
                course_id=course.id,
                section_number=section_number,
                capacity=capacity,
                waitlist_capacity=waitlist_capacity,
                delivery_mode=delivery_mode,
                location=location,
                status=status,
            )
        )
        created += 1
    db.commit()
    return {"created": created}
