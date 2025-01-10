from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.declarative import declarative_base

# Create an async engine for database connection
DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5433/shopping_db"
engine = create_async_engine(DATABASE_URL, echo=True)

# Use `run_sync` to handle the migrations
def run_migrations_online():
    connectable = engine

    # Wrap the async context in a sync function
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            literal_binds=True,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()
