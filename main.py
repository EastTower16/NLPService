from fastapi import FastAPI, HTTPException
from loguru import logger
import uvicorn
from app.api import router
from app.service import SentimentService

# Configure logging
logger.add("logs/app.log", rotation="500 MB")

app = FastAPI(
    title="Text Sentiment Analysis Service",
    description="A service for analyzing sentiment in Chinese and English text",
    version="1.0.0"
)

# Initialize sentiment service
sentiment_service = SentimentService()

# Include API router
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    """Initialize models on startup"""
    try:
        await sentiment_service.initialize()
        logger.info("Service initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize service: {str(e)}")
        raise

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        workers=4,
        reload=True
    ) 