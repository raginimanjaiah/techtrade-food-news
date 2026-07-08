"""
Run once to classify all existing articles into food segments.
Usage: cd backend && source venv/bin/activate && python scripts/backfill_segments.py
"""
import asyncio
from dotenv import load_dotenv
load_dotenv()

from app.services.article_repo_v2 import backfill_segments

async def main():
    print("Starting segment backfill...")
    updated = await backfill_segments()
    print(f"Done — {updated} articles classified")

if __name__ == "__main__":
    asyncio.run(main())
