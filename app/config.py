from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # API Configuration (Using OpenAI SDK with Gemini)
    GEMINI_API_KEY: str
    GEMINI_BASE_URL: str = "https://generativelanguage.googleapis.com/v1beta/openai/"
    EMBEDDING_MODEL: str = "text-embedding-004"  # Gemini embedding model
    CHAT_MODEL: str = "gemini-1.0-pro"  # Use available model for OpenAI compatibility
    MAX_TOKENS: int = 500
    TEMPERATURE: float = 0.7
    
    # Qdrant Configuration
    QDRANT_URL: str
    QDRANT_API_KEY: str
    QDRANT_COLLECTION_NAME: str = "book_content"
    
    # Database Configuration
    DATABASE_URL: str
    
    # Application Configuration
    ENVIRONMENT: str = "development"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    CORS_ORIGINS: str = "http://localhost:3000"
    
    # RAG Configuration
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    TOP_K_RESULTS: int = 5
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convert comma-separated CORS origins to list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
