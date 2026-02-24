from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ProgramRequirement(Base):
    __tablename__ = "program_requirements"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    program_id: Mapped[int] = mapped_column(ForeignKey("programs.id"))
    course_code: Mapped[str] = mapped_column(String(20))
    requirement_type: Mapped[str] = mapped_column(String(20), default="required")

    program = relationship("Program", back_populates="requirements")
