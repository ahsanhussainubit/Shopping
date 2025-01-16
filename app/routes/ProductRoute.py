from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..model.schemas import ProductCreate
from ..repository import ProductRepository

router = APIRouter(
    prefix="/products",
    tags=["products"],
    # dependencies=[Depends(get_current_user)]
    )


@router.get("/{product_id}")
async def get_product_by_id(product_id:int,db: AsyncSession = Depends(get_db)):
    return await ProductRepository.get_product_by_id(product_id,db)


@router.get("/")
async def get_products(keyword:str="",page:int=1,limit:int=10,db: AsyncSession = Depends(get_db)):
    return await ProductRepository.get_products(keyword,page, limit, db)

@router.post("")
async def create_product(product:ProductCreate,db: AsyncSession = Depends(get_db)):
    return await ProductRepository.create(product,db)
