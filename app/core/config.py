from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings using Pydantic BaseSettings."""
    
    # API Keys
    GEMINI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    VOYAGE_API_KEY: str
    
    # App Configuration
    APP_NAME: str = "Medicare Q&A RAG API"
    VERSION: str = "0.0.1"
    LLM_MODEL: str = "gemini-1.5-flash"
    
    # Database Configuration
    VECTOR_DB_PATH: str = Field("vector_db", alias="CHROMA_PATH")
    CHROMA_COLLECTION_NAME: str = Field("medicare_docs", alias="DEFAULT_COLLECTION_NAME")
    
    # Observability
    LOGFIRE_TOKEN: Optional[str] = Field(None, alias="LOGFIRE_API_KEY")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True
    )

# Global settings instance
settings = Settings()
