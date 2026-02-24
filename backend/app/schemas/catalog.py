from datetime import date, time

from pydantic import BaseModel


class DepartmentRead(BaseModel):
    id: int
    code: str
    name: str

    class Config:
        from_attributes = True


class DepartmentCreate(BaseModel):
    code: str
    name: str


class CourseRead(BaseModel):
    id: int
    code: str
    title: str
    description: str
    credits_min: int
    credits_max: int
    level: int
    active: bool
    department_id: int

    class Config:
        from_attributes = True


class CourseCreate(BaseModel):
    code: str
    title: str
    description: str
    credits_min: int
    credits_max: int
    level: int
    active: bool = True
    department_id: int


class TermRead(BaseModel):
    id: int
    code: str
    name: str
    start_date: date
    end_date: date
    registration_open: date
    registration_close: date
    add_drop_deadline: date

    class Config:
        from_attributes = True


class TermCreate(BaseModel):
    code: str
    name: str
    start_date: date
    end_date: date
    registration_open: date
    registration_close: date
    add_drop_deadline: date


class SectionRead(BaseModel):
    id: int
    term_id: int
    course_id: int
    instructor_id: int | None
    section_number: str
    capacity: int
    waitlist_capacity: int
    delivery_mode: str
    location: str
    status: str

    class Config:
        from_attributes = True


class SectionCreate(BaseModel):
    term_id: int
    course_id: int
    instructor_id: int | None = None
    section_number: str
    capacity: int = 30
    waitlist_capacity: int = 0
    delivery_mode: str = "in_person"
    location: str = ""
    status: str = "open"


class MeetingTimeRead(BaseModel):
    id: int
    section_id: int
    day_of_week: str
    start_time: time
    end_time: time

    class Config:
        from_attributes = True


class MeetingTimeCreate(BaseModel):
    section_id: int
    day_of_week: str
    start_time: time
    end_time: time
