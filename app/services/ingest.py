import re
from typing import Any, Dict

import chromadb
import voyageai
from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.core.schema import Document


class IngestService:
    """Service for ingesting documents into the vector database."""

    # Hardcoded paths and settings
    MARKDOWN_FILE_PATH = "app/gen-ai-homework-assignment/input/medicare_comparison.md"
    CHROMA_DB_PATH = "vector_db"
    COLLECTION_NAME = "medicare_docs"

    def __init__(self):
        """Initialize the service."""
        self.voyage_client = voyageai.Client()
        self.chroma_client = chromadb.PersistentClient(path=self.CHROMA_DB_PATH)

    def preprocess_markdown_hierarchical(self, text):
        """Converts bold-only lines to H3 and italic-only lines to H4."""
        # Process bold lines first (**...** -> ### ...)
        h2_pattern = re.compile(r"^\s*\*\*([^*]+)\*\*\s*$", re.MULTILINE)
        processed_text = h2_pattern.sub(r"### \1\n", text)  # Use H3

        # Process italic lines next (*...* -> #### ...)
        h3_pattern = re.compile(r"^\s*\*([^*]+)\*\s*$", re.MULTILINE)
        processed_text = h3_pattern.sub(r"#### \1\n", processed_text)  # Use H4

        return processed_text

    def ingest_medicare_docs(self) -> Dict[str, Any]:
        """
        Ingest medicare docs into the vector database.

        Returns:
            Dict with ingestion status and details

        Raises:
            FileNotFoundError: If the markdown file doesn't exist
            ValueError: For processing errors
        """
        # Read and preprocess the markdown file
        try:
            with open(self.MARKDOWN_FILE_PATH, "r") as f:
                markdown_doc = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Markdown file not found at hardcoded path: {self.MARKDOWN_FILE_PATH}"
            )

        preprocessed_text = self.preprocess_markdown_hierarchical(markdown_doc)

        # Create a Document object from your string
        # ? would llama index handle super large files? 
        document = Document(text=preprocessed_text)

        # Initialize the Markdown parser and parse the document into nodes
        parser = MarkdownNodeParser()
        nodes = parser.get_nodes_from_documents([document])

        # Prepare text, metadata, and ids for embedding and storage
        texts = [node.get_content() for node in nodes]
        metadatas = [node.metadata for node in nodes]
        ids = [f"doc_{i}" for i in range(len(texts))]

        # Generate embeddings with VoyageAI
        try:
            embeddings_response = self.voyage_client.embed(
                texts=texts,
                model="voyage-3",
                input_type="document",
            )
            embeddings = embeddings_response.embeddings
        except Exception as e:
            raise ValueError(f"Error generating embeddings: {str(e)}")

        # Add documents to Chroma
        try:
            # Delete collection if it exists
            try:
                self.chroma_client.delete_collection(name=self.COLLECTION_NAME)
            except:
                pass  # Collection might not exist

            collection = self.chroma_client.create_collection(name=self.COLLECTION_NAME)
            collection.add(
                embeddings=embeddings, documents=texts, metadatas=metadatas, ids=ids
            )
        except Exception as e:
            raise ValueError(f"Error storing data in Chroma DB: {str(e)}")

        return {
            "status": "success",
            "message": "Successfully ingested medicare data into vector database",
            "node_count": len(nodes),
            "markdown_path": self.MARKDOWN_FILE_PATH,
            "collection_name": self.COLLECTION_NAME,
            "db_path": self.CHROMA_DB_PATH,
        }
