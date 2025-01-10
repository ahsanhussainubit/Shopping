import traceback
from ..model.schemas import ProductCreate,ShowProduct,ShowCategory
from ..database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from ..model import models
from sqlalchemy import select
from sqlalchemy.orm import selectinload


async def get_product_by_id(product_id: int, db: AsyncSession):
    result = await db.execute(
        select(models.Product)
        .options(selectinload(models.Product.categories))  # Eager load categories
        .filter(models.Product.id == product_id)
    )
    product = result.scalar()
    
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {product_id} not found")

    # Manually map categories to ShowCategory
    categories = [ShowCategory(id=category.id, name=category.name) for category in product.categories]
    
    return ShowProduct(
        id=product.id,
        title=product.title,
        description=product.description,
        price=product.price,
        imgUrl=product.imgUrl,
        productURL=product.productURL,
        stars=product.stars,
        reviews=product.reviews,
        listPrice=product.listPrice,
        isBestSeller=product.isBestSeller,
        boughtInLastMonth=product.boughtInLastMonth,
        categories=categories
    )
async def create(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    try:
        # Fetch the category by category_id from the database asynchronously
        result = await db.execute(select(models.Category).filter(models.Category.id == product.category_id))
        category = result.scalar_one_or_none()

        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        # Create the new product with the correct many-to-many relationship
        new_product = models.Product(
            title=product.title,
            description=product.description,
            price=product.price,
            imgUrl=product.imgUrl,
            productURL=product.productURL,
            stars=product.stars,
            reviews=product.reviews,
            listPrice=product.listPrice,
            isBestSeller=product.isBestSeller,
            boughtInLastMonth=product.boughtInLastMonth,
            category_id=category.id,  # Directly set the category_id here
            categories=[category],  # Bind the fetched category to the product
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

async def get_products(db: AsyncSession = Depends(get_db)):
    # Use selectinload to eagerly load categories
    result = await db.execute(
        select(models.Product)
        .options(selectinload(models.Product.categories))  # Eagerly load categories
    )
    products = result.scalars().all()

    # Map the products and include categories
    return [
        ShowProduct(
            id=product.id,
            title=product.title,
            description=product.description,
            price=product.price,
            imgUrl=product.imgUrl,
            productURL=product.productURL,
            stars=product.stars,
            reviews=product.reviews,
            listPrice=product.listPrice,
            isBestSeller=product.isBestSeller,
            boughtInLastMonth=product.boughtInLastMonth,
            categories=[
                ShowCategory(id=category.id, name=category.name)
                for category in product.categories
            ]
        )
        for product in products
    ]
