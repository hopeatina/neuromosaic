"""
Configuration management for Neuromosaic.

This module handles loading and validating configuration from multiple sources:
1. Default values
2. Configuration files (config.yaml)
3. Environment variables
4. Command line arguments

Environment variables take precedence over config file values.
Command line arguments take precedence over environment variables.

Example:
    >>> from neuromosaic.utils.config import load_config
    >>> config = load_config()
    >>> print(config.storage.cache_size)
    "50GB"
"""

import os
import yaml
import logging
from pathlib import Path
from typing import Any, Dict, Optional, Union
from dataclasses import dataclass, field
from dotenv import load_dotenv

from .exceptions import ConfigurationError

# Load environment variables from .env file
load_dotenv()


@dataclass
class LLMConfig:
    """Configuration for LLM providers."""

    openai_api_key: Optional[str] = field(default=None)
    anthropic_api_key: Optional[str] = field(default=None)
    cohere_api_key: Optional[str] = field(default=None)

    @classmethod
    def from_env(cls) -> "LLMConfig":
        """Create config from environment variables."""
        return cls(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            cohere_api_key=os.getenv("COHERE_API_KEY"),
        )


@dataclass
class StorageConfig:
    """Configuration for data and artifact storage."""

    root: Path = field(default=Path("data"))
    cache_size: str = field(default="50GB")
    artifact_retention_days: int = field(default=30)

    @classmethod
    def from_env(cls) -> "StorageConfig":
        """Create config from environment variables."""
        return cls(
            root=Path(os.getenv("STORAGE_ROOT", "data")),
            cache_size=os.getenv("MAX_CACHE_SIZE", "50GB"),
            artifact_retention_days=int(os.getenv("ARTIFACT_RETENTION_DAYS", "30")),
        )


@dataclass
class DatabaseConfig:
    """Configuration for database connection."""

    host: str = field(default="localhost")
    port: int = field(default=5432)
    name: str = field(default="neuromosaic")
    user: str = field(default="postgres")
    password: Optional[str] = field(default=None)

    @classmethod
    def from_env(cls) -> "DatabaseConfig":
        """Create config from environment variables."""
        return cls(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "5432")),
            name=os.getenv("DB_NAME", "neuromosaic"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD"),
        )


@dataclass
class ContainerConfig:
    """Configuration for container execution."""

    registry: Optional[str] = field(default=None)
    cpu_limit: int = field(default=4)
    memory_limit: str = field(default="8G")
    gpu_limit: int = field(default=1)

    @classmethod
    def from_env(cls) -> "ContainerConfig":
        """Create config from environment variables."""
        return cls(
            registry=os.getenv("DOCKER_REGISTRY"),
            cpu_limit=int(os.getenv("CONTAINER_CPU_LIMIT", "4")),
            memory_limit=os.getenv("CONTAINER_MEMORY_LIMIT", "8G"),
            gpu_limit=int(os.getenv("CONTAINER_GPU_LIMIT", "1")),
        )


@dataclass
class MonitoringConfig:
    """Configuration for monitoring and logging."""

    log_level: str = field(default="INFO")
    enable_wandb: bool = field(default=False)
    wandb_api_key: Optional[str] = field(default=None)
    wandb_project: str = field(default="neuromosaic")
    wandb_entity: Optional[str] = field(default=None)

    @classmethod
    def from_env(cls) -> "MonitoringConfig":
        """Create config from environment variables."""
        return cls(
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            enable_wandb=os.getenv("ENABLE_WANDB", "false").lower() == "true",
            wandb_api_key=os.getenv("WANDB_API_KEY"),
            wandb_project=os.getenv("WANDB_PROJECT", "neuromosaic"),
            wandb_entity=os.getenv("WANDB_ENTITY"),
        )


@dataclass
class SecurityConfig:
    """Configuration for security settings."""

    auth_secret_key: Optional[str] = field(default=None)
    encryption_key: Optional[str] = field(default=None)

    @classmethod
    def from_env(cls) -> "SecurityConfig":
        """Create config from environment variables."""
        return cls(
            auth_secret_key=os.getenv("AUTH_SECRET_KEY"),
            encryption_key=os.getenv("ENCRYPTION_KEY"),
        )


@dataclass
class Config:
    """Main configuration class."""

    llm: LLMConfig = field(default_factory=LLMConfig)
    storage: StorageConfig = field(default_factory=StorageConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    container: ContainerConfig = field(default_factory=ContainerConfig)
    monitoring: MonitoringConfig = field(default_factory=MonitoringConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    debug: bool = field(default=False)
    environment: str = field(default="production")

    @classmethod
    def from_env(cls) -> "Config":
        """Create config from environment variables."""
        return cls(
            llm=LLMConfig.from_env(),
            storage=StorageConfig.from_env(),
            database=DatabaseConfig.from_env(),
            container=ContainerConfig.from_env(),
            monitoring=MonitoringConfig.from_env(),
            security=SecurityConfig.from_env(),
            debug=os.getenv("DEBUG", "false").lower() == "true",
            environment=os.getenv("ENVIRONMENT", "production"),
        )


def parse_size(size_str: str) -> int:
    """Parse size string (e.g., '50GB') to bytes."""
    units = {"B": 1, "KB": 1024, "MB": 1024**2, "GB": 1024**3, "TB": 1024**4}

    size_str = size_str.strip().upper()
    for unit, multiplier in units.items():
        if size_str.endswith(unit):
            try:
                number = float(size_str[: -len(unit)])
                return int(number * multiplier)
            except ValueError:
                raise ConfigurationError(f"Invalid size format: {size_str}")

    try:
        return int(size_str)
    except ValueError:
        raise ConfigurationError(f"Invalid size format: {size_str}")


def load_yaml_config(path: Union[str, Path]) -> Dict[str, Any]:
    """Load configuration from YAML file."""
    try:
        with open(path, "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        raise ConfigurationError(f"Failed to load config file: {e}")


def merge_configs(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively merge two configuration dictionaries."""
    result = base.copy()

    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_configs(result[key], value)
        else:
            result[key] = value

    return result


def validate_config(config: Config) -> None:
    """Validate configuration values."""
    # Validate storage configuration
    try:
        parse_size(config.storage.cache_size)
    except ValueError:
        raise ConfigurationError(f"Invalid cache size: {config.storage.cache_size}")

    # Validate container configuration
    try:
        parse_size(config.container.memory_limit)
    except ValueError:
        raise ConfigurationError(
            f"Invalid container memory limit: {config.container.memory_limit}"
        )

    # Validate environment
    valid_environments = {"development", "staging", "production"}
    if config.environment not in valid_environments:
        raise ConfigurationError(
            f"Invalid environment: {config.environment}. "
            f"Must be one of {valid_environments}"
        )

    # Validate log level
    valid_log_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
    if config.monitoring.log_level not in valid_log_levels:
        raise ConfigurationError(
            f"Invalid log level: {config.monitoring.log_level}. "
            f"Must be one of {valid_log_levels}"
        )


def load_config(config_path: Optional[Union[str, Path]] = None) -> Config:
    """
    Load configuration from all sources.

    Args:
        config_path: Optional path to YAML config file

    Returns:
        Loaded configuration object

    Raises:
        ConfigurationError: If configuration is invalid
    """
    # Start with environment-based configuration
    config = Config.from_env()

    # Load and merge YAML configuration if provided
    if config_path is not None:
        yaml_config = load_yaml_config(config_path)
        # TODO: Implement merging of YAML config with env config

    # Validate final configuration
    validate_config(config)

    return config


# Global configuration instance
config: Optional[Config] = None


def get_config() -> Config:
    """Get the global configuration instance."""
    global config
    if config is None:
        config = load_config()
    return config
