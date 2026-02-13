# Canada Tax Advisor

An AI-powered tax consultation application for Canadian residents that uses Retrieval-Augmented Generation (RAG) to parse Canada Revenue Agency (CRA) documents and provide intelligent answers through customizable AI personas.

## Prerequisites
- Python 3.12+
- Node.js 18+ (for React frontend)
- uv (Python dependency manager)
- PostgreSQL with pgvector extension (optional - can use JSON file storage for development)
- Ollama (for local embedding models)

## Environment Setup

Create a `.env` file in the root directory:

**For PostgreSQL storage (recommended for production):**
```
EMBEDDINGS_MODEL_HOST=<ollama host>
EMBEDDINGS_MODEL_APIKEY=<api key>
EMBEDDINGS_STORAGE=postgresql+psycopg://<connection string>
OPENAI_API_KEY=<openai api key>
GOOGLE_API_KEY=<google api key>
OLLAMA_MODEL=<model name>
```

**For JSON file storage (simpler development setup):**
```
EMBEDDINGS_MODEL_HOST=<ollama host>
EMBEDDINGS_MODEL_APIKEY=<api key>
OPENAI_API_KEY=<openai api key>
GOOGLE_API_KEY=<google api key>
OLLAMA_MODEL=<model name>
```
*Note: Omit `EMBEDDINGS_STORAGE` to use JSON file storage by default.*

## Installation

```bash
# Install Python dependencies
uv sync

# Install frontend dependencies (optional)
cd tax-frontend
npm install
```

### Windows-Specific Notes
- **uv installation**: Install via `pip install uv` or download from [astral.sh/uv](https://astral.sh/uv)
- **Ollama**: Download Windows version from [ollama.com/download](https://ollama.com/download)
- **Path separators**: Use backslashes `\` or forward slashes `/` in file paths
- **PowerShell**: All commands work in PowerShell, Command Prompt, or Git Bash

## Running the Application

### 1. Data Pipeline (One-time Setup)

```bash
# Crawl CRA website for PDF links (creates pdf_links.txt)
uv run python crawler.py

# Download PDFs to downloaded_pdfs/
uv run python downloader.py

# Generate embeddings and store in vector database
uv run python pdf2embed.py
```

### 2. Start the Streamlit Chat UI

```bash
uv run streamlit run pdf_agent.py
```
Access at `http://localhost:8501`

### 3. Start the Flask Backend API (Optional)

```bash
uv run python backend_api/app.py
```
Access at `http://localhost:5000`

### 4. Start the React Frontend (Optional)

```bash
cd tax-frontend
npm start
```
Access at `http://localhost:3000`

## Features

- **Multiple AI Personas**: Choose from G.A.B.E, The Beaver, Maple, or Section 245
- **RAG-based Answers**: Retrieves relevant CRA documents to provide accurate tax advice
- **Vector Storage Options**: Use PostgreSQL + pgvector for production or JSON files for development
- **Web Interface**: Streamlit chat UI for easy interaction
- **API Backend**: Flask API with Gemini integration
- **React Frontend**: Modern tax form interface

## Vector Storage

- **PostgreSQL + pgvector**: Scalable, supports concurrent access (recommended for production)
- **JSON File Storage**: No database setup required (good for development)

To switch between storage types:
1. Update your `.env` file (add/remove `EMBEDDINGS_STORAGE`)
2. Re-run `uv run python pdf2embed.py`

## Tech Stack

- **Backend**: Python 3.12+, agno, OpenAI API, Google Gemini, Streamlit, Flask
- **Frontend**: React 19, TypeScript, Tailwind CSS
- **Vector DB**: PostgreSQL + pgvector OR JSON file storage
- **Embeddings**: Ollama (nomic-embed-text)

## Documentation

For detailed setup and development instructions, see [AGENTS.md](./AGENTS.md).
