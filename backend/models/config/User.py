import enum
import uuid
from typing import Any

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Uuid
from models.database import Base

class UserRole(enum.Enum):
    ADMIN = "admin"
    BAR = "bar"
    DELIVERER = "deliverer"

class User(Base):
    __tablename__ = "users"

    def __init__(self, name: str, password_hash: str, role: UserRole, **kw: Any) -> None:
        super().__init__(**kw)
        self.name = name
        self.password_hash = password_hash
        self.role = role

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column()
    password_hash: Mapped[str] = mapped_column()
    role: Mapped[UserRole] = mapped_column()
