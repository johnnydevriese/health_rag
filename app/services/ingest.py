from typing import Any, Dict
import logfire
import chromadb
import voyageai
from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.core.schema import Document

from .semantic_chunking import SemanticChunker
from ..core.config import settings


class IngestService:
    """Service for ingesting documents into the vector database using semantic chunking."""

    def __init__(self):
        """Initialize the service."""
        self.voyage_client = voyageai.Client(api_key=settings.VOYAGE_API_KEY)
        self.chroma_client = chromadb.PersistentClient(path=settings.VECTOR_DB_PATH)
        self.semantic_chunker = SemanticChunker()
        self.markdown_path = "app/gen-ai-homework-assignment/input/medicare_comparison.md"

    def ingest_medicare_docs(self) -> Dict[str, Any]:
        """
        Ingest medicare docs into the vector database.

        Returns:
            Dict with ingestion status and details
        """
        with logfire.span("ingestion_pipeline"):
            # Read the markdown file
            try:
                with open(self.markdown_path, "r") as f:
                    markdown_doc = f.read()
            except FileNotFoundError:
                raise FileNotFoundError(
                    f"Markdown file not found at: {self.markdown_path}"
                )

            # Perform Semantic Chunking
            with logfire.span("performing_semantic_chunking"):
                chunks = self.semantic_chunker.chunk(markdown_doc)

            # Prepare text, metadata, and ids
            ids = [f"doc_{i}" for i in range(len(chunks))]
            metadatas = [{"source": "medicare_comparison.md", "chunk_index": i} for i in range(len(chunks))]

            # Generate embeddings with VoyageAI
            with logfire.span("generating_embeddings"):
                try:
                    embeddings_response = self.voyage_client.embed(
                        texts=chunks,
                        model="voyage-3",
                        input_type="document",
                    )
                    embeddings = embeddings_response.embeddings
                except Exception as e:
                    raise ValueError(f"Error generating embeddings: {str(e)}")

            # Add documents to Chroma
            with logfire.span("storing_in_chroma"):
                try:
                    # Delete collection if it exists to ensure freshness
                    try:
                        self.chroma_client.delete_collection(name=settings.CHROMA_COLLECTION_NAME)
                    except:
                        pass  # Collection might not exist

                    collection = self.chroma_client.create_collection(name=settings.CHROMA_COLLECTION_NAME)
                    collection.add(
                        embeddings=embeddings, 
                        documents=chunks, 
                        metadatas=metadatas, 
                        ids=ids
                    )
                except Exception as e:
                    raise ValueError(f"Error storing data in Chroma DB: {str(e)}")

            return {
                "status": "success",
                "message": "Successfully ingested medicare data into vector database using semantic chunking",
                "chunk_count": len(chunks),
                "collection_name": settings.CHROMA_COLLECTION_NAME,
                "db_path": settings.VECTOR_DB_PATH,
            }
