from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict
from app.service import sentiment_service
from loguru import logger

router = APIRouter()

class SingleTextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=1024)

class BatchTextRequest(BaseModel):
    texts: List[str] = Field(..., min_items=1, max_items=100)

class SentimentResponse(BaseModel):
    label: str
    confidence: float

@router.post("/analyze", response_model=SentimentResponse)
async def analyze_sentiment(request: SingleTextRequest):
    """Analyze sentiment for a single text"""
    try:
        result = await sentiment_service.analyze(request.text)
        return result
    except Exception as e:
        logger.error(f"Error analyzing sentiment: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/batch_analyze", response_model=List[SentimentResponse])
async def batch_analyze_sentiment(request: BatchTextRequest):
    """Analyze sentiment for multiple texts"""
    try:
        results = await sentiment_service.batch_analyze(request.texts)
        return results
    except Exception as e:
        logger.error(f"Error in batch sentiment analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 