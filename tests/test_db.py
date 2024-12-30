"""Tests for the results database implementation."""

import pytest
import json
from datetime import datetime, timedelta
from typing import Dict, Any

from neuromosaic.results_db.db import ResultsDB
from neuromosaic.results_db.models import Base

pytestmark = pytest.mark.asyncio  # Mark all tests in this module as async tests


@pytest.fixture
def db_config() -> Dict[str, Any]:
    """Create a test database configuration."""
    return {"database": {"db_url": "sqlite:///test_results.db"}}


@pytest.fixture
async def db(db_config: Dict[str, Any]) -> ResultsDB:
    """Create a test database instance."""
    db = ResultsDB(db_config)
    yield db
    # Cleanup: Drop all tables after tests
    Base.metadata.drop_all(db.engine)


@pytest.fixture
async def sample_experiment(db: ResultsDB) -> str:
    """Create a sample experiment and return its ID."""
    config = {"batch_size": 32, "learning_rate": 0.001}
    exp_id = await db.create_experiment("Test Experiment", "Test Description", config)
    return exp_id


@pytest.fixture
async def sample_architecture(db: ResultsDB) -> str:
    """Create a sample architecture and return its ID."""
    run_info = {
        "architecture_id": "test_arch_1",
        "arch_spec": {"layers": [64, 32, 16]},
        "code_commit": "abc123",
        "metrics": {"accuracy": 0.95},
        "experiment_id": None,
    }
    await db.save_run_info(run_info)
    return "test_arch_1"


async def test_create_experiment(db: ResultsDB):
    """Test creating an experiment."""
    config = {"batch_size": 32, "learning_rate": 0.001}
    exp_id = await db.create_experiment("Test Experiment", "Test Description", config)

    details = await db.get_experiment_details(exp_id)
    assert details is not None
    assert details["status"] == "created"
    assert "Test Experiment" in details["config"]["name"]


async def test_update_experiment_status(db: ResultsDB, sample_experiment: str):
    """Test updating experiment status."""
    await db.update_experiment_status(sample_experiment, "running")
    details = await db.get_experiment_details(sample_experiment)
    assert details["status"] == "running"

    # Test completing experiment
    await db.update_experiment_status(sample_experiment, "completed")
    details = await db.get_experiment_details(sample_experiment)
    assert details["status"] == "completed"
    assert details["end_time"] is not None


async def test_save_and_list_runs(db: ResultsDB, sample_experiment: str):
    """Test saving and listing runs."""
    # Create multiple runs
    run_infos = [
        {
            "architecture_id": f"arch_{i}",
            "experiment_id": sample_experiment,
            "metrics": {"accuracy": 0.8 + i * 0.05},
            "arch_spec": {"layers": [32, 16]},
            "code_commit": f"commit_{i}",
        }
        for i in range(3)
    ]

    for run_info in run_infos:
        await db.save_run_info(run_info)

    # List all runs
    runs = await db.list_all_runs()
    assert len(runs) == 3

    # Test filtering by experiment
    filtered_runs = await db.list_all_runs(experiment_id=sample_experiment)
    assert len(filtered_runs) == 3

    # Test date filtering
    tomorrow = (datetime.now() + timedelta(days=1)).isoformat()
    future_runs = await db.list_all_runs(start_date=tomorrow)
    assert len(future_runs) == 0


async def test_get_best_architectures(db: ResultsDB, sample_experiment: str):
    """Test getting best architectures based on metrics."""
    # Create runs with different metrics
    run_infos = [
        {
            "architecture_id": f"arch_{i}",
            "experiment_id": sample_experiment,
            "metrics": {"accuracy": 0.8 + i * 0.05},
            "arch_spec": {"layers": [32, 16]},
            "code_commit": f"commit_{i}",
        }
        for i in range(5)
    ]

    for run_info in run_infos:
        await db.save_run_info(run_info)

    # Get best architectures
    best = await db.get_best_architectures("accuracy", limit=2)
    assert len(best) == 2
    assert best[0]["metrics"]["accuracy"] > best[1]["metrics"]["accuracy"]


async def test_delete_experiment(db: ResultsDB, sample_experiment: str):
    """Test deleting an experiment."""
    # First verify it exists
    assert await db.get_experiment_details(sample_experiment) is not None

    # Delete it
    success = await db.delete_experiment(sample_experiment)
    assert success is True

    # Verify it's gone
    assert await db.get_experiment_details(sample_experiment) is None


async def test_get_architecture(db: ResultsDB, sample_architecture: str):
    """Test getting architecture details."""
    arch = await db.get_architecture(sample_architecture)
    assert arch is not None
    assert arch["id"] == sample_architecture
    assert "layers" in arch["arch_spec"]
    assert arch["code_commit"] == "abc123"


async def test_list_architectures(db: ResultsDB, sample_architecture: str):
    """Test listing architectures with pagination."""
    # Create additional architectures
    for i in range(3):
        run_info = {
            "architecture_id": f"arch_{i}",
            "arch_spec": {"layers": [32, 16]},
            "code_commit": f"commit_{i}",
            "metrics": {"accuracy": 0.9},
            "experiment_id": None,
        }
        await db.save_run_info(run_info)

    # Test pagination
    archs = await db.list_architectures(skip=0, limit=2)
    assert len(archs) == 2

    all_archs = await db.list_architectures(skip=0, limit=100)
    assert len(all_archs) == 4  # 3 new + 1 from fixture


async def test_get_metrics(db: ResultsDB, sample_experiment: str):
    """Test getting metrics with filtering."""
    # Create runs with metrics
    run_infos = [
        {
            "architecture_id": f"arch_{i}",
            "experiment_id": sample_experiment,
            "metrics": {"accuracy": 0.8 + i * 0.05, "loss": 0.5 - i * 0.1},
            "arch_spec": {"layers": [32, 16]},
            "code_commit": f"commit_{i}",
        }
        for i in range(3)
    ]

    for run_info in run_infos:
        await db.save_run_info(run_info)

    # Get all metrics
    metrics = await db.get_metrics(experiment_id=sample_experiment)
    assert len(metrics) == 3

    # Get specific metrics
    specific_metrics = await db.get_metrics(
        experiment_id=sample_experiment, metric_names=["accuracy"]
    )
    assert len(specific_metrics) == 3
    assert all("loss" not in m["metrics"] for m in specific_metrics)
    assert all("accuracy" in m["metrics"] for m in specific_metrics)


async def test_error_handling(db: ResultsDB):
    """Test error handling for various scenarios."""
    # Test non-existent experiment
    assert await db.get_experiment_details("non_existent") is None

    # Test updating non-existent experiment
    await db.update_experiment_status(
        "non_existent", "running"
    )  # Should not raise error

    # Test deleting non-existent experiment
    assert await db.delete_experiment("non_existent") is False

    # Test invalid metric name
    best = await db.get_best_architectures("non_existent_metric")
    assert len(best) == 0
