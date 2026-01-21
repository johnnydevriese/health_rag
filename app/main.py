from app.routers import batch, query, ingest, evaluation
from app.core.config import settings
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import logfire
from scalar_fastapi import get_scalar_api_reference

# Configure logfire defensively
if settings.LOGFIRE_TOKEN:
    logfire.configure(token=settings.LOGFIRE_TOKEN)
else:
    # Disable logfire if no token is provided to avoid authentication errors
    pass

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="API for answering Medicare questions using RAG",
    version=settings.VERSION,
    docs_url=None,  # Disable default Swagger UI
    redoc_url=None, # Disable default ReDoc UI
)

# Instrument FastAPI with logfire
logfire.instrument_fastapi(app)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Scalar documentation route
@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )

# Add routes
app.include_router(batch.router, prefix="/api/v1", tags=["batch"])
app.include_router(query.router, prefix="/api/v1", tags=["query"])
app.include_router(ingest.router, prefix="/api/v1", tags=["ingest"])
app.include_router(evaluation.router, prefix="/api/v1", tags=["evaluation"])


@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {"message": "Medicare Q&A RAG API", "docs_url": "/scalar", "version": "0.0.1"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
