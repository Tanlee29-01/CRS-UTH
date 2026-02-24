from pydantic import BaseModel


class StudentRead(BaseModel):
    id: int
    user_id: int
    student_number: str
    status: str
    level: str
    major: str
    gpa: float
    holds: str

    class Config:
        from_attributes = True


class StudentUpdate(BaseModel):
    status: str | None = None
    level: str | None = None
    major: str | None = None
    gpa: float | None = None
    holds: str | None = None
