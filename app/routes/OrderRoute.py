from fastapi import APIRouter, Depends
from ..repository import OrderRepository
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..schemas import OrderCreate

router = APIRouter(prefix="/orders",tags=["orders"])


@router.get("/{order_id}")
async def get_order_by_id(order_id:int,db: AsyncSession = Depends(get_db)):
    return await OrderRepository.get_order_by_id(order_id,db)

@router.get("/user/{user_id}")
async def get_orders_by_user_id(user_id:int,db: AsyncSession = Depends(get_db)):
    return await OrderRepository.get_orders_by_user_id(user_id,db)


@router.post("")
async def create_order(order:OrderCreate,db: AsyncSession = Depends(get_db)):
    return await OrderRepository.create(order,db)