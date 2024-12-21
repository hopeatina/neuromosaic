"""Tests for the Neuromosaic CLI."""

import pytest
from click.testing import CliRunner
from pathlib import Path
import yaml
import json
from unittest.mock import patch, Mock, AsyncMock, MagicMock

from neuromosaic.cli import cli, DEFAULT_CONFIG
from neuromosaic.utils.config import Config
from neuromosaic.orchestrator import Orchestrator


@pytest.fixture
def runner():
    """Create a CLI runner for testing."""
    return CliRunner(mix_stderr=False)  # Capture stderr separately


@pytest.fixture
def mock_orchestrator():
    """Mock the Orchestrator class."""
    mock = MagicMock()
    # Create a mock that returns a completed future
    mock_coro = AsyncMock()
    mock_coro.return_value = [
        {
            "id": "test_arch_1",
            "metrics": {"accuracy": 0.95, "latency": 10.5},
            "config": {"layers": 4},
        },
        {
            "id": "test_arch_2",
            "metrics": {"accuracy": 0.85, "latency": 8.5},
            "config": {"layers": 3},
        },
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


def test_quickstart_command(runner, mock_orchestrator, tmp_path):
    """Test the quickstart command."""
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        with patch("neuromosaic.cli.Orchestrator", mock_orchestrator):
            result = runner.invoke(cli, ["quickstart", "--output-dir", "test_output"])

            assert result.exit_code == 0
            assert "Starting quickstart architecture search..." in result.stdout
            assert "Search completed successfully!" in result.stdout
            assert "Best architecture achieved" in result.stdout

            # Verify orchestrator was called correctly
            mock_orchestrator.assert_called_once()
            mock_orchestrator.return_value.run_batch.assert_called_once()


def test_experiment_command(runner, mock_orchestrator, tmp_path):
    """Test the experiment command."""
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        # Create a test config file
        config_path = Path(td) / "test_config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(DEFAULT_CONFIG, f)

        with patch("neuromosaic.cli.Orchestrator", mock_orchestrator):
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
            assert "Starting new experiment..." in result.stdout
            assert "Experiment completed successfully!" in result.stdout

            # Verify orchestrator was called correctly
            mock_orchestrator.assert_called_once()
            mock_orchestrator.return_value.run_batch.assert_called_once()


def test_quickstart_with_gpu_flag(runner, mock_orchestrator, tmp_path):
    """Test quickstart command with GPU flag."""
    with runner.isolated_filesystem(temp_dir=tmp_path):
        with patch("neuromosaic.cli.Orchestrator", mock_orchestrator):
            # Test CPU flag
            result = runner.invoke(cli, ["quickstart", "--cpu"])
            assert result.exit_code == 0
            assert mock_orchestrator.return_value.run_batch.call_count == 1

            # Test GPU flag
            result = runner.invoke(cli, ["quickstart", "--gpu"])
            assert result.exit_code == 0
            assert mock_orchestrator.return_value.run_batch.call_count == 2


def test_experiment_resume(runner, mock_orchestrator, tmp_path):
    """Test experiment command with resume option."""
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        config_path = Path(td) / "test_config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(DEFAULT_CONFIG, f)

        with patch("neuromosaic.cli.Orchestrator", mock_orchestrator):
            result = runner.invoke(
                cli, ["experiment", "--config", str(config_path), "--resume"]
            )

            assert result.exit_code == 0
            assert "Resuming previous experiment..." in result.stdout
            assert "Experiment completed successfully!" in result.stdout

            # Verify load_state was called
            mock_orchestrator.return_value.load_state.assert_called_once()
            mock_orchestrator.return_value.run_batch.assert_called_once()


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
