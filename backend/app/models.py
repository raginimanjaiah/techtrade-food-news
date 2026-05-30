from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Article(BaseModel):
    id:           str
    title:        str
    summary:      Optional[str] = None
    url:          str
    image_url:    Optional[str] = None
    source:       Optional[str] = None
    category:     Optional[str] = None
    is_breaking:  bool = False
    published_at: Optional[datetime] = None

class FeedResponse(BaseModel):
    articles: List[Article]
    page:     int
    limit:    int
    total:    int

class HealthResponse(BaseModel):
    status:  str
    service: str
    version: str
