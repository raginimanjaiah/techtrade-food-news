# app/services/article_repo.py
from app.database import get_pool
from typing import List, Dict, Optional
import uuid, hashlib

async def save_articles(articles: List[Dict]) -> int:
    pool = await get_pool()
    saved = 0
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            for a in articles:
                try:
                    await cur.execute("""
                        INSERT IGNORE INTO articles
                            (id, url_hash, title, summary, url, image_url,
                             source, category, is_breaking, published_at)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """, (
                        str(uuid.uuid4()),
                        a["url_hash"], a["title"], a["summary"], a["url"],
                        a["image_url"], a["source"], a["category"],
                        a["is_breaking"], a["published_at"],
                    ))
                    if cur.rowcount > 0:
                        saved += 1
                except Exception as e:
                    print(f"[Repo] Save error: {e}")
    return saved

async def get_article_by_id(article_id: str) -> Optional[Dict]:
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute("""
                SELECT id, title, summary, url, image_url,
                       source, category, is_breaking, published_at
                FROM articles WHERE id = %s
            """, (article_id,))
            return await cur.fetchone()
