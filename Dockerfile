FROM python:3.12-slim

WORKDIR /app

# Install build dependencies and uv
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && curl -LsSf https://astral.sh/uv/install.sh | sh

# Copy project files
COPY pyproject.toml .
COPY app/ ./app/

# Create directories for data
RUN mkdir -p ./chroma_db

# Set environment variables
ENV PYTHONPATH=/app
ENV CHROMA_PATH=/app/chroma_db
ENV DEFAULT_COLLECTION_NAME=medicare_docs

# Install dependencies using uv
RUN uv pip install --system .

# Expose the port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]