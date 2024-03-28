from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from .movement import Movement


class User(Base):
    __tablename__ = "users"
    name: Mapped[str] = mapped_column(String(30))
    rut: Mapped[str] = mapped_column(String(30))
    santander_pswd: Mapped[str] = mapped_column(String(30))

    movements: Mapped[List["Movement"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}"
