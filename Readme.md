# Canada Tax Advisor

This project is intended to parse latest CRA docs and guides, parse it to a pgvector database, and use embedding models to store them. Then ask questions through LLM as a basic RAG model

## Requirements
- Create .env file with the following variables, you can get openai api key
```
EMBEDDINGS_MODEL_HOST=""
EMBEDDINGS_MODEL_APIKEY=""
EMBEDDINGS_STORAGE=""
OPENAI_API_KEY=""
```
- host a pgvector database in a separate docker-compose (outside the scope of this)

## Running the app
1. To host, use poetry virtual environment using poetry install.
2. Run crawler.py to start gathering the list of latest version (currently only find 2025 docs). This will create a list of pdf links from CRA and putting it in pdf_links.txt.
3. Run downloader.py to start downloading the pdf files and putting it under downloaded_pdfs.
4. Run pdf2embed.py to start parsing the pdf documents into a pgvector databases. I personally use a local ollama embedding model.
5. Run pdf_agent.py through streamlit by doing:
```
streamlit run pdf_agent.py
```
This should open local port localhost:8501 that give you the interface you need
