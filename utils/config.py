"""
Global configuration management utilities.
"""

from typing import Dict, Any, Optional
import yaml
from pathlib import Path


class Config:
    """
    Global configuration manager implementing the singleton pattern.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._config = {}
        self._initialized = True

    def load_config(self, config_path: str) -> None:
        """Load configuration from a YAML file."""
        with open(config_path, "r") as f:
            self._config = yaml.safe_load(f)

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        self._config[key] = value
