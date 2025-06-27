from agno.knowledge.pdf import PDFKnowledgeBase, PDFReader
from agno.vectordb.pgvector import PgVector
from agno.embedder.openai import OpenAIEmbedder
from dotenv import load_dotenv
import os


def parse_pdfs(reload=False):
    load_dotenv()

    API_KEY = os.getenv("EMBEDDINGS_MODEL_APIKEY")
    pdf_knowledge_base = PDFKnowledgeBase(
        path="downloaded_pdfs",
        # Table name: ai.pdf_documents
        vector_db=PgVector(
            table_name="pdf_documents",
            db_url=os.getenv("EMBEDDINGS_STORAGE"),
            embedder=OpenAIEmbedder(id="nomic-embed-text",
                                    dimensions=768,
                                    base_url=os.getenv("EMBEDDINGS_MODEL_HOST"),
                                    api_key=API_KEY)
        ),
        reader=PDFReader()
    )

    if reload:
        try:
            while True:
                # can comment after the first run
                pdf_knowledge_base.load(recreate=False)
                break
        except Exception as e:
            pass

if __name__ == "__main__":
    parse_pdfs(reload=True)
