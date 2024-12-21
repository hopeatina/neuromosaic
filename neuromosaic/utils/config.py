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
from typing import Any, Dict, Optional, Union, List, TYPE_CHECKING
from dataclasses import dataclass, field, asdict, fields
from dotenv import load_dotenv

from ..arch_space.vector_representation import ArchSpace
from .exceptions import ConfigurationError

# Load environment variables from .env file
load_dotenv()

# Use TYPE_CHECKING for strategy type hints to avoid circular imports
if TYPE_CHECKING:
    from ..orchestrator.strategies.random_strategy import RandomSearch
    from ..orchestrator.strategies.bayesopt_strategy import BayesianOptimization


@dataclass
class BaseConfig:
    """Base configuration class that provides dictionary-style access."""

    def __post_init__(self):
        """Handle any unknown fields by logging warnings."""
        known_fields = {f.name for f in fields(self)}
        for key, value in dict(self.__dict__).items():
            if key not in known_fields:
                logging.warning(
                    f"Unknown configuration field '{key}' for {self.__class__.__name__}, ignoring it"
                )
                delattr(self, key)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value by key, with an optional default.
        Uses dataclasses.asdict() for dictionary-style access.

        Args:
            key: The configuration key to look up
            default: The default value to return if key is not found

        Returns:
            The configuration value if found, otherwise the default value
        """
        try:
            if "." in key:
                section, subkey = key.split(".", 1)
                section_dict = asdict(getattr(self, section))
                return section_dict.get(subkey, default)
            return asdict(self).get(key, default)
        except (AttributeError, TypeError):
            return default


@dataclass
class Training(BaseConfig):
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
class LLMConfig(BaseConfig):
    """Configuration for LLM providers."""

    openai_api_key: Optional[str] = field(default=None)
    anthropic_api_key: Optional[str] = field(default=None)
    cohere_api_key: Optional[str] = field(default=None)
    provider: str = field(default="openai")
    model: str = field(default="gpt-4")
    temperature: float = field(default=0.7)
    max_tokens: int = field(default=2000)
    retry_config: Dict[str, Any] = field(
        default_factory=lambda: {
            "max_retries": 3,
            "initial_wait": 1.0,
            "backoff_factor": 2.0,
        }
    )

    @classmethod
    def from_env(cls) -> "LLMConfig":
        """Create config from environment variables."""
        return cls(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            cohere_api_key=os.getenv("COHERE_API_KEY"),
            provider=os.getenv("LLM_PROVIDER", "openai"),
            model=os.getenv("LLM_MODEL", "gpt-4"),
            temperature=float(os.getenv("LLM_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("LLM_MAX_TOKENS", "2000")),
            retry_config={"max_retries": 3, "initial_wait": 1.0, "backoff_factor": 2.0},
        )

    def __post_init__(self):
        """Validate LLM configuration."""
        if self.provider not in ["openai", "anthropic", "cohere", "llama"]:
            raise ConfigurationError(f"Invalid LLM provider: {self.provider}")
        if self.temperature < 0 or self.temperature > 1:
            raise ConfigurationError(f"Invalid temperature: {self.temperature}")
        if self.max_tokens <= 0:
            raise ConfigurationError(f"Invalid max_tokens: {self.max_tokens}")
        if self.retry_config is None:
            self.retry_config = {
                "max_retries": 3,
                "initial_wait": 1.0,
                "backoff_factor": 2.0,
            }


@dataclass
class StorageConfig(BaseConfig):
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
            artifact_retention_days=30,
        )


@dataclass
class DatabaseConfig(BaseConfig):
    """Configuration for database connection."""

    host: str = field(default="localhost")
    port: int = field(default=5432)
    name: str = field(default="neuromosaic")
    user: str = field(default="postgres")
    password: Optional[str] = field(default=None)
    db_url: str = field(default="sqlite:///neuromosaic.db")
    type: Optional[str] = field(default="sqlite")
    path: Optional[str] = field(default=None)

    @classmethod
    def from_env(cls) -> "DatabaseConfig":
        """Create config from environment variables."""
        return cls(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "5432")),
            name=os.getenv("DB_NAME", "neuromosaic"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD"),
            db_url=os.getenv("DB_URL", "sqlite:///neuromosaic.db"),
            type=os.getenv("DB_TYPE", "sqlite"),
            path=os.getenv("DB_PATH"),
        )

    def __post_init__(self):
        """Validate database configuration."""
        super().__post_init__()
        if self.type == "sqlite" and not self.path and "sqlite:///" not in self.db_url:
            self.path = "neuromosaic.db"
            self.db_url = f"sqlite:///{self.path}"


@dataclass
class ContainerConfig(BaseConfig):
    """Configuration for container runtime."""

    device: str = field(default="cpu")
    memory_limit: str = field(default="8GB")
    num_cpus: int = field(default=4)
    runtime: str = field(default="docker")
    base_image: str = field(default="pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime")
    gpu_support: bool = field(default=True)
    timeout: int = field(default=3600)

    @classmethod
    def from_env(cls) -> "ContainerConfig":
        """Create config from environment variables."""
        return cls(
            device=os.getenv("CONTAINER_DEVICE", "cpu"),
            memory_limit=os.getenv("CONTAINER_MEMORY_LIMIT", "8GB"),
            num_cpus=int(os.getenv("CONTAINER_NUM_CPUS", "4")),
            runtime=os.getenv("CONTAINER_RUNTIME", "docker"),
            base_image=os.getenv(
                "CONTAINER_BASE_IMAGE", "pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime"
            ),
            gpu_support=os.getenv("CONTAINER_GPU_SUPPORT", "true").lower() == "true",
            timeout=int(os.getenv("CONTAINER_TIMEOUT", "3600")),
        )

    def __post_init__(self):
        """Validate container configuration."""
        if self.device not in ["cpu", "gpu"]:
            raise ConfigurationError(f"Invalid device: {self.device}")
        if self.num_cpus <= 0:
            raise ConfigurationError(f"Invalid number of CPUs: {self.num_cpus}")
        if self.runtime not in ["docker", "podman"]:
            raise ConfigurationError(f"Invalid runtime: {self.runtime}")
        try:
            parse_size(self.memory_limit)
        except ValueError:
            raise ConfigurationError(f"Invalid memory limit: {self.memory_limit}")


@dataclass
class MonitoringConfig(BaseConfig):
    """Configuration for monitoring and logging."""

    log_level: str = field(default="INFO")
    enable_wandb: bool = field(default=False)
    wandb_api_key: Optional[str] = field(default=None)
    wandb_project: str = field(default="neuromosaic")
    wandb_entity: Optional[str] = field(default=None)
    handlers: List[Dict[str, str]] = field(
        default_factory=lambda: [
            {
                "type": "file",
                "file": "neuromosaic.log",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
            {"type": "console", "format": "%(levelname)s: %(message)s"},
        ]
    )

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
class SecurityConfig(BaseConfig):
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
class Config(BaseConfig):
    """Main configuration class."""

    llm: LLMConfig = field(default_factory=LLMConfig)
    storage: StorageConfig = field(default_factory=StorageConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    container: ContainerConfig = field(default_factory=ContainerConfig)
    monitoring: MonitoringConfig = field(default_factory=MonitoringConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    debug: bool = field(default=False)
    environment: str = field(default="production")
    arch_space: Dict[str, Any] = field(
        default_factory=lambda: {
            "dimensions": 64,
            "bounds": {
                "num_layers": [2, 12],
                "hidden_size": [128, 1024],
                "num_heads": [4, 16],
                "ffn_ratio": [2.0, 8.0],
            },
            "categorical_dims": {
                "ffn_type": ["vanilla", "gated", "expert"],
                "attention_type": ["vanilla", "linear", "sparse"],
                "norm_type": ["layer", "rmsnorm"],
                "activation": ["relu", "gelu", "swish"],
            },
        }
    )
    search_strategy: Dict[str, Any] = field(
        default_factory=lambda: {
            "type": "bayesian_optimization",
            "acquisition_function": "expected_improvement",
            "kernel": "matern",
            "length_scale": 1.0,
            "exploration_weight": 0.1,
            "num_random_init": 10,
        }
    )
    training: Training = field(default_factory=Training)
    wandb: Dict[str, Any] = field(
        default_factory=lambda: {
            "enabled": True,
            "project": "neuromosaic",
            "entity": None,
            "tags": [],
        }
    )

    def __post_init__(self):
        """Initialize with environment variables if not already set."""
        if not self.llm.openai_api_key:
            self.llm = LLMConfig.from_env()

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
            search_strategy={
                "dimensions": 64,
                "num_trials": 10,
                "type": "bayesian_optimization",
                "kernel": "matern",
                "length_scale": 1.0,
                "acquisition_function": "expected_improvement",
                "exploration_weight": 0.1,
            },
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
                # Merge with environment variables
                env_llm = LLMConfig.from_env()
                yaml_config["llm"]["openai_api_key"] = (
                    yaml_config["llm"].get("openai_api_key") or env_llm.openai_api_key
                )
                yaml_config["llm"]["anthropic_api_key"] = (
                    yaml_config["llm"].get("anthropic_api_key")
                    or env_llm.anthropic_api_key
                )
                yaml_config["llm"]["cohere_api_key"] = (
                    yaml_config["llm"].get("cohere_api_key") or env_llm.cohere_api_key
                )
                self.llm = LLMConfig(**yaml_config["llm"])
            else:
                # If no LLM config in YAML, use environment variables
                self.llm = LLMConfig.from_env()
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
                # Store as dict, let orchestrator handle instantiation
                self.search_strategy = yaml_config["search_strategy"]
                # Ensure required fields
                if "type" not in self.search_strategy:
                    self.search_strategy["type"] = "bayesian_optimization"
                if "dimensions" not in self.search_strategy:
                    self.search_strategy["dimensions"] = 64

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
    print(size_str)
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
    if TYPE_CHECKING:
        from ..orchestrator.strategies.random_strategy import RandomSearch
        from ..orchestrator.strategies.bayesopt_strategy import BayesianOptimization

    if not (
        isinstance(config.search_strategy, dict)
        or isinstance(config.search_strategy, (RandomSearch, BayesianOptimization))
    ):
        raise ConfigurationError("Invalid search_strategy configuration")

    # If dict, validate required fields
    if isinstance(config.search_strategy, dict):
        required_fields = ["dimensions", "type"]
        for field in required_fields:
            if field not in config.search_strategy:
                raise ConfigurationError(
                    f"Missing required field in search_strategy: {field}"
                )

        valid_types = {"random", "bayesian_optimization"}
        if config.search_strategy["type"] not in valid_types:
            raise ConfigurationError(
                f"Invalid search strategy type: {config.search_strategy['type']}. "
                f"Must be one of {valid_types}"
            )

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
