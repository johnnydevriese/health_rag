# Medicare Q&A RAG API (Gemini + VoyageAI)

A modernized FastAPI-based Retrieval Augmented Generation (RAG) system for answering questions about Medicare information. It features enterprise-grade semantic chunking, Google Gemini integration, and a robust evaluation framework.

## Features

- **Google Gemini Integration**: Uses the `google-genai` (python-genai) SDK for state-of-the-art generation using `gemini-3-flash-preview`.
- **Enterprise-Grade Semantic Chunking**: Implements an advanced chunking strategy using VoyageAI embeddings to ensure context retains its semantic meaning.
- **RAG Pipeline**:
  - Semantic chunking for high-quality text segmentation.
  - Embedding generation and Reranking with **VoyageAI**.
  - Vector DB search with **Chroma**.
  - Generation with **Google Gemini**.
- **Observability**: Built-in tracing and monitoring with **Pydantic Logfire**.
- **Interactive Documentation**: Beautiful API docs powered by **Scalar** (accessible at `/scalar`).
- **Modern Python Tooling**: Fully managed with **`uv`** for lightspeed dependency management and reproducible environments.

## Project Structure

```
.
├── app/
│   ├── core/
│   │   └── config.py        # Centralized Pydantic Settings
│   ├── services/
│   │   ├── query.py          # QueryService (Retriever, Reranker, Generator)
│   │   ├── ingest.py         # IngestService with Semantic Chunking
│   │   ├── evaluation.py      # EvaluationService with GeminiGenAI wrapper
│   │   └── semantic_chunking.py # Enterprise semantic chunker
│   └── routers/              # FastAPI routers (query, ingest, etc.)
├── scripts/
│   ├── run_ingestion.py      # Populate the database
│   ├── evaluate_deepeval.py  # Batch evaluation suite
│   ├── generate_synthetic_data.py # Create test cases (Synthesizer)
│   └── list_gemini_models.py # Diagnostic tool for available models
├── eval_data/               # Test goldens and generated cases
└── eval_results/            # JSON results from evaluation runs
```

## Setup and Installation

### Prerequisites

- Python 3.12+
- `uv` (recommended)
- **VoyageAI API Key**: For embeddings and reranking.
- **Google Gemini API Key**: For generation and evaluation.

### Local Development Setup

1. **Clone and Install**:
   ```bash
   git clone <repository-url>
   cd health_rag
   uv sync
   ```

2. **Configure Environment**:
   ```bash
   cp .env.example .env
   # Edit .env and paste your GEMINI_API_KEY and VOYAGE_API_KEY
   ```

3. **Ingest Data**:
   ```bash
   uv run scripts/run_ingestion.py
   ```

4. **Start the API**:
   ```bash
   uv run uvicorn app.main:app --reload
   ```

Access the interactive documentation at `http://localhost:8000/scalar`.

## Evaluation System Overview

The project includes a comprehensive evaluation framework powered by **DeepEval**, customized to work seamlessly with the **Google Gemini** API.

### Key Components

- **GeminiGenAI Wrapper**: A custom `DeepEvalBaseLLM` implementation that enables DeepEval metrics to use the new `google-genai` SDK.
- **Automated Batch Evaluation**: The `scripts/evaluate_deepeval.py` script runs a full suite of RAG metrics.
- **Core Metrics**:
  - **Answer Relevancy**: Measures how relevant the answer is to the given query.
  - **Faithfulness**: Ensures the answer is derived strictly from the retrieved context (no hallucinations).
  - **Contextual Relevancy**: Evaluates how relevant the retrieved segments are to the query.

### Optimizing for Free Tier Quotas

To support running evaluations on a budget (or under strict API quotas), the system includes:
- **Serial Processing**: Evaluations run one at a time rather than in parallel.
- **Deliberate Rate Limiting**: A 30-second delay between queries ensures you stay within the 5 RPM limits of Gemini's free tier.
- **Robust Error Handling**: The system handles empty responses and API errors gracefully, returning readable diagnostics instead of crashing.

### Running Evaluations

1. **Generate Synthetic Data** (Optional):
   ```bash
   uv run scripts/generate_synthetic_data.py
   ```

2. **Run Batch Evaluation**:
   ```bash
   uv run scripts/evaluate_deepeval.py
   ```

## Observability

We use **Pydantic Logfire** for deep visibility into every step of the RAG pipeline.

- **To Authenticate**: Run `uv run logfire auth`
- **To View Traces**: Traces are automatically sent to your Logfire dashboard if a token is configured or you are authenticated locally.

## Development

- **Formatting**: `uv run ruff format .`
- **Linting**: `uv run ruff check .`
- **Tests**: `uv run pytest`
