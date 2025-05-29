from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ..services.evaluation import EvaluationService
from ..services.query import QueryService
from ..dependencies import get_query_service

router = APIRouter()


class EvaluationRequest(BaseModel):
    """Request model for single query evaluation."""

    query: str
    expected_answer: str
    eval_id: Optional[str] = None
    model_version: Optional[str] = None


class DatasetEvaluationRequest(BaseModel):
    """Request model for dataset evaluation."""

    dataset: List[Dict[str, str]]
    eval_id: Optional[str] = None
    model_version: Optional[str] = None


class ModelComparisonRequest(BaseModel):
    """Request model for comparing different model versions."""

    dataset: List[Dict[str, str]]
    model_versions: List[str]
    eval_id: Optional[str] = None


def get_evaluation_service(
    query_service: QueryService = Depends(get_query_service),
) -> EvaluationService:
    """Dependency to get evaluation service instance."""
    return EvaluationService(query_service)


@router.post("/evaluate-query", summary="Evaluate a single query")
async def evaluate_query(
    request: EvaluationRequest,
    evaluation_service: EvaluationService = Depends(get_evaluation_service),
):
    """
    Evaluate a single query using deepeval metrics.

    Args:
        request: The evaluation request containing query and expected answer
        evaluation_service: The evaluation service instance

    Returns:
        Evaluation results including metrics
    """
    try:
        result = evaluation_service.evaluate_single_query(
            query=request.query,
            expected_answer=request.expected_answer,
            eval_id=request.eval_id,
            model_version=request.model_version,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating query: {str(e)}")


@router.post("/evaluate-dataset", summary="Evaluate a dataset of queries")
async def evaluate_dataset(
    request: DatasetEvaluationRequest,
    evaluation_service: EvaluationService = Depends(get_evaluation_service),
):
    """
    Evaluate a dataset of queries using deepeval metrics.

    Args:
        request: The evaluation request containing a list of queries and expected answers
        evaluation_service: The evaluation service instance

    Returns:
        Overall evaluation metrics and individual results
    """
    try:
        result = evaluation_service.evaluate_dataset(
            dataset=request.dataset,
            eval_id=request.eval_id,
            model_version=request.model_version,
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error evaluating dataset: {str(e)}"
        )


@router.post("/compare-models", summary="Compare different model versions")
async def compare_models(
    request: ModelComparisonRequest,
    evaluation_service: EvaluationService = Depends(get_evaluation_service),
):
    """
    Compare performance of different model versions on the same dataset.

    Args:
        request: The comparison request containing dataset and model versions
        evaluation_service: The evaluation service instance

    Returns:
        Comparison results for each model version
    """
    try:
        result = evaluation_service.compare_model_versions(
            dataset=request.dataset,
            model_versions=request.model_versions,
            eval_id=request.eval_id,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error comparing models: {str(e)}")
