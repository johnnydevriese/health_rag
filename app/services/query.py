import voyageai
import chromadb
import logfire
from google import genai
from typing import List, Tuple

from ..models.schemas import QueryResult
from ..core.config import settings


class Retriever:
    def __init__(self, voyage_client: voyageai.Client, collection: chromadb.Collection):
        self.voyage_client = voyage_client
        self.collection = collection

    def retrieve(self, query: str, top_k: int = 10) -> Tuple[List[str], List[str]]:
        with logfire.span("retrieval", query=query, top_k=top_k):
            query_embedding = self.voyage_client.embed(
                texts=[query],
                model="voyage-3",
                input_type="query",
            ).embeddings[0]

            results = self.collection.query(
                query_embeddings=[query_embedding], n_results=top_k
            )
            
            return results["documents"][0], results["ids"][0]


class Reranker:
    def __init__(self, voyage_client: voyageai.Client):
        self.voyage_client = voyage_client

    def rerank(self, query: str, documents: List[str], ids: List[str], top_k: int = 3) -> Tuple[List[str], List[str]]:
        with logfire.span("reranking", num_docs=len(documents), top_k=top_k):
            results = self.voyage_client.rerank(
                query=query,
                documents=documents,
                model="rerank-2-lite",
                top_k=top_k,
            )
            
            reranked_docs = [results.results[i].document for i in range(len(results.results))]
            reranked_ids = [ids[results.results[i].index] for i in range(len(results.results))]
            
            return reranked_docs, reranked_ids


class Generator:
    def __init__(self):
        """Initialize Google GenAI client based on configuration."""
        self.model_name = settings.LLM_MODEL
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def generate(self, query: str, context: str) -> str:
        with logfire.span("generation", model=self.model_name, provider="google-genai"):
            prompt = f"""You are a helpful AI assistant that provides accurate and concise answers about Medicare based on the provided context.
If the information isn't in the context, say you don't have that information.
Keep your answers concise and to the point.

Context:
{context}

Question: {query}"""

            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )
                if response and response.text:
                    return response.text
                return "Error: No text returned from model (check safety filters or model availability)."
            except Exception as e:
                logfire.error("Error generating content with Gemini", error=str(e))
                return f"Error: {str(e)}"


class QueryService:
    """Service for querying the vector database and generating answers."""

    def __init__(self):
        """Initialize the query service."""
        # Initialize clients -- keys automatically loaded from env by clients
        self.voyage_client = voyageai.Client(api_key=settings.VOYAGE_API_KEY)

        self.chroma_collection = chromadb.PersistentClient(
            path=settings.VECTOR_DB_PATH
        ).get_collection(name=settings.CHROMA_COLLECTION_NAME)

        self.retriever = Retriever(self.voyage_client, self.chroma_collection)
        self.reranker = Reranker(self.voyage_client)
        self.generator = Generator()



    def answer_question(
        self, query: str, query_id: str = "Q1", top_k: int = 10, rerank_top_k: int = 3
    ) -> QueryResult:
        """Answer a question using the RAG pipeline with modular components and tracing."""
        with logfire.span("answer_question", query=query, query_id=query_id):
            # 1. Retrieve
            candidate_docs, candidate_ids = self.retriever.retrieve(query, top_k=top_k)

            # 2. Rerank
            reranked_docs, reranked_ids = self.reranker.rerank(
                query, candidate_docs, candidate_ids, top_k=rerank_top_k
            )

            # 3. Generate
            context_text = "\n\n".join(reranked_docs)
            answer = self.generator.generate(query, context_text)

            return QueryResult(
                query_id=query_id,
                query_text=query,
                answer=answer,
                source_chunks=reranked_ids,
                source_text=reranked_docs,
            )
