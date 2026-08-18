from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from models.config.ProductCategory import ProductCategory as ProductCategoryModel
from api.schemas import ProductCategory, ProductCategoryCreate
from api.auth import verify_admin

# Assume there is a function to get the DB session
# In a real app this would be imported from a db.py or similar
# For now, I'll need a mock or assume it will be provided in main.py

router = APIRouter(
    prefix="/config/product-categories",
    tags=["product-categories"],
    dependencies=[Depends(verify_admin)]
)

from api.database import get_db

@router.post("/", response_model=ProductCategory)
def create_category(category: ProductCategoryCreate, db: Session = Depends(get_db)):
    db_category = ProductCategoryModel(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.get("/", response_model=List[ProductCategory])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = db.scalars(select(ProductCategoryModel).offset(skip).limit(limit)).all()
    return categories

@router.get("/{category_id}", response_model=ProductCategory)
def read_category(category_id: UUID, db: Session = Depends(get_db)):
    category = db.get(ProductCategoryModel, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/{category_id}", response_model=ProductCategory)
def update_category(category_id: UUID, category_update: ProductCategoryCreate, db: Session = Depends(get_db)):
    db_category = db.get(ProductCategoryModel, category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db_category.name = category_update.name
    db.commit()
    db.refresh(db_category)
    return db_category

@router.delete("/{category_id}")
def delete_category(category_id: UUID, db: Session = Depends(get_db)):
    db_category = db.get(ProductCategoryModel, category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(db_category)
    db.commit()
    return {"detail": "Category deleted"}
