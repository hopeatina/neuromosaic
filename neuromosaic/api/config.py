"""
API-specific configuration settings.

Defines configuration variables for the FastAPI service, 
such as host, port, DB credentials, and orchestrator settings.
"""

from typing import List, Optional
from pathlib import Path

from pydantic_settings import BaseSettings


class APISettings(BaseSettings):
    """API configuration settings."""

    # CORS settings
    cors_origins: List[str] = [
        "http://localhost:8050",  # Default Dash frontend
        "http://localhost:8501",  # Default Streamlit frontend
        "http://127.0.0.1:8050",
        "http://127.0.0.1:8501",
    ]

    # API settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = False
    reload: bool = False
    workers: int = 1
    log_level: str = "info"

    # Database settings
    db_url: str = "sqlite:///neuromosaic.db"
    db_pool_size: int = 5
    db_max_overflow: int = 10
    db_pool_timeout: int = 30
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "neuromosaic"
    db_user: str = "postgres"
    db_password: str = ""

    # Storage settings
    storage_root: Path = Path("/tmp/neuromosaic")
    max_cache_size: str = "50GB"
    artifact_retention_days: int = 30

    # Container settings
    docker_registry: Optional[str] = None
    container_cpu_limit: int = 4
    container_memory_limit: str = "8G"
    container_gpu_limit: int = 1

    # Orchestrator settings
    orchestrator_config_path: Optional[Path] = None
    max_concurrent_experiments: int = 5
    experiment_timeout: int = 3600  # 1 hour

    # Architecture space settings
    arch_space_config_path: Optional[Path] = None
    arch_space_cache_size: int = 1000

    # API Keys and Authentication
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    cohere_api_key: Optional[str] = None
    dataset_api_key: Optional[str] = None
    huggingface_token: Optional[str] = None
    auth_secret_key: Optional[str] = None
    encryption_key: Optional[str] = None

    # W&B Integration
    enable_wandb: bool = False
    wandb_api_key: Optional[str] = None
    wandb_project: Optional[str] = None
    wandb_entity: Optional[str] = None

    # Environment
    environment: str = "development"

    class Config:
        """Pydantic config."""

        env_prefix = "NEUROMOSAIC_API_"
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"  # Allow extra fields


_settings = None


def get_api_settings() -> APISettings:
    """Get API settings singleton."""
    global _settings
    if _settings is None:
        _settings = APISettings()
    return _settings
