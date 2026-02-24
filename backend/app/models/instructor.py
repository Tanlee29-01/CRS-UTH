from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Instructor(Base):
    __tablename__ = "instructors"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    employee_number: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))

    user = relationship("User")
    department = relationship("Department", back_populates="instructors")
    sections = relationship("Section", back_populates="instructor")
