# app/routers/feed.py
import json
from fastapi import APIRouter, Query, HTTPException
from app.database import get_pool, get_redis
from app.models import FeedResponse, Article

router = APIRouter()

@router.get("/feed", response_model=FeedResponse)
async def get_feed(
    category: str = Query("all"),
    page:     int = Query(1, ge=1),
    limit:    int = Query(20, le=50),
):
    offset    = (page - 1) * limit
    cache_key = f"feed:{category}:{page}:{limit}"
    redis     = await get_redis()

    cached = await redis.get(cache_key)
    if cached:
        return FeedResponse(**json.loads(cached))

    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            if category == "all":
                await cur.execute("""
                    SELECT id, title, summary, url, image_url,
                           source, category, is_breaking, published_at
                    FROM   articles
                    ORDER  BY is_breaking DESC, published_at DESC
                    LIMIT  %s OFFSET %s
                """, (limit, offset))
                rows = await cur.fetchall()
                await cur.execute("SELECT COUNT(*) FROM articles")
            else:
                await cur.execute("""
                    SELECT id, title, summary, url, image_url,
                           source, category, is_breaking, published_at
                    FROM   articles
                    WHERE  category = %s
                    ORDER  BY is_breaking DESC, published_at DESC
                    LIMIT  %s OFFSET %s
                """, (category, limit, offset))
                rows = await cur.fetchall()
                await cur.execute(
                    "SELECT COUNT(*) FROM articles WHERE category = %s",
                    (category,)
                )

            total_row = await cur.fetchone()
            total     = total_row[0] if total_row else 0

    columns  = ["id","title","summary","url","image_url","source","category","is_breaking","published_at"]
    articles = [Article(**dict(zip(columns, r))) for r in rows]
    payload  = FeedResponse(articles=articles, page=page, limit=limit, total=total)
    await redis.setex(cache_key, 300, payload.model_dump_json())
    return payload
