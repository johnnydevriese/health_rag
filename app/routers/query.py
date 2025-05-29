from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any

from ..services.query import QueryService
from ..models.schemas import QueryRequest, QueryResult

router = APIRouter()


def get_query_service():
    """Dependency to get the query service instance."""
    return QueryService()


@router.post("/ask", response_model=QueryResult, summary="Answer a question using RAG")
async def ask_question(
    query: QueryRequest, service: QueryService = Depends(get_query_service)
):
    """
    Answer a question using RAG (Retrieval-Augmented Generation).

    The endpoint retrieves relevant context from the vector database,
    reranks the results, and generates an answer using an LLM.

    Returns the answer along with source information.
    """
    try:
        result = service.answer_question(
            query=query.query,
            query_id=query.query_id,
            top_k=query.top_k or 10,
            rerank_top_k=query.rerank_top_k or 3,
        )
        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error answering question: {str(e)}"
        )
