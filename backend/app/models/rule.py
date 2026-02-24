from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Rule(Base):
    __tablename__ = "rules"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=True)
    rule_type: Mapped[str] = mapped_column(String(50))
    rule_data: Mapped[str] = mapped_column(String(2000), default="{}")
    active: Mapped[bool] = mapped_column(default=True)

    course = relationship("Course", back_populates="rules")
