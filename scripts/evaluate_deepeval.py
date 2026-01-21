import asyncio
import os
import json
from typing import List, Dict
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    ContextualRelevancyMetric,
    HallucinationMetric
)
from deepeval import evaluate
from app.services.query import QueryService
from app.services.evaluation import GeminiGenAI
from app.core.config import settings
import logfire

# Configure logfire defensively
if settings.LOGFIRE_TOKEN:
    logfire.configure(token=settings.LOGFIRE_TOKEN)

async def run_batch_evaluation():
    """Run batch evaluation using generated synthetic test cases."""
    query_service = QueryService()
    
    # Load synthetic test cases
    goldens_path = "eval_data/goldens.json"
    if not os.path.exists(goldens_path):
        print(f"Error: Synthetic test cases not found at {goldens_path}. Run generate_synthetic_data.py first.")
        return

    with open(goldens_path, "r") as f:
        goldens = json.load(f)

    test_cases = []
    
    with logfire.span("batch_query_execution", num_cases=len(goldens)):
        for item in goldens:
            # Check if it's a list or a single golden
            # Deepeval's save_as usually exports a list of dicts
            query = item.get("input")
            expected_output = item.get("expected_output")
            retrieval_context = item.get("context", [])
            
            if not query:
                continue
                
            result = query_service.answer_question(query)
            
            test_case = LLMTestCase(
                input=query,
                actual_output=result.answer,
                expected_output=expected_output,
                retrieval_context=result.source_text
            )
            test_cases.append(test_case)
            
            # Rate limiting for Gemini free tier
            import time
            print(f"Waiting for rate limit (30s)...")
            time.sleep(30)

    # Define Metrics
    # Note: Threshold can be adjusted based on requirements
    model = GeminiGenAI(
        model_name=settings.LLM_MODEL,
        api_key=settings.GEMINI_API_KEY
    )
    
    metrics = [
        AnswerRelevancyMetric(threshold=0.7, model=model)
    ]

    with logfire.span("deepeval_batch_evaluation"):
        all_results = []
        for i, test_case in enumerate(test_cases):
            print(f"Evaluating test case {i+1}/{len(test_cases)}...")
            results = evaluate([test_case], metrics)
            all_results.append(results)
            if i < len(test_cases) - 1:
                print(f"Waiting for rate limit between evaluations (30s)...")
                time.sleep(30)

    print("\n--- Batch Evaluation Complete ---")
    
    # Save results
    os.makedirs("eval_results", exist_ok=True)
    # Convert results to a serializable format if needed or use deepeval's built-in reporting
    # For now, we'll just print that it's done.

if __name__ == "__main__":
    asyncio.run(run_batch_evaluation())
