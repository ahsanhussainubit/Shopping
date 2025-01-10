from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database URL updated to use the shared volume location for SQLite
SQL_ALCHEMY_DATABASE_URL = f"sqlite+aiosqlite:///{os.environ.get('SQLITE_DB_PATH', './data/shopping.db')}"

# Create async engine with the updated database URL
engine = create_async_engine(SQL_ALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)

# SessionLocal for handling database sessions asynchronously
AsyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# Base class for model classes
Base = declarative_base()

# Dependency to get the database session
async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()
