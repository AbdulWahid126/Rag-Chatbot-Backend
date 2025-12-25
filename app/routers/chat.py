from fastapi import APIRouter, HTTPException
from app.models import ChatRequest, ChatResponse
from app.rag_engine import RAGEngine
from app.database import save_conversation

router = APIRouter(tags=["chat"])

# Initialize RAG engine
rag_engine = RAGEngine()


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint for RAG queries
    
    Supports:
    - General questions about the book
    - Text selection-based queries
    - Module/chapter-specific questions
    """
    try:
        # Get response from RAG engine
        result = rag_engine.chat(
            query=request.query,
            selected_text=request.selected_text,
            module=request.module,
            chapter=request.chapter
        )
        
        # Save conversation to database
        conversation_id = save_conversation(
            query=request.query,
            response=result["response"],
            context=result["context"],
            module=request.module,
            chapter=request.chapter,
            selected_text=request.selected_text
        )
        
        return ChatResponse(
            response=result["response"],
            conversation_id=conversation_id,
            sources=result.get("sources", [])
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat request: {str(e)}"
        )


@router.get("/test")
async def test_chat():
    """Test endpoint to verify chat functionality"""
    try:
        result = rag_engine.chat(
            query="What is ROS 2?",
            module="module1"
        )
        return {
            "status": "success",
            "response_preview": result["response"][:200] + "...",
            "sources_count": len(result.get("sources", []))
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
