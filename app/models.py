from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    query: str
    selected_text: Optional[str] = None
    conversation_id: Optional[str] = None
    module: Optional[str] = None
    chapter: Optional[str] = None


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    response: str
    conversation_id: str
    sources: Optional[List[dict]] = None


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    environment: str
    timestamp: datetime
