from sqlalchemy import String, Integer, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING


from .base import Base

if TYPE_CHECKING:
    from .movement import Movement


class Category(Base):
    __tablename__ = "categories"

    parent_category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("categories.id")
    )

    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(255))

    children_categories: Mapped[List["Category"]] = relationship(
        back_populates="parent"
    )
    paretn_category: Mapped["Category"] = relationship(
        back_populates="children_categories", remote_side=[Base.id]
    )
    movements: Mapped[List["Movement"]] = relationship(back_populates="category")
