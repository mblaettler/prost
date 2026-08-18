from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from models.config.Product import Product as ProductModel
from models.config.ProductCategory import ProductCategory as ProductCategoryModel
from api.schemas import Product, ProductCreate
from api.auth import verify_admin

router = APIRouter(
    prefix="/config/products",
    tags=["products"],
    dependencies=[Depends(verify_admin)]
)

from api.database import get_db

@router.post("/", response_model=Product)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    category = db.get(ProductCategoryModel, product.category_id)
    if not category:
        raise HTTPException(status_code=400, detail="Invalid category_id")
    
    db_product = ProductModel(name=product.name, product_category=category)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/", response_model=List[Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.scalars(select(ProductModel).offset(skip).limit(limit)).all()
    return products

@router.get("/{product_id}", response_model=Product)
def read_product(product_id: UUID, db: Session = Depends(get_db)):
    product = db.get(ProductModel, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=Product)
def update_product(product_id: UUID, product_update: ProductCreate, db: Session = Depends(get_db)):
    db_product = db.get(ProductModel, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    category = db.get(ProductCategoryModel, product_update.category_id)
    if not category:
        raise HTTPException(status_code=400, detail="Invalid category_id")

    db_product.name = product_update.name
    db_product.category_id = product_update.category_id
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/{product_id}")
def delete_product(product_id: UUID, db: Session = Depends(get_db)):
    db_product = db.get(ProductModel, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"detail": "Product deleted"}
