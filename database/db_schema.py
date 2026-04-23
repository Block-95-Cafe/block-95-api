from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.types import Integer


class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text, unique=True)

    items: Mapped[list["MenuItem"]] = relationship(
        back_populates="category", lazy="selectin"
    )


class MenuItem(Base):
    __tablename__ = "menu"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    price: Mapped[Decimal] = mapped_column(Numeric(5, 2))
    oz: Mapped[int] = mapped_column(Integer)
    category_id: Mapped[int] = mapped_column(ForeignKey(column="categories.id"))

    category: Mapped["Category"] = relationship(back_populates="items", lazy="selectin")

    def __repr__(self) -> str:
        return f"(Menu Item) id:{self.id} name:{self.name} price:{self.price}, oz:{self.oz}, category_id:{self.category_id}"
