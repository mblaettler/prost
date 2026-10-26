from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

from api.auth import verify_deliverer
from api.database import get_db
from api.schemas import ProductState
from models.order.ProductState import ProductState as ProductStateModel, ProductStatus, DELIVERER_TRANSITIONS
from models.config.Product import Product as ProductModel

router = APIRouter(
    prefix="/deliverer/product",
    tags=["deliverer"],
    dependencies=[Depends(verify_deliverer)]
)

@router.get("/not_enough", response_model=list[ProductState])
def get_not_enough_products(db: Session = Depends(get_db)):
    # Query all product states where status is not ENOUGH
    not_enough_product_states = db.query(ProductStateModel).filter(
        ProductStateModel.status != ProductStatus.ENOUGH
    ).options(
        joinedload(ProductStateModel.product).joinedload(ProductModel.category)
    ).all()

    return not_enough_product_states

def set_product_state(bar_id: UUID, product_id: UUID, status: ProductStatus, db: Session):
    db_product_state = db.get(ProductStateModel, (product_id, bar_id))
    current_status = db_product_state.status if db_product_state is not None else ProductStatus.ENOUGH
    if status not in DELIVERER_TRANSITIONS[current_status]:
        raise HTTPException(status_code=409, detail=f"Cannot change status from {current_status.value} to {status.value}")
    db_product_state.status = status
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
    return get_not_enough_products(db)

@router.put("/{bar_id}/{product_id}/state/in_progress", response_model=list[ProductState])
def update_product_state_in_progress(bar_id: UUID, product_id: UUID, db: Session = Depends(get_db)):
    return set_product_state(bar_id, product_id, ProductStatus.IN_PROGRESS, db)

@router.put("/{bar_id}/{product_id}/state/enough", response_model=list[ProductState])
def update_product_state_enough(bar_id: UUID, product_id: UUID, db: Session = Depends(get_db)):
    return set_product_state(bar_id, product_id, ProductStatus.ENOUGH, db)
