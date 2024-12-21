"""Tests for the Neuromosaic CLI."""

import pytest
from click.testing import CliRunner
from pathlib import Path
import yaml
import json
from unittest.mock import patch, Mock, AsyncMock, MagicMock
from dataclasses import asdict

from neuromosaic.cli import cli
from neuromosaic.utils.config import (
    Config,
    LLMConfig,
    StorageConfig,
    DatabaseConfig,
    ContainerConfig,
    MonitoringConfig,
    SecurityConfig,
    ArchSpace,
)
from neuromosaic.orchestrator import Orchestrator


@pytest.fixture
def default_config():
    """Create a default config for testing."""
    return Config(
        environment="development",
        llm=LLMConfig(
            provider="openai",
            model="gpt-4",
            temperature=0.7,
            max_tokens=2000,
            retry_config={
                "max_retries": 3,
                "initial_wait": 1.0,
                "backoff_factor": 2.0,
            },
        ),
        storage=StorageConfig(
            root=Path("data"),
            cache_size="50GB",
            artifact_retention_days=30,
        ),
        database=DatabaseConfig(
            db_url="sqlite:///results.db",
            type="sqlite",
            path="results.db",
        ),
        container=ContainerConfig(
            device="cpu",
            memory_limit="8GB",
            num_cpus=4,
            runtime="docker",
            base_image="pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime",
            gpu_support=True,
            timeout=3600,
        ),
        arch_space=ArchSpace(
            dimensions=64,
            bounds={
                "num_layers": [2, 12],
                "hidden_size": [128, 1024],
                "num_heads": [4, 16],
                "ffn_ratio": [2.0, 8.0],
            },
            categorical_dims={
                "ffn_type": ["vanilla", "gated", "expert"],
                "attention_type": ["vanilla", "linear", "sparse"],
                "norm_type": ["layer", "rmsnorm"],
                "activation": ["relu", "gelu", "swish"],
            },
        ),
        search_strategy={
            "type": "bayesian_optimization",
            "dimensions": 64,
            "acquisition_function": "expected_improvement",
            "kernel": "matern",
            "length_scale": 1.0,
            "exploration_weight": 0.1,
            "num_random_init": 10,
        },
    )


@pytest.fixture
def minimal_config(tmp_path):
    """Create a minimal config for testing."""
    return Config(
        environment="development",
        llm=LLMConfig(
            provider="openai",
            model="gpt-4",
            temperature=0.7,
            max_tokens=2000,
        ),
        storage=StorageConfig(
            root=Path("data"),
            cache_size="50GB",
        ),
        database=DatabaseConfig(
            db_url=f"sqlite:///{tmp_path}/results.db",
            type="sqlite",
            path="results.db",
        ),
        container=ContainerConfig(
            device="cpu",
            memory_limit="8GB",
        ),
        search_strategy={
            "type": "bayesian_optimization",
            "dimensions": 64,
            "kernel": "matern",
            "length_scale": 1.0,
            "acquisition_function": "expected_improvement",
            "exploration_weight": 0.1,
        },
    )


@pytest.fixture
def config_dict(tmp_path):
    """Create a config dictionary for testing."""
    return {
        "environment": "development",
        "llm": {
            "provider": "openai",
            "model": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 2000,
            "retry_config": {
                "max_retries": 3,
                "initial_wait": 1.0,
                "backoff_factor": 2.0,
            },
        },
        "storage": {
            "root": str(Path("data")),
            "cache_size": "50GB",
            "artifact_retention_days": 30,
        },
        "database": {
            "db_url": f"sqlite:///{tmp_path}/results.db",
            "type": "sqlite",
            "path": "results.db",
        },
        "container": {
            "device": "cpu",
            "memory_limit": "8GB",
            "num_cpus": 4,
            "runtime": "docker",
            "base_image": "pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime",
            "gpu_support": True,
            "timeout": 3600,
        },
        "arch_space": {
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
        },
        "search_strategy": {
            "type": "bayesian_optimization",
            "dimensions": 64,
            "acquisition_function": "expected_improvement",
            "kernel": "matern",
            "length_scale": 1.0,
            "exploration_weight": 0.1,
            "num_random_init": 10,
        },
    }


@pytest.fixture
def mock_multiprocessing():
    """Mock multiprocessing Process."""
    with patch("multiprocessing.Process") as mock_process:
        mock_instance = MagicMock()
        mock_process.return_value = mock_instance
        yield mock_process


@pytest.fixture
def mock_uvicorn():
    """Mock uvicorn run."""
    with patch("uvicorn.run") as mock:
        yield mock


@pytest.fixture
def mock_dashboard():
    """Mock dashboard run."""
    with patch("neuromosaic.frontend.dashboard.run_dashboard") as mock:
        yield mock


@pytest.fixture
def runner():
    """Create a CLI runner for testing."""
    return CliRunner(mix_stderr=False)  # Capture stderr separately


@pytest.fixture
def mock_orchestrator():
    """Mock the Orchestrator class."""
    mock = MagicMock()
    # Create a mock that returns a completed future with proper metrics
    mock_coro = AsyncMock()
    mock_coro.return_value = [
        {
            "id": "test_arch_1",
            "metrics": {"accuracy": 0.95, "latency": 10.5},
            "config": {"layers": 4},
            "status": "completed",
        },
        {
            "id": "test_arch_2",
            "metrics": {"accuracy": 0.85, "latency": 8.5},
            "config": {"layers": 3},
            "status": "completed",
        },
    ]
    mock.return_value.run_batch = mock_coro
    return mock


@pytest.fixture
def mock_failed_orchestrator():
    """Mock the Orchestrator class with failed results."""
    mock = MagicMock()
    mock_coro = AsyncMock()
    mock_coro.return_value = [
        {"id": "test_arch_1", "error": "API key invalid", "status": "failed"}
    ]
    mock.return_value.run_batch = mock_coro
    return mock


@pytest.fixture
def mock_results_db():
    """Mock the ResultsDB class."""
    with patch("neuromosaic.cli.ResultsDB") as mock:
        mock.return_value.get_run_info.return_value = {
            "id": "test_arch_1",
            "metrics": {"accuracy": 0.95, "latency": 10.5},
            "code_version": "1.0.0",
            "code": "def model(): pass",
        }
        mock.return_value.load_results.return_value = [
            {"id": "test_1", "metrics": {"accuracy": 0.9}},
            {"id": "test_2", "metrics": {"accuracy": 0.85}},
        ]
        yield mock


@pytest.fixture
def mock_analysis():
    """Mock analysis functions."""
    with patch("neuromosaic.cli.analyze_results") as analyze_mock, patch(
        "neuromosaic.cli.display_detailed_metrics"
    ) as display_mock, patch("neuromosaic.cli.display_summary") as summary_mock, patch(
        "neuromosaic.cli.compare_experiments"
    ) as compare_mock, patch(
        "neuromosaic.cli.display_comparison"
    ) as display_compare_mock, patch(
        "neuromosaic.cli.generate_analysis_plots"
    ) as plot_mock, patch(
        "neuromosaic.cli.output_analysis"
    ) as output_mock:

        analyze_mock.return_value = {"accuracy": {"mean": 0.9}}
        yield {
            "analyze": analyze_mock,
            "display": display_mock,
            "summary": summary_mock,
            "compare": compare_mock,
            "display_compare": display_compare_mock,
            "plot": plot_mock,
            "output": output_mock,
        }


def test_quickstart_command(
    runner,
    mock_orchestrator,
    mock_multiprocessing,
    mock_uvicorn,
    mock_dashboard,
    tmp_path,
):
    """Test the quickstart command."""
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        with patch("neuromosaic.cli.Orchestrator", mock_orchestrator), patch(
            "neuromosaic.cli.Config"
        ) as mock_config, patch(
            "neuromosaic.cli.get_api_settings"
        ) as mock_settings, patch(
            "asyncio.sleep", side_effect=KeyboardInterrupt
        ):  # Simulate Ctrl+C

            # Mock Config.from_env()
            mock_config.from_env.return_value = Config(
                environment="development",
                llm=LLMConfig(),
                storage=StorageConfig(cache_size="50GB"),  # Fixed cache size format
                database=DatabaseConfig(db_url=f"sqlite:///{td}/results.db"),
                container=ContainerConfig(),
            )

            # Mock API settings
            mock_settings.return_value = MagicMock(api_host="0.0.0.0", api_port=8000)

            result = runner.invoke(cli, ["quickstart", "--output-dir", "test_output"])

            assert result.exit_code == 0
            assert "Starting quickstart architecture search..." in result.stdout
            assert "Starting API server at http://0.0.0.0:8000" in result.stdout
            assert "Starting dashboard at http://0.0.0.0:8050" in result.stdout
            assert "Shutting down servers..." in result.stdout

            # Verify processes were started and terminated
            mock_multiprocessing.assert_called()
            assert mock_multiprocessing.call_count == 2  # API and dashboard
            mock_multiprocessing.return_value.terminate.assert_called()
            mock_multiprocessing.return_value.join.assert_called()

            # Verify orchestrator was called correctly
            mock_orchestrator.assert_called_once()
            mock_orchestrator.return_value.run_batch.assert_called_once()


def test_quickstart_with_failed_search(
    runner,
    mock_failed_orchestrator,
    mock_multiprocessing,
    mock_uvicorn,
    mock_dashboard,
    minimal_config,
    tmp_path,
):
    """Test quickstart command with failed search."""
    with runner.isolated_filesystem(temp_dir=tmp_path):
        with patch("neuromosaic.cli.Orchestrator", mock_failed_orchestrator), patch(
            "neuromosaic.cli.Config"
        ) as mock_config, patch(
            "neuromosaic.cli.get_api_settings"
        ) as mock_settings, patch(
            "asyncio.sleep", side_effect=KeyboardInterrupt
        ):
            # Mock Config.from_env()
            mock_config.from_env.return_value = minimal_config

            # Mock API settings
            mock_settings.return_value = MagicMock(api_host="0.0.0.0", api_port=8000)

            # Mock the orchestrator to raise an error
            mock_failed_orchestrator.return_value.run_cycle.side_effect = RuntimeError(
                "Search failed"
            )
            mock_failed_orchestrator.return_value.run_batch.side_effect = RuntimeError(
                "Search failed"
            )

            result = runner.invoke(cli, ["quickstart", "--output-dir", "test_output"])

            # Check that the command failed
            assert result.exit_code == 1
            # Check that the error message is in stderr
            assert "Error during search: Search failed" in result.stderr
            assert "Aborted!" in result.stderr


def test_experiment_command(
    runner, mock_orchestrator, default_config, config_dict, tmp_path
):
    """Test the experiment command."""
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        # Create a test config file
        config_path = Path(td) / "test_config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config_dict, f)

        with patch("neuromosaic.cli.Orchestrator", mock_orchestrator), patch(
            "neuromosaic.cli.Config"
        ) as mock_config:
            # Mock Config.from_env()
            mock_config.from_env.return_value = default_config
            mock_config.return_value = default_config

            result = runner.invoke(
                cli,
                [
                    "experiment",
                    "--config",
                    str(config_path),
                    "--output-dir",
                    "test_output",
                ],
            )

            assert result.exit_code == 0


def test_experiment_resume(
    runner, mock_orchestrator, default_config, config_dict, tmp_path
):
    """Test experiment command with resume option."""
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        # Create a test config file
        config_path = Path(td) / "test_config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config_dict, f)

        with patch("neuromosaic.cli.Orchestrator", mock_orchestrator), patch(
            "neuromosaic.cli.Config"
        ) as mock_config:
            # Mock Config.from_env()
            mock_config.from_env.return_value = default_config
            mock_config.return_value = default_config

            result = runner.invoke(
                cli, ["experiment", "--config", str(config_path), "--resume"]
            )

            assert result.exit_code == 0


def test_quickstart_with_gpu_flag(
    runner,
    mock_orchestrator,
    mock_multiprocessing,
    mock_uvicorn,
    mock_dashboard,
    tmp_path,
):
    """Test quickstart command with GPU flag."""
    with runner.isolated_filesystem(temp_dir=tmp_path):
        with patch("neuromosaic.cli.Orchestrator", mock_orchestrator), patch(
            "neuromosaic.cli.Config"
        ) as mock_config, patch(
            "neuromosaic.cli.get_api_settings"
        ) as mock_settings, patch(
            "asyncio.sleep", side_effect=KeyboardInterrupt
        ):  # Simulate Ctrl+C

            # Mock Config.from_env()
            config = Config(
                environment="development",
                llm=LLMConfig(),
                storage=StorageConfig(),
                database=DatabaseConfig(),
                container=ContainerConfig(),
            )
            mock_config.from_env.return_value = config

            # Mock API settings
            mock_settings.return_value = MagicMock(api_host="0.0.0.0", api_port=8000)

            # Test CPU flag
            result = runner.invoke(cli, ["quickstart", "--cpu"])
            assert result.exit_code == 0
            assert mock_orchestrator.return_value.run_batch.call_count == 1
            assert config.container.device == "cpu"
            assert "Shutting down servers..." in result.stdout

            # Test GPU flag
            result = runner.invoke(cli, ["quickstart", "--gpu"])
            assert result.exit_code == 0
            assert mock_orchestrator.return_value.run_batch.call_count == 2
            assert config.container.device == "gpu"
            assert "Shutting down servers..." in result.stdout

            # Verify processes were properly terminated
            assert (
                mock_multiprocessing.return_value.terminate.call_count == 4
            )  # 2 processes × 2 runs
            assert (
                mock_multiprocessing.return_value.join.call_count == 4
            )  # 2 processes × 2 runs


def test_analyze_command(runner, mock_results_db, mock_analysis, tmp_path):
    """Test the analyze command."""
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        # Create test results directory
        results_dir = Path(td) / "results"
        results_dir.mkdir()

        result = runner.invoke(
            cli,
            ["analyze", str(results_dir), "--metric", "accuracy", "--format", "json"],
        )

        assert result.exit_code == 0
        mock_analysis["analyze"].assert_called_once()
        mock_analysis["output"].assert_called_once()


def test_inspect_command(runner, mock_results_db, mock_analysis, tmp_path):
    """Test the inspect command."""
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        result = runner.invoke(
            cli, ["inspect", "test_arch_1", "--detailed", "--export-code"]
        )

        assert result.exit_code == 0
        mock_analysis["display"].assert_called_once()

        # Check if code file was created
        code_path = Path(td) / "architecture_test_arch_1.py"
        assert code_path.exists()


def test_inspect_nonexistent_architecture(runner, mock_results_db):
    """Test inspecting a non-existent architecture."""
    mock_results_db.return_value.get_run_info.return_value = None

    result = runner.invoke(cli, ["inspect", "nonexistent_arch"])

    assert result.exit_code == 0
    assert "No architecture found with ID nonexistent_arch" in result.stderr


def test_cli_help(runner):
    """Test the CLI help command."""
    result = runner.invoke(cli, ["--help"])

    assert result.exit_code == 0
    assert "Neuromosaic: Neural Architecture Search" in result.output

    # Test help for each subcommand
    for cmd in ["quickstart", "experiment", "analyze", "inspect"]:
        result = runner.invoke(cli, [cmd, "--help"])
        assert result.exit_code == 0
        assert cmd in result.output.lower()


def test_analyze_with_comparison(runner, mock_results_db, mock_analysis, tmp_path):
    """Test analyze command with comparison option."""
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        # Create test directories
        results_dir = Path(td) / "results1"
        compare_dir = Path(td) / "results2"
        results_dir.mkdir()
        compare_dir.mkdir()

        result = runner.invoke(
            cli, ["analyze", str(results_dir), "--compare-with", str(compare_dir)]
        )

        assert result.exit_code == 0
        mock_analysis["compare"].assert_called_once()
        mock_analysis["display_compare"].assert_called_once()
