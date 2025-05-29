from typing import ClassVar, List, Optional

from pydantic import BaseModel, Field


class QueryResult(BaseModel):
    """
    A model representing the result of a query.
    Includes the query details, the generated answer,
    and the supporting source information.
    """

    query_id: str = Field(description="Unique identifier for the query")
    query_text: str = Field(description="The original query text")
    answer: str = Field(description="The generated answer to the query")
    source_chunks: List[str] = Field(description="List of source chunk identifiers")
    source_text: List[str] = Field(description="List of supporting text from sources")

    class Config:
        json_schema_extra: ClassVar[dict] = {
            "example": {
                "query_id": "Q1",
                "query_text": "Can I see any doctor with Original Medicare?",
                "answer": "Yes, with Original Medicare, you can see any doctor that"
                " accepts Medicare patients.",
                "source_chunks": ["chunk_123", "chunk_456"],
                "source_text": [
                    "Original Medicare allows you to see any doctor that accepts Medicare.",
                    "Doctors who accept Medicare assignment agree to accept Medicare's approved amount as payment in full.",
                ],
            },
        }


class QueryRequest(BaseModel):
    """Request model for a single query."""

    query: str = Field(..., description="The question to answer")
    query_id: str = Field(default="Q1", description="Optional query identifier")
    top_k: Optional[int] = Field(None, description="Number of documents to retrieve")
    rerank_top_k: Optional[int] = Field(
        None, description="Number of documents to return after reranking"
    )
