import json
from fastapi import APIRouter, Query, HTTPException
from app.database import get_pool, get_redis
from app.models import FeedResponse, Article
from app.services.article_repo import get_article_by_id

router = APIRouter()

@router.get("/feed", response_model=FeedResponse)
async def get_feed(
    category: str = Query("all", description="all|industry|market_news|technology|regulatory|exhibition"),
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
        if category == "all":
            rows  = await conn.fetch("""
                SELECT id::text, title, summary, url, image_url,
                       source, category, is_breaking, published_at
                FROM   articles
                ORDER  BY is_breaking DESC, published_at DESC
                LIMIT  $1 OFFSET $2
            """, limit, offset)
            total = await conn.fetchval("SELECT COUNT(*) FROM articles")
        else:
            rows  = await conn.fetch("""
                SELECT id::text, title, summary, url, image_url,
                       source, category, is_breaking, published_at
                FROM   articles WHERE category = $1
                ORDER  BY is_breaking DESC, published_at DESC
                LIMIT  $2 OFFSET $3
            """, category, limit, offset)
            total = await conn.fetchval(
                "SELECT COUNT(*) FROM articles WHERE category = $1", category
            )

    articles = [Article(**dict(r)) for r in rows]
    payload  = FeedResponse(articles=articles, page=page, limit=limit, total=total or 0)
    await redis.setex(cache_key, 300, payload.model_dump_json())
    return payload

@router.get("/articles/{article_id}", response_model=Article)
async def get_article(article_id: str):
    article = await get_article_by_id(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return Article(**article)
