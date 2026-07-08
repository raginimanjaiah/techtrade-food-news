import ssl
import json
import httpx
from fastapi import APIRouter
from app.database import get_redis

router = APIRouter()

FOOD_STOCKS = {
    "UL":   "Unilever",
    "KO":   "Coca-Cola",
    "PEP":  "PepsiCo",
    "MCD":  "McDonald's",
    "MDLZ": "Mondelez",
    "GIS":  "General Mills",
    "K":    "Kellanova",
    "CAG":  "ConAgra",
    "CPB":  "Campbell's",
    "TSN":  "Tyson Foods",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
}

async def fetch_stock(symbol: str, name: str, client: httpx.AsyncClient):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        r   = await client.get(url, headers=HEADERS, timeout=5)
        r.raise_for_status()
        meta       = r.json()["chart"]["result"][0]["meta"]
        price      = float(meta.get("regularMarketPrice", 0))
        prev_close = float(meta.get("chartPreviousClose", 0) or meta.get("previousClose", 0))
        if not price or not prev_close:
            return None
        change     = round(price - prev_close, 2)
        change_pct = round((change / prev_close) * 100, 2)
        return {
            "symbol":     symbol,
            "name":       name,
            "price":      round(price, 2),
            "change":     change,
            "change_pct": change_pct,
            "up":         change >= 0,
        }
    except Exception as e:
        print(f"[Stocks] Error {symbol}: {e}")
        return None

@router.get("/stocks")
async def get_food_stocks():
    redis     = await get_redis()
    cache_key = "food_stocks"

    cached = await redis.get(cache_key)
    if cached:
        return json.loads(cached)

    import asyncio
    async with httpx.AsyncClient(verify=False) as client:
        tasks   = [fetch_stock(sym, name, client) for sym, name in FOOD_STOCKS.items()]
        results = await asyncio.gather(*tasks)

    stocks  = [r for r in results if r is not None]
    payload = {"stocks": stocks}

    if stocks:
        await redis.setex(cache_key, 300, json.dumps(payload))
    return payload
