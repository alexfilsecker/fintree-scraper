from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Date

from .base import Base


class Movement(Base):
    __tablename__ = "movements"
    date: Mapped[Date] = mapped_column(Date)
    description: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f"Movement(id={self.id!r}, date={self.date!r}, description={self.description!r}"
