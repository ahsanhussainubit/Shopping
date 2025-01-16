from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.repository import CategoryRepository
from app.model.schemas import CreateCategory

router = APIRouter(
    prefix="/category",
    tags=["category"],
    # dependencies=[Depends(get_current_user)]  # Uncomment if authentication is needed
)


@router.get("/{category_id}")
async def get_category_by_id(category_id: int, db: AsyncSession = Depends(get_db)):
    return await CategoryRepository.get_category_by_id(category_id, db)


@router.get("/")
async def get_categories(
    db: AsyncSession = Depends(get_db),
):
    return await CategoryRepository.get_categories(db)


@router.post("")
async def create_category(
    category: CreateCategory,
    db: AsyncSession = Depends(get_db)
):
    return await CategoryRepository.create_category(category, db)
