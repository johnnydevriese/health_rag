import chromadb
import voyageai
from anthropic import Anthropic

from ..models.schemas import QueryResult


class QueryService:
    """Service for querying the vector database and generating answers."""

    def __init__(self):
        """Initialize the query service."""

        # Initialize clients -- keys automatically loaded
        self.voyage_client = voyageai.Client()
        self.anthropic_client = Anthropic()

        self.chroma_collection = chromadb.PersistentClient(
            path="vector_db"
        ).get_collection(name="medicare_docs")

    def answer_question(
        self, query: str, query_id: str = "Q1", top_k: int = 10, rerank_top_k: int = 3
    ) -> QueryResult:
        """
        Answer a question using RAG.

        Args:
            query: The question to answer
            query_id: Identifier for the query
            top_k: Number of documents to retrieve
            rerank_top_k: Number of documents to return after reranking

        Returns:
            QueryResult with the answer and source information
        """
        query_embedding = self.voyage_client.embed(
            texts=[query],
            model="voyage-3",
            input_type="query",
        ).embeddings[0]

        # Retrieve initial candidates from Chroma
        results = self.chroma_collection.query(
            query_embeddings=[query_embedding], n_results=top_k
        )

        # Get the retrieved documents and their ids
        candidate_docs = results["documents"][0]
        candidate_ids = results["ids"][0]

        # Apply VoyageAI reranker to improve results
        # how would you roll your own reranker.
        reranked_results = self.voyage_client.rerank(
            query=query,
            documents=candidate_docs,
            model="rerank-2-lite",
            top_k=rerank_top_k,
        )

        # Extract source information
        source_chunks = [candidate_ids[r.index] for r in reranked_results.results]
        source_text = [r.document for r in reranked_results.results]

        context_text = "\n\n".join(source_text)
        # other strategies outside of prompt design.

        prompt = f"""You are a helpful AI assistant that answers questions about Medicare based on the provided context.
        If the information isn't in the context, say you don't have that information.
        Keep your answers concise and to the point.

        Context:
        {context_text}

        Question: {query}"""

        response = self.anthropic_client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=80,
            temperature=0.0,
            system="You are a helpful AI assistant that provides accurate and concise answers about Medicare based on the provided context.",
            messages=[{"role": "user", "content": prompt}],
        )

        return QueryResult(
            query_id=query_id,
            query_text=query,
            answer=str(response.content[0].text),
            source_chunks=source_chunks,
            source_text=source_text,
        )
