from datetime import time

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class MeetingTime(Base):
    __tablename__ = "meeting_times"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    section_id: Mapped[int] = mapped_column(ForeignKey("sections.id"))
    day_of_week: Mapped[str] = mapped_column(String(9))
    start_time: Mapped[time]
    end_time: Mapped[time]

    section = relationship("Section", back_populates="meeting_times")
