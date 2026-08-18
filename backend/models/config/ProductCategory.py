import uuid
from typing import TYPE_CHECKING, Any
from sqlalchemy import Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.database import Base

if TYPE_CHECKING:
    from models.config.Product import Product


class ProductCategory(Base):
    __tablename__ = "product_categories"

    def __init__(self, name: str, **kw: Any) -> None:
        super().__init__(**kw)
        self.name = name

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column()

    products: Mapped[list["Product"]] = relationship(back_populates="category")
