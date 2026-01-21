from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import os
import logfire
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    ContextualRelevancyMetric,
    HallucinationMetric
)
from deepeval import evaluate

from google import genai
from deepeval.models import DeepEvalBaseLLM

from .query import QueryService
from ..core.config import settings


class GeminiGenAI(DeepEvalBaseLLM):
    def __init__(self, model_name, api_key):
        self.model_name = model_name
        self.client = genai.Client(api_key=api_key)

    def load_model(self):
        return self.client

    async def a_generate(self, prompt: str) -> str:
        try:
            # Note: We use the synchronous generate for now as the client is sync
            # If a sync client is used in an async context, it might block, 
            # but for this script it's acceptable.
            return self.generate(prompt)
        except Exception as e:
            logfire.error("Error in a_generate", error=str(e))
            return f"Error: {str(e)}"

    def generate(self, prompt: str) -> str:
        with logfire.span("deepeval_model_generate", model=self.model_name):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )
                if response and response.text:
                    return response.text
                # Return a dummy JSON that deepeval metrics might be expecting
                return '{"score": 0, "reason": "Model returned None (quota or safety)"}'
            except Exception as e:
                logfire.error("Error in generate", error=str(e))
                return '{"score": 0, "reason": "Error: ' + str(e) + '"}'

    def get_model_name(self):
        return self.model_name


class EvaluationService:
    """Service for evaluating RAG system performance using deepeval."""

    def __init__(self, query_service: QueryService):
        """Initialize the evaluation service.

        Args:
            query_service: The QueryService instance to evaluate
        """
        self.query_service = query_service
        self.eval_metrics_dir = "eval_results"
        os.makedirs(self.eval_metrics_dir, exist_ok=True)
        self.model = GeminiGenAI(
            model_name=settings.LLM_MODEL,
            api_key=settings.GEMINI_API_KEY
        )

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
        eval_id: Optional[str] = None
    ) -> Dict:
        """
        Evaluate a single query using deepeval metrics.

        Args:
            query: The question to evaluate
            expected_answer: The expected answer
            eval_id: Optional identifier for this evaluation

        Returns:
            Dict containing evaluation metrics
        """
        with logfire.span("evaluation_single_query", query=query):
            # Get the actual answer from our RAG system
            result = self.query_service.answer_question(query=query)
            
            # Create test case
            test_case = LLMTestCase(
                input=query,
                actual_output=result.answer,
                expected_output=expected_answer,
                retrieval_context=result.source_text,
            )

            # Run evaluation with comprehensive metrics
            metrics = [
                AnswerRelevancyMetric(threshold=0.7, model=self.model),
                FaithfulnessMetric(threshold=0.7, model=self.model),
                ContextualRelevancyMetric(threshold=0.7, model=self.model),
                HallucinationMetric(threshold=0.7, model=self.model)
            ]

            evaluation_results = evaluate([test_case], metrics)

            # Prepare results with metadata
            results = {
                "query": query,
                "expected_answer": expected_answer,
                "actual_answer": result.answer,
                "metrics": [
                    {"name": m.__class__.__name__, "score": m.score, "reason": m.reason}
                    for m in metrics
                ],
                "context_used": result.source_text,
                "timestamp": datetime.now().isoformat(),
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
    ) -> Dict:
        """
        Evaluate a dataset of queries using deepeval.

        Args:
            dataset: List of dicts containing 'query' and 'expected_answer' keys
            eval_id: Optional identifier for this evaluation

        Returns:
            Dict containing overall evaluation metrics and individual results
        """
        test_cases = []
        
        with logfire.span("evaluate_dataset_execution", size=len(dataset)):
            for item in dataset:
                result = self.query_service.answer_question(item["query"])
                
                test_case = LLMTestCase(
                    input=item["query"],
                    actual_output=result.answer,
                    expected_output=item["expected_answer"],
                    retrieval_context=result.source_text,
                )
                test_cases.append(test_case)

        # Define metrics
        metrics = [
            AnswerRelevancyMetric(threshold=0.7, model=self.model),
            FaithfulnessMetric(threshold=0.7, model=self.model),
            ContextualRelevancyMetric(threshold=0.7, model=self.model),
            HallucinationMetric(threshold=0.7, model=self.model)
        ]

        with logfire.span("deepeval_dataset_evaluation"):
            evaluation_results = evaluate(test_cases, metrics)

        # Prepare summary
        results = {
            "timestamp": datetime.now().isoformat(),
            "eval_id": eval_id or f"eval_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "dataset_size": len(dataset),
            "results": str(evaluation_results) # deepeval's evaluate returns a list of results
        }

        # Save results if eval_id is provided
        if eval_id:
            self._save_evaluation_results(results, eval_id)

        return results
