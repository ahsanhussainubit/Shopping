from fastapi import APIRouter, Depends
from ..repository import ProductRepository
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..schemas import ProductCreate

router = APIRouter(prefix="/products",tags=["products"])


@router.get("/{product_id}")
async def get_product_by_id(product_id:int,db: AsyncSession = Depends(get_db)):
    return await ProductRepository.get_product_by_id(product_id,db)

@router.post("")
async def create_product(product:ProductCreate,db: AsyncSession = Depends(get_db)):
    return await ProductRepository.create(product,db)