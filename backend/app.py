from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import sys

from .config import settings
from .api.endpoints import router
from .services.usda_service import usda_service
from .services.gemini_service import gemini_service

# Configure logging
logger.remove()
logger.add(
    sys.stdout,
    level=settings.LOG_LEVEL,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info("Starting up Nutrition Tracker API...")
    if settings.USDA_API_KEY:
        logger.info("USDA API key configured - real nutrition data available")
    else:
        logger.warning("USDA API key not configured - using fallback nutrition data")
    if settings.GEMINI_API_KEY:
        logger.info("Gemini API key configured - AI chat assistant available")
    else:
        logger.warning("Gemini API key not configured - chat assistant disabled")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown."""
    logger.info("Shutting down Nutrition Tracker API...")
    await usda_service.close_session()
    await gemini_service.close_session()
    logger.info("All service sessions closed")

# Include API router
app.include_router(router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "name": settings.PROJECT_NAME,
        "version": "1.0.0",
        "model_type": settings.MODEL_TYPE,
        "usda_api_enabled": bool(settings.USDA_API_KEY)
    }

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting {settings.PROJECT_NAME} on {settings.HOST}:{settings.PORT}")
    uvicorn.run(
        "app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
