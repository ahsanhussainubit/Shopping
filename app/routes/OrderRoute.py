from fastapi import APIRouter, Depends
from ..repository import OrderRepository
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..model.schemas import OrderCreate
from ..auth.oauth2 import get_current_user

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    dependencies=[Depends(get_current_user)]
)


@router.get("/{order_id}")
async def get_order_by_id(order_id: int, db: AsyncSession = Depends(get_db)):
    return await OrderRepository.get_order_by_id(order_id, db)

@router.get("/user/")
async def get_orders_by_user_id(user_id: int | None = None, db: AsyncSession = Depends(get_db), current_user_id: int = Depends(get_current_user)):
    if user_id is None:
        user_id = current_user_id
    return await OrderRepository.get_orders_by_user_id(user_id, db)

@router.post("")
async def create_order(order: OrderCreate, db: AsyncSession = Depends(get_db), current_user_id: int = Depends(get_current_user)):
    return await OrderRepository.create(order, current_user_id, db)