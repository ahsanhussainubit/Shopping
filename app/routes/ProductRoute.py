from fastapi import APIRouter, Depends
from ..repository import ProductRepository
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..model.schemas import ProductCreate,ShowUser
from ..auth.oauth2 import get_current_user

router = APIRouter(prefix="/products",tags=["products"])


@router.get("/{product_id}")
async def get_product_by_id(product_id:int,db: AsyncSession = Depends(get_db),user:ShowUser = Depends(get_current_user)):
    return await ProductRepository.get_product_by_id(product_id,db)

@router.post("")
async def create_product(product:ProductCreate,db: AsyncSession = Depends(get_db),user:ShowUser = Depends(get_current_user)):
    return await ProductRepository.create(product,db)