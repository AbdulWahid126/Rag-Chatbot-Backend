import re
from typing import List


def chunk_markdown(content: str, chunk_size: int = 500, chunk_overlap: int = 50) -> List[str]:
    """
    Chunk markdown content into smaller pieces for embedding
    
    Args:
        content: Markdown content to chunk
        chunk_size: Target size of each chunk in characters
        chunk_overlap: Number of characters to overlap between chunks
    
    Returns:
        List of text chunks
    """
    # Remove frontmatter
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    
    # Split by headers first to maintain context
    sections = re.split(r'\n(#{1,6}\s+.*?)\n', content)
    
    chunks = []
    current_chunk = ""
    current_header = ""
    
    for i, section in enumerate(sections):
        # Check if this is a header
        if re.match(r'^#{1,6}\s+', section):
            current_header = section
            continue
        
        # Add header to chunk if we have one
        if current_header and not current_chunk:
            current_chunk = current_header + "\n\n"
        
        # Split section into sentences
        sentences = re.split(r'(?<=[.!?])\s+', section)
        
        for sentence in sentences:
            # If adding this sentence would exceed chunk_size, save current chunk
            if len(current_chunk) + len(sentence) > chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                
                # Start new chunk with overlap
                overlap_text = current_chunk[-chunk_overlap:] if len(current_chunk) > chunk_overlap else current_chunk
                current_chunk = overlap_text + " " + sentence
            else:
                current_chunk += " " + sentence
    
    # Add remaining chunk
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks


def clean_text(text: str) -> str:
    """Clean text by removing extra whitespace and special characters"""
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    # Remove code blocks for cleaner embedding
    text = re.sub(r'```[\s\S]*?```', '[CODE_BLOCK]', text)
    return text.strip()
