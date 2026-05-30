import httpx
import feedparser
import hashlib
from datetime import datetime
from typing import List, Dict

FOOD_QUERY = "food industry OR food technology OR food safety OR food regulation OR FMCG"

RSS_FEEDS = [
    "https://www.foodnavigator.com/rss/feed",
    "https://www.fooddive.com/feeds/news/",
    "https://www.ift.org/rss/all-news",
    "https://www.just-food.com/feed/",
]

def make_hash(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()

async def fetch_newsdata(api_key: str) -> List[Dict]:
    if not api_key or api_key == "your_newsdata_key_here":
        print("[NewsData] No API key — skipping")
        return []
    async with httpx.AsyncClient() as client:
        r = await client.get(
            "https://newsdata.io/api/1/news",
            params={
                "apikey": api_key,
                "q": FOOD_QUERY,
                "language": "en",
                "category": "food,business,technology",
            },
            timeout=10,
        )
        r.raise_for_status()
        return [_norm_newsdata(a) for a in r.json().get("results", []) if a.get("link")]

async def fetch_gnews(api_key: str) -> List[Dict]:
    if not api_key or api_key == "your_gnews_key_here":
        print("[GNews] No API key — skipping")
        return []
    async with httpx.AsyncClient() as client:
        r = await client.get(
            "https://gnews.io/api/v4/search",
            params={"q": "food industry", "lang": "en", "max": 10, "token": api_key},
            timeout=10,
        )
        r.raise_for_status()
        return [_norm_gnews(a) for a in r.json().get("articles", []) if a.get("url")]

def fetch_rss_feeds() -> List[Dict]:
    articles = []
    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:10]:
                url = entry.get("link", "")
                if not url:
                    continue
                articles.append({
                    "title":        entry.get("title", "No title"),
                    "summary":      entry.get("summary", ""),
                    "url":          url,
                    "url_hash":     make_hash(url),
                    "image_url":    None,
                    "source":       feed.feed.get("title", "RSS"),
                    "category":     "industry",
                    "is_breaking":  False,
                    "published_at": _parse_date(entry.get("published") or entry.get("updated")),
                })
        except Exception as e:
            print(f"[RSS] Error {feed_url}: {e}")
    return articles

def _norm_newsdata(a: dict) -> dict:
    return {
        "title":        a.get("title", ""),
        "summary":      a.get("description", "") or "",
        "url":          a.get("link", ""),
        "url_hash":     make_hash(a.get("link", "")),
        "image_url":    a.get("image_url"),
        "source":       a.get("source_id", "Unknown"),
        "category":     _map_category(a.get("category", [])),
        "is_breaking":  False,
        "published_at": _parse_date(a.get("pubDate")),
    }

def _norm_gnews(a: dict) -> dict:
    return {
        "title":        a.get("title", ""),
        "summary":      a.get("description", "") or "",
        "url":          a.get("url", ""),
        "url_hash":     make_hash(a.get("url", "")),
        "image_url":    a.get("image"),
        "source":       a.get("source", {}).get("name", "Unknown"),
        "category":     "industry",
        "is_breaking":  False,
        "published_at": _parse_date(a.get("publishedAt")),
    }

def _map_category(cats: list) -> str:
    s = " ".join(cats).lower() if cats else ""
    if "food" in s:       return "industry"
    if "business" in s:   return "market_news"
    if "technology" in s: return "technology"
    if "health" in s:     return "regulatory"
    return "industry"

def _parse_date(date_str) -> datetime:
    if not date_str:
        return datetime.utcnow()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%SZ",
                "%a, %d %b %Y %H:%M:%S %z", "%Y-%m-%dT%H:%M:%S%z"):
        try:
            return datetime.strptime(str(date_str)[:25], fmt)
        except Exception:
            continue
    return datetime.utcnow()
