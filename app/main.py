import asyncio
from fastapi import FastAPI
from app.routes import OrderRoute, AuthenticationRoute, UserRoute, ProductRoute
from app.database import engine
from app.models import Base
from app import models
import asyncio
import nest_asyncio

app = FastAPI(title="Shopping App",version="v1")
app.include_router(AuthenticationRoute.router)
app.include_router(UserRoute.router)
app.include_router(OrderRoute.router)
app.include_router(ProductRoute.router)

# models.Base.metadata.create_all(bind=engine)

nest_asyncio.apply()

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

asyncio.run(create_tables())