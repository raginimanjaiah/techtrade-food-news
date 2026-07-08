import json
from fastapi import APIRouter, Query
from app.database import get_pool, get_redis
from app.services.segment_classifier import get_all_segments
from app.models import Article, FeedResponse

router = APIRouter()

@router.get("/segments")
async def list_segments():
    """List all food industry segments with article counts."""
    pool      = await get_pool()
    redis     = await get_redis()
    cache_key = "segments:list"

    cached = await redis.get(cache_key)
    if cached:
        return json.loads(cached)

    segments = get_all_segments()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            for s in segments:
                await cur.execute(
                    "SELECT COUNT(*) FROM articles WHERE segment = %s",
                    (s["key"],)
                )
                row = await cur.fetchone()
                s["count"] = row[0] if row else 0

    await redis.setex(cache_key, 300, json.dumps(segments))
    return segments

@router.get("/segments/{segment_key}", response_model=FeedResponse)
async def get_segment_feed(
    segment_key: str,
    page:  int = Query(1, ge=1),
    limit: int = Query(20, le=50),
):
    """Get news articles for a specific food segment."""
    offset    = (page - 1) * limit
    cache_key = f"segment:{segment_key}:{page}:{limit}"
    redis     = await get_redis()

    cached = await redis.get(cache_key)
    if cached:
        return FeedResponse(**json.loads(cached))

    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""
                SELECT id, title, summary, url, image_url,
                       source, category, is_breaking, published_at
                FROM   articles
                WHERE  segment = %s
                ORDER  BY is_breaking DESC, published_at DESC
                LIMIT  %s OFFSET %s
            """, (segment_key, limit, offset))
            rows  = await cur.fetchall()

            await cur.execute(
                "SELECT COUNT(*) FROM articles WHERE segment = %s",
                (segment_key,)
            )
            total_row = await cur.fetchone()
            total     = total_row[0] if total_row else 0

    columns  = ["id","title","summary","url","image_url","source","category","is_breaking","published_at"]
    articles = [Article(**dict(zip(columns, r))) for r in rows]
    payload  = FeedResponse(articles=articles, page=page, limit=limit, total=total)
    await redis.setex(cache_key, 180, payload.model_dump_json())
    return payload
