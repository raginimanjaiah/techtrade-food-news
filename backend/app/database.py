# app/database.py
import aiomysql
import redis.asyncio as aioredis
import os

_pool = None
_redis = None

async def get_pool():
    global _pool
    if _pool is None:
        _pool = await aiomysql.create_pool(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER", "techtrade"),
            password=os.getenv("DB_PASSWORD", ""),
            db=os.getenv("DB_NAME", "techtrade_food"),
            minsize=2,
            maxsize=10,
            autocommit=True,
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
        _pool.close()
        await _pool.wait_closed()
    if _redis:
        await _redis.aclose()
