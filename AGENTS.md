# AGENT.md

## Project Overview

This is a **Canada Tax Advisor** application that provides AI-powered tax consultation services for Canadian residents. It uses Retrieval-Augmented Generation (RAG) to parse Canada Revenue Agency (CRA) documents, store them as vector embeddings, and provide intelligent answers to tax-related questions through customizable AI personas.

## Tech Stack

### Backend (Python)
- **Python 3.12+** with uv for dependency management
- **agno** - AI agent framework for RAG
- **OpenAI API** - GPT-4o-mini for LLM capabilities
- **Google Genai** - Gemini API support
- **PyPDF** - PDF parsing
- **PostgreSQL + pgvector** OR **JSON file** - Vector database for embeddings
- **Streamlit** - Chat interface UI
- **Flask** - Backend API

### Frontend
- **React 19** with TypeScript
- **Tailwind CSS** - Styling
- **Create React App** - Build tooling

### External Services
- **Ollama** - Local LLM/embedding model hosting (nomic-embed-text)
- **OpenAI API** - GPT models and embeddings
- **Google Gemini API** - Alternative LLM

## Directory Structure

```
/cra-doc-scraper/
├── crawler.py          # Web scraper for CRA PDF links
├── downloader.py       # PDF file downloader
├── pdf2embed.py        # PDF parser & embedding generator
├── pdf_agent.py        # Streamlit chat interface (main app)
├── persona.py          # AI persona definitions
├── pyproject.toml      # Python dependencies (uv)
├── .env                # Environment variables
│
├── backend_api/
│   └── app.py          # Flask API for tax form submission
│
├── tax-frontend/       # React frontend application
│   ├── src/
│   │   ├── App.tsx     # Main React component
│   │   └── index.tsx   # Entry point
│   ├── package.json
│   └── tailwind.config.js
│
├── downloaded_pdfs/    # CRA documents (PDFs and HTML)
└── app.tsx             # Alternative React component (root level)
```

## Architecture

```
Frontend (React)          Backend API (Flask)         Streamlit UI
localhost:3000       -->  localhost:5000         -->  localhost:8501
                              |                           |
                              v                           v
                         Gemini API               Agno Agent (RAG)
                                                        |
                                                        v
                                              PostgreSQL + pgvector
                                              (Vector embeddings)
```

## Development Setup

### Prerequisites
- Python 3.12+
- Node.js 18+
- PostgreSQL with pgvector extension (optional - can use JSON instead)
- uv (Python dependency manager)

### Environment Variables
Create a `.env` file with:

**For PostgreSQL (recommended for production):**
```
EMBEDDINGS_MODEL_HOST=<ollama host>
EMBEDDINGS_MODEL_APIKEY=<api key>
EMBEDDINGS_STORAGE=postgresql+psycopg://<connection string>
OPENAI_API_KEY=<openai api key>
GOOGLE_API_KEY=<google api key>
OLLAMA_MODEL=<model name>
```

**For JSON file storage (simpler setup, good for development):**
```
EMBEDDINGS_MODEL_HOST=<ollama host>
EMBEDDINGS_MODEL_APIKEY=<api key>
OPENAI_API_KEY=<openai api key>
GOOGLE_API_KEY=<google api key>
OLLAMA_MODEL=<model name>
```
Note: Omit `EMBEDDINGS_STORAGE` to use JSON file storage by default.

### Installation

**Python Backend:**
```bash
uv sync
```

**Frontend:**
```bash
cd tax-frontend
npm install
```

## Running the Application

### Data Pipeline (One-time setup)
```bash
# 1. Crawl CRA website for PDF links
uv run python crawler.py

# 2. Download PDFs
uv run python downloader.py

# 3. Generate embeddings and store in vector DB
uv run python pdf2embed.py
```

### Running Services

**Streamlit Chat UI:**
```bash
uv run streamlit run pdf_agent.py
# Available at localhost:8501
```

**Flask Backend API:**
```bash
uv run python backend_api/app.py
# Available at localhost:5000
```

**React Frontend:**
```bash
cd tax-frontend
npm start
# Available at localhost:3000
```

## Key Files

| File | Purpose |
|------|---------|
| `pdf_agent.py` | Main Streamlit app with RAG agent and persona selection |
| `persona.py` | Four AI personas: G.A.B.E, The Beaver, Maple, Section 245 |
| `pdf2embed.py` | PDF processing and embedding generation |
| `crawler.py` | CRA website scraping for document links |
| `backend_api/app.py` | Flask API with Gemini integration |
| `tax-frontend/src/App.tsx` | React tax form interface |

## Testing

**Frontend tests:**
```bash
cd tax-frontend
npm test
```

## Common Tasks

### Adding New Documents
1. Add PDF URLs to `pdf_links.txt`
2. Run `uv run python downloader.py`
3. Run `uv run python pdf2embed.py` to generate embeddings

### Adding a New Persona
Edit `persona.py` and add a new persona dictionary with:
- `name`: Display name
- `description`: Short description
- `instructions`: System prompt for the AI

### Modifying the Knowledge Base
The knowledge base uses pgvector with 768-dimensional embeddings (nomic-embed-text). Configuration is in `pdf2embed.py`.

## Code Style

- Python: Follow PEP 8
- TypeScript/React: Standard React conventions with TypeScript strict mode
- Use meaningful variable names and add comments for complex logic

## API Endpoints

### Flask Backend (`backend_api/app.py`)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/save_progress` | POST | Save form progress |
| `/submit_form` | POST | Submit tax form and get AI advice |

## Vector Storage Options

### Option 1: PostgreSQL + pgvector (Recommended for Production)
- **Pros**: Scalable, persistent, supports concurrent access
- **Cons**: Requires PostgreSQL setup
- **Configuration**: Set `EMBEDDINGS_STORAGE=postgresql+psycopg://<connection string>` in `.env`
- Table: `pdf_documents` (managed by agno)
- Embedding dimensions: 768
- Model: nomic-embed-text (via Ollama)

### Option 2: JSON File Storage (Simple Development Setup)
- **Pros**: No database setup required, easy to start
- **Cons**: Not suitable for production, slower for large datasets
- **Configuration**: Omit `EMBEDDINGS_STORAGE` from `.env` or set to empty
- File location: `tmp/json_vector_db/` (auto-created)
- Embedding dimensions: 768
- Model: nomic-embed-text (via Ollama)

**To switch between storage types:**
1. Update your `.env` file (add/remove `EMBEDDINGS_STORAGE`)
2. Re-run `uv run python pdf2embed.py` to regenerate embeddings

## Platform Support

### Windows
All commands work on Windows with the following considerations:

**Installation:**
- Install uv: `pip install uv` or download from [astral.sh/uv](https://astral.sh/uv)
- Install Ollama: Download Windows version from [ollama.com/download](https://ollama.com/download)
- Install PostgreSQL (if using): Download from [postgresql.org](https://www.postgresql.org/download/windows/)

**Shell compatibility:**
- All `uv run` commands work in PowerShell, Command Prompt, and Git Bash
- Path separators: Use `\` (backslash) or `/` (forward slash) interchangeably
- Example: `downloaded_pdfs\file.pdf` or `downloaded_pdfs/file.pdf`

**JSON storage recommendation:**
- On Windows, JSON file storage is recommended for development to avoid PostgreSQL setup complexity
- Simply omit `EMBEDDINGS_STORAGE` from your `.env` file

### macOS/Linux
All commands work natively. Install uv via:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Troubleshooting

- **Streamlit not loading**: Ensure `.env` file exists with valid credentials
- **Embedding errors**: Verify Ollama is running and model is available
- **Database connection issues**: Check PostgreSQL is accessible and pgvector extension is installed, or switch to JSON storage for simpler setup
- **Slow queries with JSON storage**: Consider migrating to PostgreSQL for better performance
- **Windows path issues**: Use forward slashes `/` in paths or escape backslashes `\\`
- **Windows firewall**: Allow Python/Streamlit/Flask through firewall for localhost access
