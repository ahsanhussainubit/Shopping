from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_ALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./shopping.db"

engine = create_async_engine(SQL_ALCHEMY_DATABASE_URL,connect_args={"check_same_thread": False},echo=True)

AsyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

Base = declarative_base()


async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
         await db.close()