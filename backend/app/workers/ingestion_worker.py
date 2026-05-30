import os
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services.news_sources import fetch_newsdata, fetch_gnews, fetch_rss_feeds
from app.services.article_repo import save_articles

scheduler = AsyncIOScheduler()

async def ingest_all():
    print("[Ingestion] Starting fetch...")
    results = []

    try:
        articles = await fetch_newsdata(os.getenv("NEWSDATA_KEY", ""))
        results.extend(articles)
        print(f"[NewsData]  {len(articles)} articles")
    except Exception as e:
        print(f"[NewsData]  Error: {e}")

    try:
        articles = await fetch_gnews(os.getenv("GNEWS_KEY", ""))
        results.extend(articles)
        print(f"[GNews]     {len(articles)} articles")
    except Exception as e:
        print(f"[GNews]     Error: {e}")

    try:
        rss = await asyncio.get_event_loop().run_in_executor(None, fetch_rss_feeds)
        results.extend(rss)
        print(f"[RSS]       {len(rss)} articles")
    except Exception as e:
        print(f"[RSS]       Error: {e}")

    seen, unique = set(), []
    for a in results:
        if a["url_hash"] not in seen:
            seen.add(a["url_hash"])
            unique.append(a)

    saved = await save_articles(unique)
    print(f"[Ingestion] Done — {len(unique)} unique, {saved} new saved\n")

def start_scheduler():
    scheduler.add_job(ingest_all, "interval", minutes=15, id="news_ingest")
    scheduler.start()
    print("[Scheduler] Ingestion running every 15 min")
