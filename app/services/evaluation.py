from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import os
from deepeval import evaluate
from deepeval.metrics import (
    HallucinationMetric,
    AnswerRelevancyMetric,
    ContextualRelevancyMetric,
    FactualConsistencyMetric,
    ResponseTimeMetric,
)
from deepeval.test_case import LLMTestCase
from deepeval.dataset import EvaluationDataset

from .query import QueryService


class EvaluationService:
    """Service for evaluating RAG system performance using deepeval."""

    def __init__(self, query_service: QueryService):
        """Initialize the evaluation service.

        Args:
            query_service: The QueryService instance to evaluate
        """
        self.query_service = query_service
        self.eval_metrics_dir = os.getenv("EVAL_METRICS_DIR", "eval_metrics")
        os.makedirs(self.eval_metrics_dir, exist_ok=True)

    def _save_evaluation_results(self, results: Dict[str, Any], eval_id: str) -> str:
        """Save evaluation results to disk.

        Args:
            results: The evaluation results to save
            eval_id: Unique identifier for this evaluation

        Returns:
            Path to the saved results file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{eval_id}_{timestamp}.json"
        filepath = os.path.join(self.eval_metrics_dir, filename)

        with open(filepath, "w") as f:
            json.dump(results, f, indent=2)

        return filepath

    def evaluate_single_query(
        self,
        query: str,
        expected_answer: str,
        context: Optional[List[str]] = None,
        eval_id: Optional[str] = None,
        model_version: Optional[str] = None,
    ) -> Dict:
        """
        Evaluate a single query using deepeval metrics.

        Args:
            query: The question to evaluate
            expected_answer: The expected answer
            context: Optional list of context strings to evaluate against
            eval_id: Optional identifier for this evaluation
            model_version: Optional model version identifier for A/B testing

        Returns:
            Dict containing evaluation metrics
        """
        # Get the actual answer from our RAG system
        result = self.query_service.answer_question(query=query)
        actual_answer = result.answer
        actual_context = result.source_text

        # Create test case
        test_case = LLMTestCase(
            input=query,
            actual_output=actual_answer,
            expected_output=expected_answer,
            context=context or actual_context,
        )

        # Run evaluation with comprehensive metrics
        metrics = [
            HallucinationMetric(),
            AnswerRelevancyMetric(),
            ContextualRelevancyMetric(),
            FactualConsistencyMetric(),
            ResponseTimeMetric(),
        ]

        evaluation_results = evaluate(
            [test_case],
            metrics=metrics,
        )

        # Prepare results with metadata
        results = {
            "query": query,
            "expected_answer": expected_answer,
            "actual_answer": actual_answer,
            "metrics": evaluation_results,
            "context_used": actual_context,
            "timestamp": datetime.now().isoformat(),
            "model_version": model_version or "default",
            "eval_id": eval_id or f"eval_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        }

        # Save results if eval_id is provided
        if eval_id:
            self._save_evaluation_results(results, eval_id)

        return results

    def evaluate_dataset(
        self,
        dataset: List[Dict[str, str]],
        eval_id: Optional[str] = None,
        model_version: Optional[str] = None,
    ) -> Dict:
        """
        Evaluate a dataset of queries using deepeval.

        Args:
            dataset: List of dicts containing 'query' and 'expected_answer' keys
            eval_id: Optional identifier for this evaluation
            model_version: Optional model version identifier for A/B testing

        Returns:
            Dict containing overall evaluation metrics and individual results
        """
        test_cases = []
        individual_results = []

        for item in dataset:
            query = item["query"]
            expected_answer = item["expected_answer"]

            # Get the actual answer from our RAG system
            result = self.query_service.answer_question(query=query)
            actual_answer = result.answer
            actual_context = result.source_text

            # Create test case
            test_case = LLMTestCase(
                input=query,
                actual_output=actual_answer,
                expected_output=expected_answer,
                context=actual_context,
            )
            test_cases.append(test_case)

            individual_results.append(
                {
                    "query": query,
                    "expected_answer": expected_answer,
                    "actual_answer": actual_answer,
                    "context_used": actual_context,
                }
            )

        # Run evaluation with comprehensive metrics
        metrics = [
            HallucinationMetric(),
            AnswerRelevancyMetric(),
            ContextualRelevancyMetric(),
            FactualConsistencyMetric(),
            ResponseTimeMetric(),
        ]

        evaluation_results = evaluate(
            test_cases,
            metrics=metrics,
        )

        # Prepare results with metadata
        results = {
            "overall_metrics": evaluation_results,
            "individual_results": individual_results,
            "timestamp": datetime.now().isoformat(),
            "model_version": model_version or "default",
            "eval_id": eval_id or f"eval_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "dataset_size": len(dataset),
        }

        # Save results if eval_id is provided
        if eval_id:
            self._save_evaluation_results(results, eval_id)

        return results

    def compare_model_versions(
        self,
        dataset: List[Dict[str, str]],
        model_versions: List[str],
        eval_id: Optional[str] = None,
    ) -> Dict:
        """
        Compare performance of different model versions on the same dataset.

        Args:
            dataset: List of dicts containing 'query' and 'expected_answer' keys
            model_versions: List of model version identifiers to compare
            eval_id: Optional identifier for this evaluation

        Returns:
            Dict containing comparison results for each model version
        """
        comparison_results = {}

        for version in model_versions:
            # Temporarily set model version in query service
            original_version = self.query_service.model_version
            self.query_service.model_version = version

            # Run evaluation for this version
            results = self.evaluate_dataset(
                dataset=dataset,
                eval_id=f"{eval_id}_{version}" if eval_id else None,
                model_version=version,
            )
            comparison_results[version] = results

            # Restore original model version
            self.query_service.model_version = original_version

        return {
            "comparison_results": comparison_results,
            "timestamp": datetime.now().isoformat(),
            "eval_id": eval_id
            or f"comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        }
