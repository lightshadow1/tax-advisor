from agno.knowledge.pdf import PDFKnowledgeBase, PDFReader
from agno.vectordb.pgvector import PgVector
from agno.embedder.openai import OpenAIEmbedder
# from agno.embedder.google import GeminiE
# mbedder
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("EMBEDDINGS_MODEL_APIKEY")
pdf_knowledge_base = PDFKnowledgeBase(
    path="downloaded_pdfs",
    # Table name: ai.pdf_documents
    vector_db=PgVector(
        table_name="pdf_documents",
        # table_name="gemini_embeddings",
        db_url=os.getenv("EMBEDDINGS_STORAGE"),
        # embedder=GeminiEmbedder(
        #     api_key=API_KEY, 
        #     task_type="RETRIEVAL_DOCUMENT",
        #     id="gemini-embedding-exp-03-07"),
        embedder=OpenAIEmbedder(id="nomic-embed-text",
                                dimensions=768,
                                base_url=os.getenv("EMBEDDINGS_MODEL_HOST"),
                                api_key=API_KEY)
    ),
    reader=PDFReader()
)

# pdf_knowledge_base.load(recreate=True)

# try gemini embedder
