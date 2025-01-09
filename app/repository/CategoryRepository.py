from ..model.schemas import CategoryCreate,ShowCategory
from ..database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from ..model import models
from sqlalchemy import select

async def get_category_by_id(category_id:int,db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Category).filter(models.Category.id == category_id))
    category = result.scalar()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with id {category_id} not found")
    return ShowCategory(**category.__dict__)


async def get_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Category))
    categories = result.scalars().all()
    if not categories:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No categories found")
    return [ShowCategory(**category.__dict__) for category in categories]

async def create(category:CategoryCreate,db: AsyncSession = Depends(get_db)):
    new_category = models.Category(name=category.name)
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    return new_category