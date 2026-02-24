from pydantic import BaseModel


class ProgramCreate(BaseModel):
    code: str
    name: str


class ProgramRead(BaseModel):
    id: int
    code: str
    name: str

    class Config:
        from_attributes = True


class ProgramRequirementCreate(BaseModel):
    program_id: int
    course_code: str
    requirement_type: str = "required"


class ProgramRequirementRead(BaseModel):
    id: int
    program_id: int
    course_code: str
    requirement_type: str

    class Config:
        from_attributes = True


class StudentProgramCreate(BaseModel):
    student_id: int
    program_id: int
