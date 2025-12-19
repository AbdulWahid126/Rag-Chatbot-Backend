from sqlalchemy import create_engine, Column, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from datetime import datetime
import uuid

# Create engine - explicitly use psycopg driver
# Convert postgresql:// to postgresql+psycopg:// if needed
database_url = settings.DATABASE_URL
if database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)

engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Conversation(Base):
    """Conversation model for storing chat history"""
    __tablename__ = "conversations"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    query = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    context = Column(Text)
    module = Column(String)
    chapter = Column(String)
    selected_text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def save_conversation(
    query: str,
    response: str,
    context: str = None,
    module: str = None,
    chapter: str = None,
    selected_text: str = None
) -> str:
    """Save conversation to database"""
    db = SessionLocal()
    try:
        conversation = Conversation(
            query=query,
            response=response,
            context=context,
            module=module,
            chapter=chapter,
            selected_text=selected_text
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation.id
    finally:
        db.close()
