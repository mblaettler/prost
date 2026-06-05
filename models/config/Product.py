import uuid
from typing import Any
from sqlalchemy import ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.database import Base
from models.config.ProductCategory import ProductCategory


class Product(Base):
    __tablename__ = "products"

    def __init__(self, name: str, product_category: ProductCategory, **kw: Any) -> None:
        super().__init__(**kw)
        self.name = name
        self.category_id = product_category.id

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column()
    category_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("product_categories.id"))

    category: Mapped["ProductCategory"] = relationship(back_populates="products")
