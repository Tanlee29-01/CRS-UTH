from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(2000))
    credits_min: Mapped[int] = mapped_column(default=3)
    credits_max: Mapped[int] = mapped_column(default=3)
    level: Mapped[int] = mapped_column(default=100)
    active: Mapped[bool] = mapped_column(default=True)

    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))
    department = relationship("Department", back_populates="courses")

    sections = relationship("Section", back_populates="course")
    rules = relationship("Rule", back_populates="course")
