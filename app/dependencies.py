from .services.query import QueryService
from .services.ingest import IngestService
from .services.evaluation import EvaluationService

# Global instances for simple singleton-like behavior or initialization logic
_query_service = QueryService()
_ingest_service = IngestService()
_evaluation_service = EvaluationService(_query_service)

def get_query_service() -> QueryService:
    """Dependency provider for QueryService."""
    return _query_service

def get_ingest_service() -> IngestService:
    """Dependency provider for IngestService."""
    return _ingest_service

def get_evaluation_service() -> EvaluationService:
    """Dependency provider for EvaluationService."""
    return _evaluation_service
