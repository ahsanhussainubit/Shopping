from ..model.schemas import OrderCreate,ShowOrder
from ..database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from ..model import models
from sqlalchemy import select
from sqlalchemy.orm import joinedload

async def get_order_by_id(order_id:int,db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Order).filter(models.Order.id == order_id))
    order = result.scalar()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id {order_id} not found")
    return ShowOrder(**order.__dict__)

async def get_orders_by_user_id(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Order).filter(models.Order.user_id == user_id))
    orders = result.scalars().all()
    if not orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No orders found for User id {user_id}")
    return [ShowOrder(**order.__dict__) for order in orders]

async def create(order: OrderCreate,user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Product).filter(models.Product.id.in_(order.product_ids)))
    products = result.scalars().all()

    new_order = models.Order(user_id=user_id, status=order.status,products=products)

    db.add(new_order)
    await db.commit()

    await db.refresh(new_order)
    await db.execute(select(models.Order).options(joinedload(models.Order.products)).filter(models.Order.id == new_order.id))

    # Return the new order as a response
    return new_order