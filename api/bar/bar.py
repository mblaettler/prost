from fastapi import APIRouter, Depends
from uuid import UUID
from sqlalchemy.orm import Session, joinedload

from api.auth import verify_bar
from api.database import get_db
from api.schemas import ProductState
from models.order.ProductState import ProductState as ProductStateModel, ProductStatus
from models.config.Product import Product as ProductModel
from models.config.User import User as UserModel

router = APIRouter(
    prefix="/bar/product",
    tags=["bar"]
)

@router.get("/", response_model=list[ProductState])
def get_product_states(user_id: str = Depends(verify_bar), db: Session = Depends(get_db)):
    product_states_db = db.query(ProductStateModel).where(ProductStateModel.bar_id == user_id).options(
        joinedload(ProductStateModel.product).joinedload(ProductModel.category)
    ).all()
    all_products = db.query(ProductModel).options(joinedload(ProductModel.category)).all()

    existing_product_ids = {ps.product_id for ps in product_states_db}
    
    product_states = list(product_states_db)
    
    bar_user = db.get(UserModel, user_id)

    for product in all_products:
        if product.id not in existing_product_ids:
            new_state = ProductStateModel(product_id=product.id, bar_id=user_id, status=ProductStatus.ENOUGH)
            new_state.product = product
            new_state.bar = bar_user
            product_states.append(new_state)

    return product_states

@router.put("/{product_id}/state/enough", response_model=list[ProductState])
def update_product_state_enough(product_id: UUID, user_id: UUID = Depends(verify_bar), db: Session = Depends(get_db)):
    db_product_state = db.get(ProductStateModel, (product_id, user_id))
    if db_product_state is None:
        db_product_state = ProductStateModel(product_id=product_id, bar_id=user_id)
        db.add(db_product_state)
    db_product_state.status = ProductStatus.ENOUGH
    db.commit()
    return get_product_states(user_id, db)

@router.put("/{product_id}/state/required", response_model=list[ProductState])
def update_product_state_required(product_id: UUID, user_id: UUID = Depends(verify_bar), db: Session = Depends(get_db)):
    db_product_state = db.get(ProductStateModel, (product_id, user_id))
    if db_product_state is None:
        db_product_state = ProductStateModel(product_id=product_id, bar_id=user_id)
        db.add(db_product_state)
    db_product_state.status = ProductStatus.REQUIRED
    db.commit()
    return get_product_states(user_id, db)

@router.put("/{product_id}/state/emergency", response_model=list[ProductState])
def update_product_state_emergency(product_id: UUID, user_id: UUID = Depends(verify_bar), db: Session = Depends(get_db)):
    db_product_state = db.get(ProductStateModel, (product_id, user_id))
    if db_product_state is None:
        db_product_state = ProductStateModel(product_id=product_id, bar_id=user_id)
        db.add(db_product_state)
    db_product_state.status = ProductStatus.EMERGENCY
    db.commit()
    return get_product_states(user_id, db)
