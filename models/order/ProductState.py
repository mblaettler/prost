import enum
import uuid
from sqlalchemy import ForeignKey, Enum, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from models.config.Orderer import Orderer
from models.config.Product import Product
from models.database import Base


class ProductStatus(enum.Enum):
    NEW = "NEW"
    PROCESSED = "PROCESSED"


class ProductState(Base):
    __tablename__ = "product_states"

    def __init__(self, product: Product, owner: Orderer) -> None:
        super().__init__()
        self.status = ProductStatus.NEW
        self.product = product.id
        self.owner = owner.id

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    status: Mapped[ProductStatus] = mapped_column(Enum(ProductStatus))
    product: Mapped[uuid.UUID] = mapped_column(ForeignKey("products.id"))
    owner: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
