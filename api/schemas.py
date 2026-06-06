from pydantic import BaseModel
from uuid import UUID

from models.config.User import UserRole
from models.order.ProductState import ProductStatus


class ProductCategoryBase(BaseModel):
    name: str

class ProductCategoryCreate(ProductCategoryBase):
    pass

class ProductCategory(ProductCategoryBase):
    id: UUID

class ProductBase(BaseModel):
    name: str
    category_id: UUID

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: UUID

class UserBase(BaseModel):
    name: str
    role: UserRole
    model_config = {
        "from_attributes": True,
        "use_enum_values": True,
    }

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: UUID
    # password_hash is omitted for security in general output

class Token(BaseModel):
    access_token: str
    token_type: str

class ProductState(BaseModel):
    product: Product
    bar: User
    status: ProductStatus
