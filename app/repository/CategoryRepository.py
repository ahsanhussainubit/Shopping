from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from ..model.schemas import CreateCategory, ShowCategory
from ..database import get_db
from ..model import models

async def get_category_by_id(category_id: int, db: AsyncSession = Depends(get_db)):
    # Query for the category using its ID
    result = await db.execute(select(models.Category).filter(models.Category.id == category_id))
    category = result.scalar()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {category_id} not found"
        )
    return ShowCategory(**category.__dict__)

async def create_category(category: CreateCategory, db: AsyncSession = Depends(get_db)):
    # Create a new category
    new_category = models.Category(name=category.name)
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    return ShowCategory(**new_category.__dict__)

async def get_categories(db: AsyncSession = Depends(get_db)):
    # Query all categories
    result = await db.execute(select(models.Category))
    categories = result.scalars().all()
    return [ShowCategory(**category.__dict__) for category in categories]
