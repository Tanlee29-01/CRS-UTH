from datetime import datetime

from pydantic import BaseModel


class EnrollmentRead(BaseModel):
    id: int
    student_id: int
    section_id: int
    status: str
    enrolled_at: datetime
    dropped_at: datetime | None = None

    class Config:
        from_attributes = True


class WaitlistRead(BaseModel):
    id: int
    student_id: int
    section_id: int
    position: int
    created_at: datetime

    class Config:
        from_attributes = True
