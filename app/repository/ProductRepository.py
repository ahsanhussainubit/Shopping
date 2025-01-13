from math import ceil
import traceback
from ..model.schemas import ProductCreate,ShowProduct,ShowCategory
from ..database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from ..model import models
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload



async def get_product_by_id(product_id: int, db: AsyncSession):
    result = await db.execute(select(models.Product).options(selectinload(models.Product.category)).filter(models.Product.id == product_id))
    product = result.scalar()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {product_id} not found")
    return ShowProduct(**product.__dict__)

async def create(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    try:
        # Create the new product with the correct many-to-many relationship
        new_product = models.Product(
            title=product.title,
            description=product.description,
            price=product.price,
            img_url=product.img_url,
            product_url=product.product_url,
            stars=product.stars,
            reviews=product.reviews,
            list_price=product.list_price,
            is_best_seller=product.is_best_seller,
            bought_in_last_month=product.bought_in_last_month,
            category_id=product.category_id,  # Directly set the category_id here
        )

        # Add the product to the session
        db.add(new_product)

        # Commit and refresh asynchronously
        await db.commit()
        await db.refresh(new_product)

        # Return the newly created product
        return new_product

    except Exception as e:
        # Capture detailed error for debugging
        traceback_str = ''.join(traceback.format_exception(None, e, e.__traceback__))
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {traceback_str}")

async def get_products(
    keyword: str = "", 
    page: int = 1, 
    limit: int = 10, 
    category_id: int = None, 
    db: AsyncSession = Depends(get_db)
):
    # Base query for products
    query = select(models.Product).options(selectinload(models.Product.category))
    
    # Add filters
    if keyword:
        query = query.filter(func.lower(models.Product.title).like(f"%{keyword.lower()}%"))
    if category_id:
        query = query.filter(models.Product.category_id == category_id)
    
    # Count total number of matching products
    count_query = query.with_only_columns(func.count()).scalar_subquery()
    total_products = (await db.execute(select(count_query))).scalar()
    
    # Calculate total pages
    total_pages = ceil(total_products / limit) if total_products else 1
    
    # Paginated query
    query = (
        query.order_by(models.Product.id)
        .offset((page - 1) * limit)
        .limit(limit)
    )
    result = await db.execute(query)
    products = result.scalars().all()
    
    # Response
    return {
        "products": [ShowProduct(**p.__dict__) for p in products],
        "total_pages": total_pages
    }