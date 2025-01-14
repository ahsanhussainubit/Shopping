import asyncio

import nest_asyncio
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.database import engine
from app.model import models
from app.routes import OrderRoute, AuthenticationRoute, UserRoute, ProductRoute, CategoryRoute, StaticRoute

app = FastAPI(title="Shopping App",version="v1")
app.include_router(AuthenticationRoute.router)
app.include_router(UserRoute.router)
app.include_router(OrderRoute.router)
app.include_router(ProductRoute.router)
app.include_router(StaticRoute.router)
app.include_router(CategoryRoute.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.add_middleware(AdvancedMiddleware)

# models.Base.metadata.create_all(bind=engine)

nest_asyncio.apply()

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

asyncio.run(create_tables())