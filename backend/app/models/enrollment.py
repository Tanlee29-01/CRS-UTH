from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Enrollment(Base):
    __tablename__ = "enrollments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    section_id: Mapped[int] = mapped_column(ForeignKey("sections.id"))
    status: Mapped[str] = mapped_column(String(20), default="enrolled")
    source: Mapped[str] = mapped_column(String(20), default="self")
    enrolled_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    dropped_at: Mapped[datetime] = mapped_column(nullable=True)

    student = relationship("Student", back_populates="enrollments")
    section = relationship("Section", back_populates="enrollments")
