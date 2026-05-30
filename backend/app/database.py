import asyncpg
import redis.asyncio as aioredis
import os

_pool = None
_redis = None

async def get_pool():
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(
            os.getenv("DATABASE_URL", "postgresql://localhost/techtrade_food"),
            min_size=2, max_size=10,
        )
    return _pool

async def get_redis():
    global _redis
    if _redis is None:
        _redis = await aioredis.from_url(
            os.getenv("REDIS_URL", "redis://localhost:6379"),
            decode_responses=True,
        )
    return _redis

async def close_pool():
    global _pool, _redis
    if _pool:
        await _pool.close()
    if _redis:
        await _redis.aclose()
