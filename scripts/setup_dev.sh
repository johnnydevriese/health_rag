#!/bin/bash

# Install uv if not already installed
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Create and activate virtual environment
echo "Creating virtual environment..."
uv venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
uv pip install -e .

# Install development dependencies
echo "Installing development dependencies..."
uv pip install ruff black pytest pytest-cov

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p eval_metrics
mkdir -p chroma_db

echo "Setup complete! Don't forget to:"
echo "1. Copy .env.example to .env and fill in your API keys"
echo "2. Activate the virtual environment with: source .venv/bin/activate" 