"""
Drop-in replacement for article_repo.py — adds segment classification.
Rename this to article_repo.py to activate.
"""
from app.database import get_pool
from app.services.segment_classifier import classify_segment
from typing import List, Dict, Optional
import uuid

async def save_articles(articles: List[Dict]) -> int:
    pool = await get_pool()
    saved = 0
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            for a in articles:
                segment = classify_segment(
                    a.get("title", ""),
                    a.get("summary", "")
                )
                try:
                    await cur.execute("""
                        INSERT IGNORE INTO articles
                            (id, url_hash, title, summary, url, image_url,
                             source, category, is_breaking, published_at, segment)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """, (
                        str(uuid.uuid4()),
                        a["url_hash"], a["title"], a["summary"], a["url"],
                        a["image_url"], a["source"], a["category"],
                        a["is_breaking"], a["published_at"], segment,
                    ))
                    if cur.rowcount > 0:
                        saved += 1
                except Exception as e:
                    print(f"[Repo] Save error: {e}")
    return saved

async def backfill_segments():
    """Run once to classify all existing articles that have no segment."""
    from app.services.segment_classifier import classify_segment
    pool = await get_pool()
    updated = 0
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "SELECT id, title, summary FROM articles WHERE segment IS NULL LIMIT 1000"
            )
            rows = await cur.fetchall()
            for row in rows:
                art_id, title, summary = row
                segment = classify_segment(title or "", summary or "")
                if segment:
                    await cur.execute(
                        "UPDATE articles SET segment = %s WHERE id = %s",
                        (segment, art_id)
                    )
                    updated += 1
    print(f"[Backfill] Updated {updated} articles with segments")
    return updated

async def get_article_by_id(article_id: str) -> Optional[Dict]:
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""
                SELECT id, title, summary, url, image_url,
                       source, category, is_breaking, published_at
                FROM articles WHERE id = %s
            """, (article_id,))
            row = await cur.fetchone()
            if not row:
                return None
            cols = ["id","title","summary","url","image_url","source","category","is_breaking","published_at"]
            return dict(zip(cols, row))
