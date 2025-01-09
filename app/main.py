import asyncio
from fastapi import FastAPI, Path
from fastapi.staticfiles import StaticFiles
from app.routes import OrderRoute, AuthenticationRoute, UserRoute, ProductRoute,StaticRoute
from app.database import engine
from app.model.models import Base
from app.model import models
import asyncio
import nest_asyncio
from app.logs.middleware import AdvancedMiddleware

app = FastAPI(title="Shopping App",version="v1")
app.include_router(AuthenticationRoute.router)
app.include_router(UserRoute.router)
app.include_router(OrderRoute.router)
app.include_router(ProductRoute.router)
app.add_middleware(AdvancedMiddleware)
app.include_router(StaticRoute.router)

# models.Base.metadata.create_all(bind=engine)

nest_asyncio.apply()

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

asyncio.run(create_tables())