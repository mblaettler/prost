from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/config/products",
    tags=["products"],
    dependencies=[Depends(verify_orderer)]
)
