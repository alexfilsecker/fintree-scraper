from sqlalchemy import String, Integer, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, Union

from .base import Base


if TYPE_CHECKING:
    from .user import User
    from .category import Category


class Movement(Base):
    __tablename__ = "movements"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"))

    date: Mapped[Date] = mapped_column(Date)
    ammount: Mapped[int] = mapped_column(Integer)
    description: Mapped[str | None] = mapped_column(String(255))

    user: Mapped["User"] = relationship(back_populates="movements")
    category: Mapped[Union["Category", None]] = relationship(back_populates="movements")

    def __repr__(self) -> str:
        return f"Movement(id={self.id!r}, date={self.date!r}, description={self.description!r}"
