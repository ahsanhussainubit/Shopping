import asyncio
from contextlib import asynccontextmanager
import nest_asyncio
from fastapi import FastAPI, Depends
import redlock
from starlette.middleware.cors import CORSMiddleware
from app.database import engine
from app.model import models
from app.routes import OrderRoute, AuthenticationRoute, UserRoute, ProductRoute, CategoryRoute, StaticRoute
from redis_client import init_redis, get_redis_clients

# Initialize RedLock
async def init_redlock():
    redis_clients = await init_redis()  # Initialize Redis clients for multiple instances
    return redlock.Redlock(redis_clients)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    redis_clients = await init_redis()  # Initialize Redis clients
    redlock = await init_redlock()  # Initialize RedLock with multiple Redis clients

    app.state.redis = redis_clients
    app.state.redlock = redlock  # Store RedLock in app state
    print("Application started and Redis connected.")

    yield  # Allows the application to handle requests

    # Shutdown logic
    for redis_client in redis_clients:
        await redis_client.close()
    print("Application shut down and Redis connections closed.")

# Initialize FastAPI app with lifespan event
app = FastAPI(
    title="Shopping App",
    version="v1",
    lifespan=lifespan
)

# Include routers
app.include_router(AuthenticationRoute.router)
app.include_router(UserRoute.router)
app.include_router(OrderRoute.router)
app.include_router(ProductRoute.router)
app.include_router(StaticRoute.router)
app.include_router(CategoryRoute.router)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Apply nest_asyncio for compatibility with running inside Jupyter Notebooks or other environments
nest_asyncio.apply()

# Database table creation
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

asyncio.run(create_tables())

