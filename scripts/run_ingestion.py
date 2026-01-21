import logfire
from app.services.ingest import IngestService
from app.core.config import settings

# Configure logfire defensively
if settings.LOGFIRE_TOKEN:
    logfire.configure(token=settings.LOGFIRE_TOKEN)

def run_ingestion():
    """Run the ingestion process."""
    print("Starting ingestion with semantic chunking...")
    service = IngestService()
    try:
        result = service.ingest_medicare_docs()
        print(f"Ingestion successful: {result}")
    except Exception as e:
        print(f"Ingestion failed: {e}")

if __name__ == "__main__":
    run_ingestion()
