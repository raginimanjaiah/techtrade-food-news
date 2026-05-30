from app.database import get_pool
from typing import List, Dict, Optional

async def save_articles(articles: List[Dict]) -> int:
    pool = await get_pool()
    saved = 0
    async with pool.acquire() as conn:
        for a in articles:
            try:
                result = await conn.execute("""
                    INSERT INTO articles
                        (url_hash, title, summary, url, image_url, source,
                         category, is_breaking, published_at)
                    VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)
                    ON CONFLICT (url_hash) DO NOTHING
                """,
                    a["url_hash"], a["title"], a["summary"], a["url"],
                    a["image_url"], a["source"], a["category"],
                    a["is_breaking"], a["published_at"],
                )
                if result == "INSERT 0 1":
                    saved += 1
            except Exception as e:
                print(f"[Repo] Save error: {e}")
    return saved

async def get_article_by_id(article_id: str) -> Optional[Dict]:
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("""
            SELECT id::text, title, summary, url, image_url,
                   source, category, is_breaking, published_at
            FROM   articles WHERE id = $1::uuid
        """, article_id)
        return dict(row) if row else None
