from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.routers import feed
from app.workers.ingestion_worker import start_scheduler, ingest_all
from app.database import close_pool
from app.models import HealthResponse

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await ingest_all()
    start_scheduler()
    yield
    await close_pool()

app = FastAPI(
    title="TechTrade.Food API",
    version="1.0.0",
    description="Food industry news and exhibition platform API",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(feed.router, prefix="/api", tags=["Feed"])

@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health():
    return HealthResponse(status="ok", service="techtrade-food-api", version="1.0.0")
