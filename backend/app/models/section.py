from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Section(Base):
    __tablename__ = "sections"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    term_id: Mapped[int] = mapped_column(ForeignKey("terms.id"))
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    instructor_id: Mapped[int] = mapped_column(ForeignKey("instructors.id"), nullable=True)

    section_number: Mapped[str] = mapped_column(String(10))
    capacity: Mapped[int] = mapped_column(default=30)
    waitlist_capacity: Mapped[int] = mapped_column(default=0)
    delivery_mode: Mapped[str] = mapped_column(String(20), default="in_person")
    location: Mapped[str] = mapped_column(String(100), default="")
    status: Mapped[str] = mapped_column(String(20), default="open")

    term = relationship("Term", back_populates="sections")
    course = relationship("Course", back_populates="sections")
    instructor = relationship("Instructor", back_populates="sections")
    meeting_times = relationship("MeetingTime", back_populates="section")
    enrollments = relationship("Enrollment", back_populates="section")
    waitlist_entries = relationship("WaitlistEntry", back_populates="section")
