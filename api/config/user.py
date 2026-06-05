from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from api.database import get_db
from models.config.User import User as UserModel, UserRole
from api.config.schemas import User, UserCreate
from api.auth import verify_admin, hash_password

router = APIRouter(
    prefix="/config/users",
    tags=["users"],
    dependencies=[Depends(verify_admin)]
)


@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_db = db.query(UserModel).filter(UserModel.name == user.name).first()
    if user_db:
        raise HTTPException(status_code=400, detail="User already exists")

    user_db = UserModel(name=user.name, password_hash=hash_password(user.password), role=UserRole(user.role))
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


@router.get("/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.scalars(select(UserModel).offset(skip).limit(limit)).all()
    return users


@router.get("/{user_id}", response_model=User)
def read_user(user_id: UUID, db: Session = Depends(get_db)):
    user = db.get(UserModel, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return user


@router.put("/{user_id}", response_model=User)
def update_user(user_id: UUID, user_update: UserCreate, db: Session = Depends(get_db)):
    db_user = db.get(UserModel, user_id)

    db_user.name = user_update.name
    db_user.password_hash = hash_password(user_update.password)
    db_user.role = user_update.role

    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/{user_id}")
def delete_product(user_id: UUID, db: Session = Depends(get_db)):
    db_user = db.get(UserModel, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_user)
    db.commit()
    return {"detail": "Product deleted"}
