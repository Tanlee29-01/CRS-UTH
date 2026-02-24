from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    student_number: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    status: Mapped[str] = mapped_column(String(20), default="active")
    level: Mapped[str] = mapped_column(String(20), default="undergrad")
    major: Mapped[str] = mapped_column(String(100), default="")
    gpa: Mapped[float] = mapped_column(default=0.0)
    holds: Mapped[str] = mapped_column(String(200), default="")

    user = relationship("User")
    enrollments = relationship("Enrollment", back_populates="student")
    waitlist_entries = relationship("WaitlistEntry", back_populates="student")
