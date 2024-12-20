"""
Pytest configuration and fixtures.

This module provides common fixtures and configuration for all tests.
"""

import os
import pytest
import tempfile
from pathlib import Path
from typing import Dict, Any, Generator

from neuromosaic.utils.config import Config


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Provide a temporary directory that is cleaned up after the test."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def test_config() -> Dict[str, Any]:
    """Provide a test configuration."""
    return {
        "arch_space": {
            "dimensions": 8,
            "bounds": {"num_layers": [2, 4], "hidden_size": [64, 128]},
        },
        "search_strategy": {"type": "random", "num_samples": 10},
        "llm": {"provider": "mock", "temperature": 0.7},
        "container": {"runtime": "mock", "memory_limit": "1g"},
        "training": {"batch_size": 8, "max_epochs": 2},
        "database": {"type": "sqlite", "path": ":memory:"},
    }


@pytest.fixture
def config(test_config: Dict[str, Any], temp_dir: Path) -> Config:
    """Provide an initialized Config instance."""
    config = Config()
    config._config = test_config
    return config


@pytest.fixture
def mock_llm_response() -> str:
    """Provide a mock LLM-generated code response."""
    return """
import torch
import torch.nn as nn

class GeneratedModel(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.layers = nn.ModuleList([
            nn.Linear(64, 64) for _ in range(4)
        ])
        
    def forward(self, x):
        for layer in self.layers:
            x = layer(x)
        return x
"""


@pytest.fixture
def mock_training_results() -> Dict[str, float]:
    """Provide mock training results."""
    return {"accuracy": 0.85, "loss": 0.32, "latency": 45.6, "memory_usage": 1024.0}


@pytest.fixture(autouse=True)
def setup_environment(temp_dir: Path) -> None:
    """Set up environment variables for testing."""
    os.environ["NEURAMOSAIC_TEST"] = "1"
    os.environ["NEURAMOSAIC_HOME"] = str(temp_dir)
