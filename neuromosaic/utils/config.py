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
from typing import Any, Dict, Optional, Union, List
from dataclasses import dataclass, field
from dotenv import load_dotenv

from ..arch_space.vector_representation import ArchSpace
from ..orchestrator.strategies.random_strategy import RandomSearch
from ..orchestrator.strategies.bayesopt_strategy import BayesianOptimization
from .exceptions import ConfigurationError

# Load environment variables from .env file
load_dotenv()


@dataclass
class Training:
    """Configuration for model training."""

    batch_size: int = field(default=32)
    max_epochs: int = field(default=10)
    learning_rate: float = field(default=0.001)
    optimizer: str = field(default="adam")
    scheduler: str = field(default="cosine")
    metrics: List[str] = field(
        default_factory=lambda: ["accuracy", "loss", "latency", "memory_usage"]
    )

    def __post_init__(self):
        """Validate training configuration."""
        if self.batch_size <= 0:
            raise ConfigurationError(f"Invalid batch size: {self.batch_size}")
        if self.max_epochs <= 0:
            raise ConfigurationError(f"Invalid max epochs: {self.max_epochs}")
        if self.learning_rate <= 0:
            raise ConfigurationError(f"Invalid learning rate: {self.learning_rate}")
        if self.optimizer not in ["adam", "sgd", "adamw"]:
            raise ConfigurationError(f"Invalid optimizer: {self.optimizer}")
        if self.scheduler not in ["cosine", "linear", "step", "none"]:
            raise ConfigurationError(f"Invalid scheduler: {self.scheduler}")


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
    """Configuration for container runtime."""

    device: str = field(default="cpu")
    memory_limit: str = field(default="8GB")
    num_cpus: int = field(default=4)

    @classmethod
    def from_env(cls) -> "ContainerConfig":
        """Create config from environment variables."""
        return cls(
            device=os.getenv("CONTAINER_DEVICE", "cpu"),
            memory_limit=os.getenv("CONTAINER_MEMORY_LIMIT", "8GB"),
            num_cpus=int(os.getenv("CONTAINER_NUM_CPUS", "4")),
        )

    def __post_init__(self):
        """Validate container configuration."""
        if self.device not in ["cpu", "gpu"]:
            raise ConfigurationError(f"Invalid device: {self.device}")
        if self.num_cpus <= 0:
            raise ConfigurationError(f"Invalid number of CPUs: {self.num_cpus}")
        try:
            parse_size(self.memory_limit)
        except ValueError:
            raise ConfigurationError(f"Invalid memory limit: {self.memory_limit}")


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
    arch_space: ArchSpace = field(default_factory=ArchSpace)
    search_strategy: Union[RandomSearch, BayesianOptimization] = field(
        default_factory=lambda: BayesianOptimization(
            {
                "dimensions": 64,
                "num_trials": 10,
                "type": "bayesian_optimization",
                "kernel": "matern",
                "length_scale": 1.0,
                "acquisition_function": "expected_improvement",
                "exploration_weight": 0.1,
            }
        )
    )
    training: Training = field(default_factory=Training)

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
            arch_space=ArchSpace(),
            search_strategy=BayesianOptimization(
                {
                    "dimensions": 64,
                    "num_trials": 10,
                    "type": "bayesian_optimization",
                    "kernel": "matern",
                    "length_scale": 1.0,
                    "acquisition_function": "expected_improvement",
                    "exploration_weight": 0.1,
                }
            ),
            training=Training(),
        )

    def load_config(self, config_path: Union[str, Path]) -> None:
        """
        Load configuration from a YAML file and merge with current config.

        Args:
            config_path: Path to YAML configuration file

        Raises:
            ConfigurationError: If configuration file is invalid or cannot be loaded
        """
        try:
            yaml_config = load_yaml_config(config_path)

            # Update each config section if present in YAML
            if "llm" in yaml_config:
                self.llm = LLMConfig(**yaml_config["llm"])
            if "storage" in yaml_config:
                self.storage = StorageConfig(**yaml_config["storage"])
            if "database" in yaml_config:
                self.database = DatabaseConfig(**yaml_config["database"])
            if "container" in yaml_config:
                self.container = ContainerConfig(**yaml_config["container"])
            if "monitoring" in yaml_config:
                self.monitoring = MonitoringConfig(**yaml_config["monitoring"])
            if "security" in yaml_config:
                self.security = SecurityConfig(**yaml_config["security"])
            if "arch_space" in yaml_config:
                self.arch_space = ArchSpace(**yaml_config["arch_space"])
            if "search_strategy" in yaml_config:
                strategy_config = yaml_config["search_strategy"]
                strategy_type = strategy_config.get("type", "bayesian_optimization")
                # Ensure dimensions is set
                if "dimensions" not in strategy_config:
                    strategy_config["dimensions"] = 64

                # Add default values for bayesian optimization
                if strategy_type == "bayesian_optimization":
                    defaults = {
                        "kernel": "matern",
                        "length_scale": 1.0,
                        "acquisition_function": "expected_improvement",
                        "exploration_weight": 0.1,
                    }
                    for key, value in defaults.items():
                        if key not in strategy_config:
                            strategy_config[key] = value

                if strategy_type == "random":
                    self.search_strategy = RandomSearch(strategy_config)
                elif strategy_type == "bayesian_optimization":
                    self.search_strategy = BayesianOptimization(strategy_config)
                else:
                    raise ConfigurationError(
                        f"Unsupported search strategy type: {strategy_type}"
                    )
            if "training" in yaml_config:
                self.training = Training(**yaml_config["training"])

            # Update simple fields
            self.debug = yaml_config.get("debug", self.debug)
            self.environment = yaml_config.get("environment", self.environment)

            # Validate the final configuration
            validate_config(self)

        except Exception as e:
            raise ConfigurationError(f"Failed to load configuration: {e}")


def parse_size(size_str: str) -> int:
    """Parse size string (e.g., '50GB' or '50G') to bytes."""
    # Support both full units and single letter units
    units = {
        "TB": 1024**4,
        "T": 1024**4,
        "GB": 1024**3,
        "G": 1024**3,
        "MB": 1024**2,
        "M": 1024**2,
        "KB": 1024,
        "K": 1024,
        "B": 1,
    }

    size_str = size_str.strip().upper()

    # Try to find the unit by checking each unit in order (longest first)
    for unit, multiplier in units.items():
        if size_str.endswith(unit):
            try:
                # Extract the number part by removing the unit
                number_str = size_str[: -len(unit)].strip()
                number = float(number_str)
                return int(number * multiplier)
            except ValueError:
                continue

    # If no unit is found or parsing failed, try to parse as raw bytes
    try:
        return int(size_str)
    except ValueError:
        raise ConfigurationError(
            f"Invalid size format: {size_str}. Expected format: NUMBER[T|TB|G|GB|M|MB|K|KB|B]"
        )


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

    # Validate arch_space configuration
    if not isinstance(config.arch_space, ArchSpace):
        raise ConfigurationError("Invalid arch_space configuration")

    # Validate search_strategy configuration
    if not isinstance(config.search_strategy, (RandomSearch, BayesianOptimization)):
        raise ConfigurationError("Invalid search_strategy configuration")

    # Validate training configuration
    if not isinstance(config.training, Training):
        raise ConfigurationError("Invalid training configuration")
    try:
        config.training.__post_init__()
    except ConfigurationError as e:
        raise ConfigurationError(f"Training configuration validation failed: {e}")


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
