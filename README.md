# Physical AI & Humanoid Robotics - RAG Backend

Backend API for the Retrieval-Augmented Generation (RAG) chatbot.

## 🏗️ Architecture

- **FastAPI**: Web framework
- **OpenAI**: Embeddings and chat completion
- **Qdrant**: Vector database (free tier)
- **Neon Postgres**: Conversation storage (free tier)

## 📋 Setup Instructions

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

Required variables:
- `OPENAI_API_KEY`: Your OpenAI API key
- `QDRANT_URL`: Your Qdrant cluster URL
- `QDRANT_API_KEY`: Your Qdrant API key
- `DATABASE_URL`: Your Neon Postgres connection string

### 3. Initialize Database

```bash
python scripts/init_db.py
```

### 4. Ingest Book Content

```bash
python scripts/ingest_content.py
```

This will:
- Read all MDX files from `../docs/`
- Chunk the content
- Generate embeddings
- Upload to Qdrant

### 5. Run the API

```bash
# Development mode
uvicorn app.main:app --reload

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📡 API Endpoints

### Health Check
```
GET /health
```

### Chat
```
POST /api/chat
{
  "query": "What is ROS 2?",
  "selected_text": "optional selected text",
  "module": "module1",
  "chapter": "ros2-fundamentals"
}
```

### API Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🧪 Testing

Test the chat endpoint:
```
GET /api/chat/test
```

## 🚀 Deployment

### Railway (Recommended)

1. Connect GitHub repository
2. Add environment variables:
   - `GEMINI_API_KEY`: Your Gemini API key
   - `QDRANT_URL`: Your Qdrant cluster URL (format: https://your-cluster-id.europe-west3-0.gcp.cloud.qdrant.io:6333)
   - `QDRANT_API_KEY`: Your Qdrant API key
   - `DATABASE_URL`: Your Neon Postgres connection string
3. Deploy

### Manual Deployment

For production deployment, make sure to update the QDRANT_URL in your environment variables to match your Qdrant Cloud instance. The URL should include the proper port (6333) and use HTTPS.

Example format: `https://your-cluster-id.europe-west3-0.gcp.cloud.qdrant.io:6333`

⚠️ **Important**: Before deploying, ensure you have ingested your content by running:

```bash
python scripts/ingest_content.py
```

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── config.py            # Settings
│   ├── models.py            # Pydantic models
│   ├── database.py          # Neon Postgres
│   ├── vector_store.py      # Qdrant integration
│   ├── rag_engine.py        # RAG logic
│   ├── routers/
│   │   ├── chat.py          # Chat endpoints
│   │   └── health.py        # Health check
│   └── utils/
│       └── chunking.py      # Text processing
├── scripts/
│   ├── ingest_content.py    # Content ingestion
│   └── init_db.py           # DB initialization
├── requirements.txt
└── .env.example
```

## 🔑 Environment Variables

See `.env.example` for all required variables.

## 📝 License

MIT
