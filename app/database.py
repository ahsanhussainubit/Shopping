from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# PostgreSQL Database URL
DATABASE_URL = "postgresql+asyncpg://user:password@db/shopping_db"

# Creating an async engine with the connection URL
engine = create_async_engine(DATABASE_URL, echo=True)

# Create the async sessionmaker
AsyncSessionMaker = sessionmaker(
    engine,
    class_=AsyncSession,  # Use the actual AsyncSession class here
    expire_on_commit=False
)

# Base class for all models
Base = declarative_base()

# Dependency to get the database session
async def get_db():
    async with AsyncSessionMaker() as db:  # Use AsyncSessionMaker here
        try:
            yield db
        finally:
            await db.close()
