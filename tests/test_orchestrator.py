"""
Tests for the orchestrator module.
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch, PropertyMock
from typing import Dict, Any
from dataclasses import dataclass

from neuromosaic.orchestrator import Orchestrator
from neuromosaic.arch_space import ArchitectureVector
from neuromosaic.llm_code_gen import CodeGenerator
from neuromosaic.env_manager import ContainerManager


@dataclass
class Config:
    """Test configuration class."""

    def __init__(self, config_dict: Dict[str, Any]):
        self._config = config_dict


@pytest.fixture
def mock_version_control() -> Mock:
    """Create a mock version control."""
    vc = Mock()
    vc.commit_code = AsyncMock(return_value="abc123")
    return vc


@pytest.fixture
def mock_results_db() -> Mock:
    """Create a mock results database."""
    db = Mock()
    db.save_run_info = AsyncMock()
    return db


@pytest.fixture
def mock_arch_vector() -> Mock:
    """Create a mock architecture vector."""
    vector = Mock(spec=ArchitectureVector)
    vector.decode = Mock(
        return_value={
            "layers": [
                {"type": "linear", "units": 128},
                {"type": "relu"},
                {"type": "linear", "units": 10},
            ]
        }
    )
    return vector


@pytest.fixture
def mock_search_strategy(mock_arch_vector: Mock) -> Mock:
    """Create a mock search strategy."""
    strategy = Mock()
    strategy.suggest_architecture = AsyncMock(return_value=mock_arch_vector)
    strategy.update_with_results = AsyncMock()
    # Add history property that supports len()
    type(strategy).history = PropertyMock(return_value=[])
    return strategy


@pytest.fixture
def config() -> Config:
    """Create a test configuration."""
    return Config(
        {
            "llm": {"provider": "openai", "api_key": "test-key", "model": "gpt-4"},
            "search_strategy": {
                "type": "random",
                "params": {"population_size": 10, "mutation_rate": 0.1},
            },
            "container": {
                "runtime": "docker",
                "image": "python:3.9",
                "gpu": False,
                "memory_limit": "4g",
            },
        }
    )


@pytest.fixture
def mock_code_generator() -> Mock:
    """Create a mock code generator."""
    generator = Mock(spec=CodeGenerator)
    generator.generate_code = AsyncMock(return_value="mock code")
    generator.validate_code = AsyncMock(return_value=True)
    return generator


@pytest.fixture
def mock_container_manager() -> Mock:
    """Create a mock container manager."""
    manager = Mock(spec=ContainerManager)
    manager.create_container = AsyncMock(return_value="container-123")
    manager.run_container = AsyncMock(
        return_value={
            "status": "success",
            "results": {
                "accuracy": 0.85,
                "latency": 45.6,
                "loss": 0.32,
                "memory_usage": 1024.0,
            },
        }
    )
    manager.cleanup_container = AsyncMock()
    return manager


@pytest.fixture
def mock_llm_response() -> str:
    """Create a mock LLM response with model code."""
    return """
import torch
import torch.nn as nn

class GeneratedModel(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.layers = nn.ModuleList([
            nn.Linear(config["input_size"], 128),
            nn.ReLU(),
            nn.Linear(128, config["output_size"])
        ])
        
    def forward(self, x):
        for layer in self.layers:
            x = layer(x)
        return x
"""


@pytest.fixture
def mock_training_results() -> Dict[str, float]:
    """Create mock training results."""
    return {"accuracy": 0.85, "latency": 45.6, "loss": 0.32, "memory_usage": 1024.0}


@pytest.mark.asyncio
async def test_run_cycle(
    config: Config,
    mock_code_generator: Mock,
    mock_container_manager: Mock,
    mock_version_control: Mock,
    mock_results_db: Mock,
    mock_search_strategy: Mock,
    mock_llm_response: str,
    mock_training_results: Dict[str, float],
):
    """Test running a single search cycle."""
    # Configure mocks
    mock_code_generator.generate_code.return_value = mock_llm_response
    mock_container_manager.run_container.return_value = {
        "status": "success",
        "results": mock_training_results,
    }

    # Create orchestrator with mocked components
    with patch(
        "neuromosaic.llm_code_gen.providers.OpenAICodeGenerator"
    ) as mock_gen_cls, patch(
        "neuromosaic.env_manager.providers.DockerContainerManager"
    ) as mock_container_cls:
        mock_gen_cls.return_value = mock_code_generator
        mock_container_cls.return_value = mock_container_manager

        orchestrator = Orchestrator(config)
        orchestrator.code_generator = mock_code_generator
        orchestrator.container_manager = mock_container_manager
        orchestrator._version_control = mock_version_control
        orchestrator._results_db = mock_results_db
        orchestrator._search_strategy = mock_search_strategy

        # Run cycle
        result = await orchestrator.run_cycle()

    # Verify interactions
    assert mock_code_generator.generate_code.called
    assert mock_container_manager.create_container.called
    assert mock_container_manager.run_container.called
    assert mock_container_manager.cleanup_container.called
    assert mock_version_control.commit_code.called
    assert mock_results_db.save_run_info.called

    # Check result structure
    assert "architecture_id" in result
    assert "metrics" in result
    assert "code_version" in result
    assert result["metrics"] == mock_training_results


@pytest.mark.asyncio
async def test_get_next_architecture(
    config: Config,
    mock_code_generator: Mock,
    mock_container_manager: Mock,
    mock_search_strategy: Mock,
):
    """Test getting the next architecture to evaluate."""
    with patch(
        "neuromosaic.llm_code_gen.providers.OpenAICodeGenerator"
    ) as mock_gen_cls, patch(
        "neuromosaic.env_manager.providers.DockerContainerManager"
    ) as mock_container_cls:
        mock_gen_cls.return_value = mock_code_generator
        mock_container_cls.return_value = mock_container_manager

        orchestrator = Orchestrator(config)
        orchestrator.code_generator = mock_code_generator
        orchestrator.container_manager = mock_container_manager
        orchestrator._search_strategy = mock_search_strategy

        arch = await orchestrator.get_next_architecture()

    assert isinstance(arch, dict)
    assert "vector" in arch
    assert mock_search_strategy.suggest_architecture.called
    assert isinstance(arch["metadata"], dict)
    assert "strategy" in arch["metadata"]
    assert "iteration" in arch["metadata"]


@pytest.mark.asyncio
async def test_submit_results(
    config: Config,
    mock_code_generator: Mock,
    mock_container_manager: Mock,
    mock_results_db: Mock,
    mock_search_strategy: Mock,
):
    """Test submitting results from an experiment."""
    with patch(
        "neuromosaic.llm_code_gen.providers.OpenAICodeGenerator"
    ) as mock_gen_cls, patch(
        "neuromosaic.env_manager.providers.DockerContainerManager"
    ) as mock_container_cls:
        mock_gen_cls.return_value = mock_code_generator
        mock_container_cls.return_value = mock_container_manager

        orchestrator = Orchestrator(config)
        orchestrator.code_generator = mock_code_generator
        orchestrator.container_manager = mock_container_manager
        orchestrator._results_db = mock_results_db
        orchestrator._search_strategy = mock_search_strategy

        results = {
            "architecture_id": "test-123",
            "metrics": {"accuracy": 0.9},
            "code_version": "abc123",
        }

        await orchestrator.submit_results(results)

        # Verify results were stored and strategy updated
        mock_results_db.save_run_info.assert_called_once_with(results)
        mock_search_strategy.update_with_results.assert_called_once_with(results)


@pytest.mark.asyncio
async def test_run_batch_parallel(
    config: Config,
    mock_code_generator: Mock,
    mock_container_manager: Mock,
    mock_version_control: Mock,
    mock_results_db: Mock,
    mock_search_strategy: Mock,
):
    """Test running multiple evaluations in parallel."""
    with patch(
        "neuromosaic.llm_code_gen.providers.OpenAICodeGenerator"
    ) as mock_gen_cls, patch(
        "neuromosaic.env_manager.providers.DockerContainerManager"
    ) as mock_container_cls:
        mock_gen_cls.return_value = mock_code_generator
        mock_container_cls.return_value = mock_container_manager

        orchestrator = Orchestrator(config)
        orchestrator.code_generator = mock_code_generator
        orchestrator.container_manager = mock_container_manager
        orchestrator._version_control = mock_version_control
        orchestrator._results_db = mock_results_db
        orchestrator._search_strategy = mock_search_strategy

        results = await orchestrator.run_batch(batch_size=3, parallel=True)

    assert len(results) == 3
    assert all(isinstance(r, dict) for r in results)
    assert mock_code_generator.generate_code.call_count == 3
    assert mock_container_manager.create_container.call_count == 3
    assert mock_container_manager.cleanup_container.call_count == 3


@pytest.mark.asyncio
async def test_error_handling(
    config: Config,
    mock_code_generator: Mock,
    mock_container_manager: Mock,
    mock_version_control: Mock,
    mock_results_db: Mock,
    mock_search_strategy: Mock,
):
    """Test handling of various error conditions."""
    with patch(
        "neuromosaic.llm_code_gen.providers.OpenAICodeGenerator"
    ) as mock_gen_cls, patch(
        "neuromosaic.env_manager.providers.DockerContainerManager"
    ) as mock_container_cls:
        mock_gen_cls.return_value = mock_code_generator
        mock_container_cls.return_value = mock_container_manager

        orchestrator = Orchestrator(config)
        orchestrator.code_generator = mock_code_generator
        orchestrator.container_manager = mock_container_manager
        orchestrator._version_control = mock_version_control
        orchestrator._results_db = mock_results_db
        orchestrator._search_strategy = mock_search_strategy

        # Test code generation failure
        mock_code_generator.generate_code.side_effect = Exception("LLM error")

        with pytest.raises(Exception):
            await orchestrator.run_cycle()

        # Test container failure
        mock_code_generator.generate_code.side_effect = None
        mock_container_manager.create_container.return_value = "container-123"
        mock_container_manager.run_container.side_effect = Exception("Container error")

        with pytest.raises(Exception):
            await orchestrator.run_cycle()

        # Verify cleanup is called even on failure
        assert mock_container_manager.cleanup_container.called
