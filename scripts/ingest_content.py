#!/usr/bin/env python3
"""
Content Ingestion Script
Reads all MDX files from the docs directory and ingests them into Qdrant
"""

import os
import sys
import glob
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from openai import OpenAI
from app.vector_store import VectorStore
from app.utils.chunking import chunk_markdown, clean_text
from app.config import settings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure OpenAI client for Gemini
client = OpenAI(
    api_key=settings.GEMINI_API_KEY,
    base_url=settings.GEMINI_BASE_URL
)


def extract_metadata_from_path(file_path: str) -> dict:
    """Extract module and chapter information from file path"""
    parts = Path(file_path).parts
    
    # Find module (e.g., module1, module2)
    module = ""
    for part in parts:
        if part.startswith("module"):
            module = part
            break
    
    # Get chapter name from filename
    chapter = Path(file_path).stem
    
    return {
        "module": module if module else "intro",
        "chapter": chapter,
        "file_path": str(file_path)
    }


def ingest_book_content():
    """Read all MDX files and ingest into Qdrant"""
    print("[INFO] Starting content ingestion...")

    # Initialize vector store
    vector_store = VectorStore()

    # Create collection
    print("[INFO] Creating Qdrant collection...")
    vector_store.create_collection(vector_size=1536)  # Gemini text-embedding-004 size


    # Find all MDX files
    docs_path = Path(__file__).parent.parent.parent / "docs"
    mdx_files = list(docs_path.glob("**/*.mdx"))

    print(f"[INFO] Found {len(mdx_files)} MDX files")

    total_chunks = 0

    for file_path in mdx_files:
        print(f"\n[INFO] Processing: {file_path.name}")

        try:
            # Read file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract metadata
            metadata_base = extract_metadata_from_path(str(file_path))

            # Chunk content
            chunks = chunk_markdown(content, chunk_size=settings.CHUNK_SIZE)
            print(f"   [INFO] Created {len(chunks)} chunks")

            if not chunks:
                print(f"   [WARNING] No chunks created, skipping")
                continue

            # Generate embeddings using OpenAI SDK (Gemini endpoint)
            print(f"   [INFO] Generating embeddings...")
            embeddings = []

            for chunk in chunks:
                cleaned_chunk = clean_text(chunk)
                response = client.embeddings.create(
                    model=settings.EMBEDDING_MODEL,
                    input=cleaned_chunk
                )
                embeddings.append(response.data[0].embedding)

            # Create metadata for each chunk
            metadata = [metadata_base.copy() for _ in chunks]

            # Upsert to Qdrant
            print(f"   [INFO] Uploading to Qdrant...")
            count = vector_store.upsert_chunks(chunks, embeddings, metadata)
            total_chunks += count

            print(f"   [SUCCESS] Successfully ingested {count} chunks")

        except Exception as e:
            print(f"   [ERROR] Error processing {file_path.name}: {e}")
            continue

    print(f"\n[SUCCESS] Ingestion complete!")
    print(f"[INFO] Total chunks ingested: {total_chunks}")

    # Show collection info
    info = vector_store.collection_info()
    print(f"[INFO] Collection info: {info}")


if __name__ == "__main__":
    ingest_book_content()
