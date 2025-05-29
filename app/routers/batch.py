from fastapi import APIRouter, Depends, HTTPException

from ..services.batch import BatchProcessingService
from ..services.query import QueryService

router = APIRouter()


def get_query_service():
    """Dependency to get the core service instance."""
    return QueryService()


def get_batch_service(query_service: QueryService = Depends(get_query_service)):
    """Dependency to get the batch processing service."""
    return BatchProcessingService(query_service)


@router.post(
    "/process-batch",
    summary="Process queries from the hardcoded file and write answers to another hardcoded file",
)
async def process_batch(
    batch_service: BatchProcessingService = Depends(get_batch_service),
):
    """
    Process a batch of questions from a hardcoded file and save results to another hardcoded file.

    This endpoint:
    1. Reads questions from app/gen-ai-homework-assignment/input/queries.json
    2. Processes each question using the RAG pipeline
    3. Saves the results to app/gen-ai-homework-assignment/output/answers.json

    Returns status and information about the batch processing.
    """
    try:
        result = batch_service.process_batch()
        return result

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing batch: {str(e)}")
