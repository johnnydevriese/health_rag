from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# from .api.endpoints import router
from app.routers import batch, query, ingest, evaluation

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Medicare Q&A RAG API",
    description="API for answering Medicare questions using RAG",
    version="0.0.1",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add routes
# app.include_router(router, prefix="/api")

app.include_router(batch.router, prefix="/api/v1", tags=["batch"])
app.include_router(query.router, prefix="/api/v1", tags=["query"])
app.include_router(ingest.router, prefix="/api/v1", tags=["ingest"])
app.include_router(evaluation.router, prefix="/api/v1", tags=["evaluation"])


@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {"message": "Medicare Q&A RAG API", "docs_url": "/docs", "version": "0.0.1"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
