from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat, health
from app.config import settings

# Create FastAPI app
app = FastAPI(
    title="Physical AI & Humanoid Robotics - RAG API",
    description="Retrieval-Augmented Generation API for the Physical AI textbook",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(chat.router, prefix="/api/chat")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Physical AI & Humanoid Robotics RAG API",
        "version": "1.0.0",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True
    )
