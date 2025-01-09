from ..model.schemas import ProductCreate,ShowProduct
from ..database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from ..model import models
from sqlalchemy import select
from sqlalchemy.orm import selectinload

async def get_product_by_id(product_id:int,db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Product).options(selectinload(models.Product.category)).filter(models.Product.id == product_id))
    product = result.scalar()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {product_id} not found")
    return ShowProduct(**product.__dict__)

async def create(product:ProductCreate,db: AsyncSession = Depends(get_db)):
    new_product = models.Product(name=product.name, description=product.description, price=product.price, category_id=product.category_id)
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product