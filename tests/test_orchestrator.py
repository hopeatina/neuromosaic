"""
Tests for the orchestrator module.
"""

import pytest
from unittest.mock import Mock, AsyncMock
from typing import Dict, Any

from neuramosaic.orchestrator import Orchestrator
from neuramosaic.arch_space import ArchitectureVector
from neuramosaic.llm_code_gen import CodeGenerator
from neuramosaic.env_manager import ContainerManager


@pytest.fixture
def mock_code_generator() -> Mock:
    """Create a mock code generator."""
    generator = Mock(spec=CodeGenerator)
    generator.generate_code = AsyncMock()
    generator.validate_code = AsyncMock(return_value=True)
    return generator


@pytest.fixture
def mock_container_manager() -> Mock:
    """Create a mock container manager."""
    manager = Mock(spec=ContainerManager)
    manager.create_container = AsyncMock(return_value="container-123")
    manager.run_container = AsyncMock(return_value={"status": "success"})
    manager.cleanup_container = AsyncMock()
    return manager


@pytest.mark.asyncio
async def test_run_cycle(
    config: Dict[str, Any],
    mock_code_generator: Mock,
    mock_container_manager: Mock,
    mock_llm_response: str,
    mock_training_results: Dict[str, float],
):
    """Test running a single search cycle."""
    orchestrator = Orchestrator(config)
    orchestrator._code_generator = mock_code_generator
    orchestrator._container_manager = mock_container_manager

    # Configure mocks
    mock_code_generator.generate_code.return_value = mock_llm_response
    mock_container_manager.run_container.return_value = {
        "status": "success",
        "results": mock_training_results,
    }

    # Run cycle
    result = await orchestrator.run_cycle()

    # Verify interactions
    assert mock_code_generator.generate_code.called
    assert mock_container_manager.create_container.called
    assert mock_container_manager.run_container.called
    assert mock_container_manager.cleanup_container.called

    # Check result structure
    assert "architecture_id" in result
    assert "metrics" in result
    assert "code_version" in result
    assert result["metrics"] == mock_training_results


@pytest.mark.asyncio
async def test_get_next_architecture(config: Dict[str, Any]):
    """Test getting the next architecture to evaluate."""
    orchestrator = Orchestrator(config)

    arch = await orchestrator.get_next_architecture()

    assert isinstance(arch, dict)
    assert "vector" in arch
    assert isinstance(arch["vector"], ArchitectureVector)


@pytest.mark.asyncio
async def test_submit_results(config: Dict[str, Any]):
    """Test submitting results from an experiment."""
    orchestrator = Orchestrator(config)

    results = {
        "architecture_id": "test-123",
        "metrics": {"accuracy": 0.9},
        "code_version": "abc123",
    }

    await orchestrator.submit_results(results)
    # Add assertions based on how results should be stored


@pytest.mark.asyncio
async def test_run_batch_parallel(
    config: Dict[str, Any], mock_code_generator: Mock, mock_container_manager: Mock
):
    """Test running multiple evaluations in parallel."""
    orchestrator = Orchestrator(config)
    orchestrator._code_generator = mock_code_generator
    orchestrator._container_manager = mock_container_manager

    results = await orchestrator.run_batch(batch_size=3, parallel=True)

    assert len(results) == 3
    assert mock_code_generator.generate_code.call_count == 3
    assert mock_container_manager.create_container.call_count == 3


@pytest.mark.asyncio
async def test_error_handling(
    config: Dict[str, Any], mock_code_generator: Mock, mock_container_manager: Mock
):
    """Test handling of various error conditions."""
    orchestrator = Orchestrator(config)
    orchestrator._code_generator = mock_code_generator
    orchestrator._container_manager = mock_container_manager

    # Test code generation failure
    mock_code_generator.generate_code.side_effect = Exception("LLM error")

    with pytest.raises(Exception):
        await orchestrator.run_cycle()

    # Test container failure
    mock_code_generator.generate_code.side_effect = None
    mock_container_manager.run_container.side_effect = Exception("Container error")

    with pytest.raises(Exception):
        await orchestrator.run_cycle()

    # Verify cleanup is called even on failure
    assert mock_container_manager.cleanup_container.called
