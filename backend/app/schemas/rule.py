from pydantic import BaseModel


class RuleCreate(BaseModel):
    course_id: int | None = None
    rule_type: str
    rule_data: str
    active: bool = True


class RuleRead(BaseModel):
    id: int
    course_id: int | None
    rule_type: str
    rule_data: str
    active: bool

    class Config:
        from_attributes = True
