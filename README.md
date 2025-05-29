# Medicare RAG API

A FastAPI-based Retrieval Augmented Generation (RAG) system for answering questions about Medicare information, using Claude for answer generation and deepeval for evaluation.

## Features

- **Modern Python Setup**: Uses `pyproject.toml` and `uv` for dependency management and virtual environment handling
- **RAG Pipeline**:
  - Embedding generation with VoyageAI
  - Vector DB search with Chroma
  - Reranking with VoyageAI
  - Answer generation with Claude
- **Evaluation System**:
  - Comprehensive metrics with deepeval
  - A/B testing capabilities
  - Automated evaluation pipeline
  - Metrics tracking and monitoring

## Project Structure

```
app/
├── services/
│   ├── __init__.py
│   ├── query.py              # QueryService for answering questions
│   ├── batch_processing.py   # BatchProcessingService for batch operations
│   ├── ingest.py            # IngestService for data ingestion
│   └── evaluation.py        # EvaluationService for RAG evaluation
├── routers/
│   ├── __init__.py
│   ├── batch.py             # Batch processing endpoints
│   ├── query.py             # Individual query endpoints
│   ├── ingest.py            # Data ingestion endpoints
│   └── evaluation.py        # Evaluation endpoints
├── models/
│   ├── __init__.py
│   └── schemas.py           # Pydantic models for requests and responses
└── main.py                  # FastAPI application setup
```

## Setup and Installation

### Prerequisites

- Python 3.12+
- VoyageAI API key
- Anthropic API key

### Local Development Setup

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd health_rag
   ```

2. Run the setup script (this will install uv if needed, create a virtual environment, and install all dependencies):

   ```bash
   ./scripts/setup_dev.sh
   ```

3. Copy and configure environment variables:

   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. Activate the virtual environment (if not already activated by setup_dev.sh):
   ```bash
   source .venv/bin/activate
   ```

### Docker Setup

Build and run with Docker:

```bash
docker build -t health-rag .
docker run -p 8000:8000 --env-file .env health-rag
```

## API Endpoints

### Query Endpoint

```
POST /api/v1/ask
```

Answer a single question using RAG.

**Request:**

```json
{
  "query": "Can I see any doctor with Original Medicare?",
  "query_id": "Q1",
  "top_k": 10,
  "rerank_top_k": 2
}
```

### Evaluation Endpoints

#### Single Query Evaluation

```
POST /api/v1/evaluate-query
```

**Request:**

```json
{
  "query": "What are Medicare benefits?",
  "expected_answer": "Medicare provides coverage for hospital stays, medical services, and preventive care.",
  "eval_id": "eval_20240315_001",
  "model_version": "claude-3-sonnet"
}
```

#### Dataset Evaluation

```
POST /api/v1/evaluate-dataset
```

**Request:**

```json
{
  "dataset": [
    {
      "query": "What are Medicare benefits?",
      "expected_answer": "Medicare provides coverage for hospital stays, medical services, and preventive care."
    }
  ],
  "eval_id": "daily_eval_20240315",
  "model_version": "claude-3-sonnet"
}
```

#### Model Comparison

```
POST /api/v1/compare-models
```

**Request:**

```json
{
  "dataset": [
    {
      "query": "What are Medicare benefits?",
      "expected_answer": "Medicare provides coverage for hospital stays, medical services, and preventive care."
    }
  ],
  "model_versions": ["claude-3-sonnet", "claude-3-opus"],
  "eval_id": "model_comparison_20240315"
}
```

## Development

### Code Quality

The project uses Ruff for linting and formatting:

```bash
# Format code
ruff format .

# Lint code
ruff check .
```

### Testing

Run tests with pytest:

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=app
```

### Production Evaluation

For production deployments, set up automated evaluations:

1. **Scheduled Evaluations**

   ```bash
   # Example cron job for daily evaluations
   0 0 * * * curl -X POST http://your-api/api/v1/evaluate-dataset \
     -H "Content-Type: application/json" \
     -d '{"dataset": [...], "eval_id": "daily_eval_$(date +%Y%m%d)"}'
   ```

2. **Environment Variables**

   ```bash
   EVAL_METRICS_DIR=/path/to/metrics/storage
   ```

3. **Monitoring**
   - Set up monitoring for key metrics:
     - Hallucination rate
     - Answer relevancy score
     - Response time
   - Create alerts for:
     - Sudden drops in performance
     - High hallucination rates
     - Slow response times

## Dependencies

The project uses modern Python packaging with `pyproject.toml`. Key dependencies:

- `anthropic`: Claude API client
- `chromadb`: Vector database
- `fastapi`: Web framework
- `voyageai`: Embedding and reranking
- `deepeval`: RAG evaluation
- `pydantic`: Data validation
- `uvicorn`: ASGI server
