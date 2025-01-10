from fastapi import APIRouter, Depends
from ..repository import ProductRepository
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..model.schemas import ProductCreate
from ..auth.oauth2 import get_current_user

router = APIRouter(
    prefix="/products",
    tags=["products"],
    # dependencies=[Depends(get_current_user)]
    )


@router.get("/{product_id}")
async def get_product_by_id(product_id:int,db: AsyncSession = Depends(get_db)):
    return await ProductRepository.get_product_by_id(product_id,db)


@router.get("/")
async def get_products(db: AsyncSession = Depends(get_db)):
    return await ProductRepository.get_products(db)

@router.post("")
async def create_product(product:ProductCreate,db: AsyncSession = Depends(get_db)):
    return await ProductRepository.create(product,db)
