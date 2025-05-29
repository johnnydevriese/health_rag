import json
import os
from typing import Any, Dict, List

from ..services.query import QueryService


class BatchProcessingService:
    """Service for processing batches of queries from a hardcoded file."""

    # Hardcoded paths for demo
    QUERIES_PATH = "app/gen-ai-homework-assignment/input/queries.json"
    ANSWERS_PATH = "app/gen-ai-homework-assignment/output/answers.json"

    def __init__(self, query_service: QueryService):
        """Initialize with the query service.

        Args:
            query_service: The QueryService for answering queries
        """
        self.query_service = query_service

    def process_batch(self) -> Dict[str, Any]:
        """Process a batch of questions from the hardcoded file.

        Returns:
            Dict with processing status and details

        Raises:
            FileNotFoundError: If the queries file doesn't exist
            ValueError: For JSON format issues or processing errors
        """

        if not os.path.exists(self.QUERIES_PATH):
            raise FileNotFoundError(
                f"Queries file not found at hardcoded path: {self.QUERIES_PATH}"
            )

        try:
            with open(self.QUERIES_PATH, "r") as f:
                queries_data = json.load(f)
        except json.JSONDecodeError:
            raise ValueError(
                f"Invalid JSON format in queries file: {self.QUERIES_PATH}"
            )

        results = []
        for query_item in queries_data:
            try:
                query_text = query_item.get("text", "")
                query_id = query_item.get("id", "")

                result = self.query_service.answer_question(
                    query=query_text,
                    query_id=query_id,
                )

                results.append(result.model_dump())
            except Exception as e:
                # Log error but continue processing other queries
                print(
                    f"Error processing query {query_item.get('id', 'unknown')}: {str(e)}"
                )
                # Add a failed result to the results list
                results.append(
                    {
                        "id": query_item.get("id", "unknown"),
                        "text": query_text,
                        "error": str(e),
                        "status": "failed",
                    }
                )

        # Write results to the answers file
        os.makedirs(os.path.dirname(self.ANSWERS_PATH), exist_ok=True)
        with open(self.ANSWERS_PATH, "w") as f:
            json.dump(results, f, indent=2)

        return {
            "status": "success",
            "message": "Successfully processed batch queries",
            "query_count": len(queries_data),
            "processed_count": len(results),
            "queries_path": self.QUERIES_PATH,
            "answers_path": self.ANSWERS_PATH,
        }
