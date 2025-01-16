from aioredis import Redis, from_url
from typing import List
from app.model.settings import settings
from urllib.parse import urlparse

# Global variable to hold Redis clients
redis_clients: List[Redis] = []


async def init_redis() -> List[Redis]:
    global redis_clients
    # Parse the Redis URL into its components
    parsed_url = urlparse(settings.redis_url)

    redis_clients = [
        await from_url(f"{parsed_url.scheme}://{parsed_url.hostname}:{6379 + i}", decode_responses=True)
        for i in range(settings.redis_instances_count)  # Use the number of instances from settings
    ]

    return redis_clients


# Function to get Redis clients
def get_redis_clients() -> List[Redis]:
    if not redis_clients:
        raise RuntimeError("Redis clients are not initialized.")
    return redis_clients


# Set value with lock and expiry (using NX and PX)
async def set_value_with_lock(key: str, value: str, lock_key: str, lock_timeout: int = 10, value_timeout: int = 60, instance_index: int = 0):
    """
    Set a key-value pair with a lock in the specified Redis instance. Lock expires after `lock_timeout` seconds.
    Value expires after `value_timeout` seconds.
    """
    redis_client = redis_clients[instance_index]

    # Try to acquire the lock (with expiry)
    lock_acquired = await redis_client.set(lock_key, "locked", ex=lock_timeout, nx=True)

    if lock_acquired:
        # Lock acquired, proceed with setting the value
        await redis_client.set(key, value, ex=value_timeout)  # Set value with longer expiry
        print(f"Lock acquired! Set value: {key} = {value} in Redis instance {instance_index}")
    else:
        print(f"Failed to acquire lock for key: {lock_key}. Try again later.")
        return False  # Lock not acquired, return failure

    return True


# Get value from a specified Redis instance
async def get_value(key: str, instance_index: int = 0) -> str:
    """
    Get the value of a key from a specified Redis instance (default is first instance)
    """
    redis_client = redis_clients[instance_index]

    value = await redis_client.get(key)
    print(f"Got value for {key}: {value} from Redis instance {instance_index}")
    return value


# Unlocking the key by deleting the lock key
async def release_lock(lock_key: str, instance_index: int = 0):
    """
    Release the lock by deleting the lock key
    """
    redis_client = redis_clients[instance_index]
    await  redis_client.delete()
    await redis_client.delete(lock_key)
    print(f"Lock released for {lock_key} from Redis instance {instance_index}")




######## how to use this #######
# @router.get("/{category_id}")
# async def get_category_by_id(category_id: int, db: AsyncSession = Depends(get_db)):
#     lock_acquired = await redis_client.set_value_with_lock("key", "value", redis_client.LOCK_KEY, lock_timeout=20)
#     if lock_acquired:
#         await asyncio.sleep(20)  # Delay for 20 seconds
#         # Proceed with category creation if the lock is acquired
#         result = await CategoryRepository.get_category_by_id(category_id, db)
#         # Release the lock after operation
#         await redis_client.release_lock(redis_client.LOCK_KEY)
#         return result
#     else:
#         return {"message": "Failed to acquire lock, try again later."}
#
#
# @router.get("/")
# async def get_categories(
#     db: AsyncSession = Depends(get_db),
# ):
#     value = await redis_client.get_value("key")
#     return await CategoryRepository.get_categories(db)
