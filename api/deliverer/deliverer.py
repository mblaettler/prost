from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

from api.auth import verify_deliverer
from api.database import get_db
from api.schemas import ProductState
from models.order.ProductState import ProductState as ProductStateModel, ProductStatus
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

@router.put("/{bar_id}/{product_id}/state/enough", response_model=list[ProductState])
def update_product_state_enough(bar_id: UUID, product_id: UUID, db: Session = Depends(get_db)):
    db_product_state = db.get(ProductStateModel, (product_id, bar_id))
    if db_product_state is None:
        db_product_state = ProductStateModel(product_id=product_id, bar_id=bar_id, status=ProductStatus.ENOUGH)
        db_product_state = db.merge(db_product_state)
    db_product_state.status = ProductStatus.ENOUGH
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        db_product_state = db.get(ProductStateModel, (product_id, bar_id))
    return get_not_enough_products(db)