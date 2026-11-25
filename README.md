
# AI Study Assistant

An AI-powered study assistant that helps students understand, search, and summarize PDF documents. It combines Retrieval-Augmented Generation (RAG), semantic search, hybrid retrieval, and Large Language Models (LLMs) to provide useful answers with document-based citations.

## 1. Project Overview

The AI Study Assistant allows users to:

- Upload PDF documents.
- Extract and process PDF content.
- Ask questions about uploaded documents.
- Receive answers grounded in document content.
- View source citations, including page information.
- Generate simple-English PDF summaries.
- Ask general knowledge questions.
- Search the web for current information.

The application uses a custom RAG pipeline and LangGraph to manage different types of user questions.

## 2. Key Features

### PDF Processing

- Extract text from PDF documents using PyMuPDF.
- Divide extracted content into smaller chunks.
- Maintain document and page metadata.
- Store processed document information.

### Intelligent Retrieval

- Generate embeddings using BAAI/bge-m3.
- Perform semantic search using Qdrant.
- Perform keyword-based search using BM25.
- Combine retrieval results using Reciprocal Rank Fusion (RRF).
- Improve search relevance using a CrossEncoder reranker.

### AI-Powered Answers

- Use Groq LLM for answer generation.
- Answer document-related questions using retrieved context.
- Include source citations in document-based answers.
- Support general questions and web searches.

### Document Summarization

- Generate simple-English PDF summaries.
- Support map-reduce summarization for longer text.

### API

- Build REST APIs using FastAPI.
- Access interactive API documentation through Swagger UI.
- Handle document uploads, listing, chat, and summarization.

## 3. Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python 3.11 |
| Backend Framework | FastAPI |
| AI Workflow | LangGraph |
| LLM Provider | Groq |
| Embedding Model | BAAI/bge-m3 |
| Vector Database | Qdrant |
| Keyword Retrieval | BM25 |
| Hybrid Retrieval | Reciprocal Rank Fusion |
| Reranking | CrossEncoder |
| Database | MongoDB |
| Cache | Redis |
| PDF Processing | PyMuPDF |
| Web Search | DuckDuckGo Search |
| Testing | Pytest |
| Code Quality | Ruff |
| Containerization | Docker Compose |

## 4. System Architecture

The application follows this workflow:

1. The user sends a request through the FastAPI backend.
2. LangGraph receives the request.
3. The Intent Classifier identifies the type of request.
4. LangGraph routes the request to the appropriate workflow.
5. Document questions are processed through the custom RAG pipeline.
6. Hybrid retrieval combines semantic and keyword search results.
7. Reciprocal Rank Fusion combines the retrieval results.
8. The CrossEncoder reranks the retrieved chunks.
9. The Context Builder prepares relevant information.
10. Groq generates the final answer.
11. The application returns the answer and available citations.

### Architecture Diagram

```text
                    USER
                      |
                      v
                FASTAPI BACKEND
                      |
                      v
               LANGGRAPH WORKFLOW
                      |
                      v
                INTENT CLASSIFIER
                      |
          +-----------+-----------+
          |           |           |
          v           v           v
       DOCUMENT    SUMMARY     GENERAL /
       QUESTION    REQUEST     WEB SEARCH
          |           |           |
          v           v           v
       CUSTOM RAG   SUMMARY     GROQ LLM /
       PIPELINE     SERVICE     WEB SEARCH
          |
          v
     HYBRID RETRIEVAL
          |
      +---+---+
      |       |
      v       v
   SEMANTIC   BM25
    SEARCH   SEARCH
      |       |
      +---+---+
          |
          v
      RRF FUSION
          |
          v
       RERANKING
          |
          v
    CONTEXT BUILDER
          |
          v
       GROQ LLM
          |
          v
    ANSWER + CITATIONS
```

## 5. Project Structure

```text
AI_Study_Assistant/
│
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── chat.py
│   │       └── documents.py
│   │
│   ├── core/
│   │   └── config.py
│   │
│   ├── ingestion/
│   │   ├── pdf_extractor.py
│   │   ├── text_chunker.py
│   │   └── metadata_processor.py
│   │
│   ├── orchestration/
│   │   ├── graph.py
│   │   ├── intent_classifier.py
│   │   └── state.py
│   │
│   ├── rag/
│   │   ├── retrieval/
│   │   │   ├── bm25_retriever.py
│   │   │   ├── semantic_retriever.py
│   │   │   └── hybrid_retriever.py
│   │   │
│   │   ├── reranking/
│   │   │   └── reranker_service.py
│   │   │
│   │   ├── context_builder.py
│   │   └── rag_pipeline.py
│   │
│   ├── services/
│   │   ├── document_service.py
│   │   ├── embedding_service.py
│   │   ├── llm_service.py
│   │   ├── map_reduce_summary.py
│   │   ├── mongodb_service.py
│   │   ├── qdrant_service.py
│   │   ├── redis_service.py
│   │   ├── summary_service.py
│   │   └── web_search_service.py
│   │
│   └── main.py
│
├── tests/
│   ├── unit/
│   └── integration/
│
├── uploads/
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 6. Installation and Setup

### Prerequisites

Install the following software:

- Python 3.11
- Git
- Docker Desktop
- Visual Studio Code (recommended)

### Step 1: Clone the Repository

Replace the placeholder with your actual GitHub repository URL.

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd AI_Study_Assistant
```

### Step 2: Create a Virtual Environment

```bash
py -3.11 -m venv .venv
```

### Step 3: Activate the Virtual Environment

For Windows PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### Step 4: Install Dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Step 5: Configure Environment Variables

Create a `.env` file in the project root using `.env.example` as a reference.

Configure the required values, including:

- Groq API key.
- Qdrant connection URL.
- MongoDB connection URL.
- Redis connection settings.
- Embedding model configuration.

Never upload your `.env` file or expose API keys publicly.

### Step 6: Start Database Services

Make sure Docker Desktop is running.

Execute:

```bash
docker compose up -d
```

This starts the configured services:

- Qdrant
- MongoDB
- Redis

## 7. Run the Application

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

The application will be available at:

http://127.0.0.1:8000

### API Documentation

FastAPI provides interactive API documentation through Swagger UI.

Open:

http://127.0.0.1:8000/docs

## 8. Available API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Application home |
| GET | `/health` | Health endpoint |
| POST | `/api/v1/documents` | Upload a PDF document |
| GET | `/api/v1/documents` | List uploaded documents |
| POST | `/api/v1/chat` | Ask questions |
| POST | `/api/v1/documents/{document_id}/summary` | Summarize a document |

## 9. Testing

The project uses Pytest for unit and integration testing.

### Run All Tests

```bash
python -m pytest tests/ -v
```

### Run Unit Tests

```bash
python -m pytest tests/unit/ -v
```

### Run Integration Tests

```bash
python -m pytest tests/integration/ -v
```

### Check Code Quality

Run Ruff:

```bash
python -m ruff check app tests
```

## 10. Current Project Status

The following functionality has been implemented and tested:

- PDF extraction and text chunking.
- Document metadata processing.
- BAAI/bge-m3 embedding generation.
- Qdrant vector storage.
- BM25 keyword retrieval.
- Semantic retrieval.
- Hybrid retrieval with RRF.
- CrossEncoder reranking.
- Custom RAG pipeline.
- LangGraph intent classification and routing.
- Groq-based answer generation.
- PDF summarization.
- Web search integration.
- MongoDB and Redis service connections.
- FastAPI endpoints.
- Unit and integration tests.

### Testing Results

- Unit tests: 18 passed.
- Integration tests: 3 passed.
- Total: 21 passed.

### Code Quality

Ruff checks passed successfully.

## 11. Future Improvements

Potential improvements include:

- User authentication and authorization.
- Conversation history management.
- Persistent BM25 indexing.
- More advanced PDF structure extraction.
- Improved document validation and upload security.
- Better monitoring and logging.
- Frontend application for an improved user experience.
- Expanded integration and end-to-end testing.

## 12. Author

**Mohammed Ajmal K.**

- GitHub: [mohammedajmalkondambath-ux](https://github.com/mohammedajmalkondambath-ux)
- LinkedIn: [Mohammed Ajmal K.](https://linkedin.com/in/mohammed-ajmal-kondambath)

---

**AI Study Assistant — Making document-based learning smarter with Artificial Intelligence.**
