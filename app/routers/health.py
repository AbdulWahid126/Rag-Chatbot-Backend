from fastapi import APIRouter
from app.models import HealthResponse
from app.config import settings
from datetime import datetime

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        environment=settings.ENVIRONMENT,
        timestamp=datetime.utcnow()
    )
