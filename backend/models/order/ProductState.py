import enum
import uuid
from sqlalchemy import ForeignKey, Enum, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.config.User import User
from models.config.Product import Product
from models.database import Base


class ProductStatus(enum.Enum):
    ENOUGH = "ENOUGH"
    REQUIRED = "REQUIRED"
    EMERGENCY = "EMERGENCY"


class ProductState(Base):
    __tablename__ = "product_states"

    def __init__(self, product_id: uuid.UUID, bar_id: uuid.UUID, status: ProductStatus = ProductStatus.ENOUGH) -> None:
        super().__init__()
        self.status = status
        self.product_id = product_id
        self.bar_id = bar_id

    product_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("products.id"), primary_key=True)
    bar_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    status: Mapped[ProductStatus] = mapped_column(Enum(ProductStatus))

    product: Mapped[Product] = relationship()
    bar: Mapped[User] = relationship()
