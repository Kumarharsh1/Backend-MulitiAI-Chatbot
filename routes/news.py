from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.news_service import news_service

router = APIRouter()

class NewsRequest(BaseModel):
    category: str = "general"
    country: str = "us"
    query: str = None

@router.get("/news")
async def get_news(category: str = "general", country: str = "us"):
    """Get news articles"""
    try:
        result = await news_service.get_news(category, country)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"News fetch error: {str(e)}")

@router.get("/news/search")
async def search_news(query: str):
    """Search news articles"""
    try:
        if not query or len(query) < 3:
            raise HTTPException(status_code=400, detail="Query must be at least 3 characters")
        
        result = await news_service.search_news(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"News search error: {str(e)}")