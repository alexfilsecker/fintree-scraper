from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String

from .base import Base


class User(Base):
    __tablename__ = "users"
    name: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}"
