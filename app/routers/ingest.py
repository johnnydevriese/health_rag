from fastapi import APIRouter, Depends, HTTPException

from ..services.ingest import IngestService

router = APIRouter()


def get_ingest_service():
    """Dependency to get the ingest service instance."""
    return IngestService()


@router.post(
    "/ingest-medicare-docs",
    summary="Ingest medicare documentation into the vector database",
)
async def ingest_medicare_docs(service: IngestService = Depends(get_ingest_service)):
    """
    Ingest medicare documentation into the vector database.

    This endpoint uses hardcoded paths:
    - Markdown file: app/gen-ai-homework-assignment/input/medicare_comparison.md
    - Chroma DB path: vector_db
    - Collection name: medicare_docs

    Returns status and information about the ingestion.
    """
    try:
        result = service.ingest_medicare_docs()
        return result

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error ingesting medicare docs: {str(e)}"
        )
