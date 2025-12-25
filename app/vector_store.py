from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from app.config import settings
import uuid
from typing import List, Dict, Optional


class VectorStore:
    """Qdrant vector database integration"""
    
    def __init__(self):
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY
        )
        self.collection_name = settings.QDRANT_COLLECTION_NAME
    
    def create_collection(self, vector_size: int = 1536):
        """Create collection for OpenAI embeddings"""
        try:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE
                )
            )
            print(f"[SUCCESS] Collection '{self.collection_name}' created successfully")
        except Exception as e:
            print(f"[WARNING] Collection might already exist: {e}")
    
    def upsert_chunks(self, chunks: List[str], embeddings: List[List[float]], metadata: List[Dict]):
        """Store text chunks with embeddings"""
        points = [
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "text": chunk,
                    "module": meta.get("module", ""),
                    "chapter": meta.get("chapter", ""),
                    "section": meta.get("section", ""),
                    "file_path": meta.get("file_path", "")
                }
            )
            for chunk, embedding, meta in zip(chunks, embeddings, metadata)
        ]
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        return len(points)
    
    def search(
        self,
        query_vector: List[float],
        limit: int = 5,
        module_filter: Optional[str] = None,
        chapter_filter: Optional[str] = None
    ):
        """Search for relevant chunks with optional filters"""
        search_filter = None

        # Build filters if provided
        if module_filter or chapter_filter:
            conditions = []
            if module_filter:
                conditions.append(
                    FieldCondition(key="module", match=MatchValue(value=module_filter))
                )
            if chapter_filter:
                conditions.append(
                    FieldCondition(key="chapter", match=MatchValue(value=chapter_filter))
                )
            search_filter = Filter(must=conditions)

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit,
            query_filter=search_filter
        )

        return results.points
    
    def collection_info(self):
        """Get collection information"""
        try:
            info = self.client.get_collection(self.collection_name)
            # Handle different Qdrant client versions
            vectors_count = getattr(info, 'vectors_count', getattr(info, 'indexed_vectors_count', 'unknown'))
            points_count = getattr(info, 'points_count', getattr(info, 'indexed_points_count', 'unknown'))
            return {
                "name": self.collection_name,
                "vectors_count": vectors_count,
                "points_count": points_count
            }
        except Exception as e:
            return {"error": str(e)}
