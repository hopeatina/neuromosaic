#!/usr/bin/env python3
"""
Command-line interface for Neuromosaic.

This module provides a command-line interface for running neural architecture search
experiments using Neuromosaic. It supports both quick-start and customized experiments,
along with tools for analysis and visualization.

Main Commands:
    quickstart: Run a basic architecture search with sensible defaults
        Options:
            --output-dir: Directory to save results (default: neuromosaic_quickstart)
            --cpu: Use CPU for training
            --gpu: Use GPU for training
            --batch-size: Number of parallel experiments (default: 5)
    
    experiment: Run a customized architecture search experiment
        Options:
            --config: Path to custom configuration file (required)
            --output-dir: Directory to store results
            --resume: Resume from previous run
            --batch-size: Number of parallel experiments (default: 5)
            --parallel/--sequential: Run experiments in parallel or sequentially

    analyze: Deep inspection and visualization of results
        Options:
            results-dir: Path to results directory
            --metric: Metric to analyze (default: accuracy)
            --format: Output format (text/json/csv)
            --compare-with: Compare with another results directory

    inspect: Inspect specific architectures
        Options:
            architecture-id: ID of architecture to inspect
            --export-code: Export architecture code
            --detailed/--summary: Show detailed or summary metrics

Example Usage:
    # Quick start with default settings
    $ python -m neuromosaic quickstart

    # Quick start with GPU and parallel execution
    $ python -m neuromosaic quickstart --gpu --batch-size 8

    # Custom experiment with configuration
    $ python -m neuromosaic experiment --config custom_config.yaml --parallel

    # Resume previous experiment
    $ python -m neuromosaic experiment --config config.yaml --resume

    # Analyze results
    $ python -m neuromosaic analyze results_dir --metric accuracy

    # Compare experiments
    $ python -m neuromosaic analyze results_dir --compare-with other_results

    # Inspect specific architecture
    $ python -m neuromosaic inspect arch_123 --detailed

Implementation Notes:
    - Commands that involve running experiments (quickstart, experiment) handle async
      operations internally, no special handling needed by the user.
    - The experiment command supports both parallel and sequential execution modes.
    - Results are automatically saved and can be analyzed later using the analyze
      and inspect commands.
    - All commands support the --help option for detailed usage information.
"""

import traceback
import click
import yaml
import logging
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any, List
import shutil
import uvicorn
import multiprocessing
from dataclasses import asdict
import socket

from neuromosaic.orchestrator import Orchestrator
from neuromosaic.utils.config import Config, LLMConfig
from neuromosaic.utils.logging import setup_logger
from neuromosaic.meta_learning.visualization import plot_results, save_plot
from neuromosaic.results_db import ResultsDB
from neuromosaic.api.config import get_api_settings
from neuromosaic.frontend.dashboard import run_dashboard

logger = setup_logger(__name__)


def analyze_results(results: List[Dict[str, Any]], metric: str) -> Dict[str, Any]:
    """Analyze experiment results for a given metric."""
    analysis = {
        metric: {
            "mean": sum(r["metrics"][metric] for r in results) / len(results),
            "best": max(r["metrics"][metric] for r in results),
            "worst": min(r["metrics"][metric] for r in results),
        }
    }
    return analysis


def display_detailed_metrics(result: Dict[str, Any]) -> None:
    """Display detailed metrics for an architecture."""
    click.echo("Architecture Details:")
    click.echo(f"ID: {result['id']}")
    click.echo("\nMetrics:")
    for metric, value in result["metrics"].items():
        click.echo(f"  {metric}: {value}")
    click.echo(f"\nCode Version: {result['code_version']}")


def display_summary(result: Dict[str, Any]) -> None:
    """Display summary information for an architecture."""
    click.echo(f"Architecture {result['id']}:")
    click.echo(f"  Accuracy: {result['metrics'].get('accuracy', 'N/A')}")
    click.echo(f"  Latency: {result['metrics'].get('latency', 'N/A')}ms")


def compare_experiments(
    results1: List[Dict[str, Any]], results2: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Compare results from two experiments."""
    comparison = {}
    for metric in ["accuracy", "latency"]:
        comparison[metric] = {
            "exp1_mean": sum(r["metrics"].get(metric, 0) for r in results1)
            / len(results1),
            "exp2_mean": sum(r["metrics"].get(metric, 0) for r in results2)
            / len(results2),
            "difference": (
                sum(r["metrics"].get(metric, 0) for r in results1) / len(results1)
                - sum(r["metrics"].get(metric, 0) for r in results2) / len(results2)
            ),
        }
    return comparison


def display_comparison(comparison: Dict[str, Any], format: str = "text") -> None:
    """Display comparison results."""
    if format == "text":
        for metric, values in comparison.items():
            click.echo(f"\n{metric.title()} Comparison:")
            click.echo(f"  Experiment 1 mean: {values['exp1_mean']:.3f}")
            click.echo(f"  Experiment 2 mean: {values['exp2_mean']:.3f}")
            click.echo(f"  Difference: {values['difference']:.3f}")
    elif format == "json":
        click.echo(yaml.dump(comparison))


def generate_analysis_plots(results: List[Dict[str, Any]], output_dir: Path) -> None:
    """Generate analysis plots."""
    output_dir.mkdir(parents=True, exist_ok=True)
    for metric in ["accuracy", "latency"]:
        plot_results(metric, "scatter", output_dir / f"{metric}_scatter.png", results)
        plot_results(metric, "history", output_dir / f"{metric}_history.png", results)


def output_analysis(analysis: Dict[str, Any], format: str = "text") -> None:
    """Output analysis results in the specified format."""
    if format == "text":
        for metric, values in analysis.items():
            click.echo(f"\n{metric.title()} Analysis:")
            for key, value in values.items():
                click.echo(f"  {key}: {value:.3f}")
    elif format == "json":
        click.echo(yaml.dump(analysis))
    elif format == "csv":
        for metric, values in analysis.items():
            click.echo(f"metric,{','.join(values.keys())}")
            click.echo(f"{metric},{','.join(str(v) for v in values.values())}")


@click.group()
@click.option(
    "--config", type=click.Path(exists=True), help="Path to configuration file"
)
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"]),
    default="INFO",
    help="Logging level",
)
def cli(config: Optional[str], log_level: str):
    """Neuromosaic: Neural Architecture Search with LLM Code Generation"""
    if config:
        Config().load_config(config)
    logging.getLogger().setLevel(log_level)


def get_or_create_eventloop():
    """Get the current event loop or create a new one if it doesn't exist."""
    try:
        return asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop


async def _run_orchestrator(orchestrator, batch_size: int, parallel: bool = True):
    """Run the orchestrator asynchronously."""
    return await orchestrator.run_batch(batch_size=batch_size, parallel=parallel)


def find_available_port(start_port: int = 8050, max_attempts: int = 100) -> int:
    """Find an available port starting from start_port."""
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("", port))
                return port
            except OSError:
                continue
    raise RuntimeError(
        f"Could not find an available port after {max_attempts} attempts"
    )


async def _run_quickstart(
    output_dir: str, cpu: bool = False, gpu: bool = False, batch_size: int = 5
) -> None:
    """Async implementation of quickstart command."""
    try:
        # Create output directory first
        output_dir_path = Path(output_dir)
        output_dir_path.mkdir(parents=True, exist_ok=True)

        # Initialize config object with defaults
        config_obj = Config.from_env()

        # Update specific values
        if cpu:
            config_obj.container.device = "cpu"
        elif gpu:
            config_obj.container.device = "gpu"

        # Update database path to be in the output directory
        config_obj.database.db_url = f"sqlite:///{output_dir_path}/results.db"

        # Save config for reference
        # config_path = output_dir_path / "config.yaml"
        # with open(config_path, "w") as f:
        #     yaml.dump(asdict(config_obj), f)

        # Start the API server in the background with proper config
        settings = get_api_settings()
        api_host = settings.api_host
        api_port = find_available_port(8000)
        click.echo(f"Starting API server at http://{api_host}:{api_port}")

        api_process = multiprocessing.Process(
            target=uvicorn.run,
            args=("neuromosaic.api.main:app",),
            kwargs={
                "host": api_host,
                "port": api_port,
                "log_level": "info",
                "reload": False,
            },
        )
        api_process.start()

        # Start the dashboard in the background
        dashboard_host = "0.0.0.0"
        dashboard_port = find_available_port(8050)
        click.echo(f"Starting dashboard at http://{dashboard_host}:{dashboard_port}")
        dashboard_process = multiprocessing.Process(
            target=run_dashboard,
            kwargs={
                "host": dashboard_host,
                "port": dashboard_port,
                "debug": False,
            },
        )
        dashboard_process.start()

        # Create orchestrator and run batch
        orchestrator = Orchestrator(config_obj)
        results = await orchestrator.run_batch(batch_size=batch_size, parallel=True)

        # Process results
        if results:
            best_result = None
            best_accuracy = -1
            for result in results:
                if result and isinstance(result, dict):
                    metrics = result.get("metrics", {})
                    accuracy = (
                        metrics.get("accuracy", 0) if isinstance(metrics, dict) else 0
                    )
                    if accuracy > best_accuracy:
                        best_accuracy = accuracy
                        best_result = result

            if not best_result:
                logging.error("No valid results found with metrics")
                raise click.Abort()

            click.echo("Search completed successfully!")
            click.echo(f"Results saved in {output_dir}")
            if best_result.get("metrics"):
                click.echo(
                    f"Best architecture achieved {best_result['metrics']['accuracy']:.2f}% accuracy"
                )
            click.echo(f"Total architectures evaluated: {len(results)}")
        else:
            click.echo("Search completed but no valid results were produced.")

        # Keep the servers running until user interrupts
        click.echo("\nServers are running in the background. Press Ctrl+C to stop.")
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            click.echo("\nShutting down servers...")
            api_process.terminate()
            dashboard_process.terminate()
            api_process.join()
            dashboard_process.join()

    except Exception as e:
        logger.error(f"Error during quickstart: {str(e)}")
        # stack trace
        logger.error(f"Stack trace: {traceback.format_exc()}")
        click.echo(f"Error during search: {str(e)}", err=True)

        raise click.Abort()


async def _run_experiment(
    config: str,
    output_dir: Optional[str],
    resume: bool,
    batch_size: int = 5,
    parallel: bool = True,
) -> None:
    """Async implementation of experiment command."""
    try:
        # First load environment variables
        config_obj = Config.from_env()
        # Then merge with YAML config
        config_obj.load_config(config)

        if output_dir:
            output_dir_path = Path(output_dir)
            output_dir_path.mkdir(parents=True, exist_ok=True)

        # Create orchestrator
        orchestrator = Orchestrator(config_obj)

        if resume:
            click.echo("Resuming previous experiment...")
            # Load previous state if resuming
            orchestrator.load_state()
        else:
            click.echo("Starting new experiment...")

        # Run experiments
        results = await orchestrator.run_batch(batch_size=batch_size, parallel=parallel)

        # Process results
        if results:
            best_result = max(results, key=lambda x: x["metrics"]["accuracy"])
            click.echo("Experiment completed successfully!")
            click.echo(
                f"Results saved in {output_dir if output_dir else 'default directory'}"
            )
            click.echo(
                f"Best architecture achieved {best_result['metrics']['accuracy']:.2f}% accuracy"
            )
            click.echo(f"Total architectures evaluated: {len(results)}")

            # Save final state
            orchestrator.save_state()
        else:
            click.echo("Experiment completed but no valid results were produced.")

    except Exception as e:
        logger.error(f"Error during experiment: {str(e)}")
        click.echo(f"Error during experiment: {str(e)}", err=True)
        raise click.Abort()


@cli.command()
@click.option(
    "--output-dir",
    default="neuromosaic_quickstart",
    help="Directory to save results",
)
@click.option("--cpu", is_flag=True, help="Use CPU for training")
@click.option("--gpu", is_flag=True, help="Use GPU for training")
@click.option(
    "--batch-size", type=int, default=5, help="Number of parallel experiments"
)
def quickstart(
    output_dir: str, cpu: bool = False, gpu: bool = False, batch_size: int = 5
):
    """Quick start with default configuration."""
    click.echo("Starting quickstart architecture search...")
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(_run_quickstart(output_dir, cpu, gpu, batch_size))
    except RuntimeError:
        # If no event loop exists, create one
        asyncio.run(_run_quickstart(output_dir, cpu, gpu, batch_size))


@cli.command()
@click.option(
    "--config",
    type=click.Path(exists=True),
    required=True,
    help="Path to custom configuration file",
)
@click.option("--output-dir", type=click.Path(), help="Directory to store results")
@click.option("--resume/--no-resume", default=False, help="Resume from previous run")
@click.option(
    "--batch-size", type=int, default=5, help="Number of parallel experiments"
)
@click.option(
    "--parallel/--sequential", default=True, help="Run experiments in parallel"
)
def experiment(
    config: str,
    output_dir: Optional[str],
    resume: bool,
    batch_size: int = 5,
    parallel: bool = True,
):
    """Run a customized architecture search experiment."""
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            _run_experiment(config, output_dir, resume, batch_size, parallel)
        )
    except RuntimeError:
        # If no event loop exists, create one
        asyncio.run(_run_experiment(config, output_dir, resume, batch_size, parallel))


@cli.command()
@click.argument("results-dir", type=click.Path(exists=True))
@click.option("--metric", type=str, default="accuracy", help="Metric to analyze")
@click.option(
    "--format",
    type=click.Choice(["text", "json", "csv"]),
    default="text",
    help="Output format",
)
@click.option(
    "--compare-with",
    type=click.Path(exists=True),
    help="Compare with another results directory",
)
def analyze(results_dir: str, metric: str, format: str, compare_with: Optional[str]):
    """Analyze and visualize experiment results."""
    results_dir = Path(results_dir)
    db = ResultsDB(Config())

    # Load and analyze results
    results = db.load_results(results_dir)
    analysis = analyze_results(results, metric)

    if compare_with:
        compare_dir = Path(compare_with)
        compare_results = db.load_results(compare_dir)
        comparison = compare_experiments(results, compare_results)
        display_comparison(comparison, format)

    # Generate visualizations
    generate_analysis_plots(results, results_dir / "analysis")

    # Output results in requested format
    output_analysis(analysis, format)


@cli.command()
@click.argument("architecture-id")
@click.option("--export-code", is_flag=True, help="Export architecture code")
@click.option("--detailed/--summary", default=False, help="Show detailed metrics")
def inspect(architecture_id: str, export_code: bool, detailed: bool):
    """Inspect a specific architecture in detail."""
    config = Config()
    db = ResultsDB(config)
    result = db.get_run_info(architecture_id)

    if result:
        if detailed:
            display_detailed_metrics(result)
        else:
            display_summary(result)

        if export_code:
            code_path = Path(f"architecture_{architecture_id}.py")
            with open(code_path, "w") as f:
                f.write(result["code"])
            click.echo(f"Architecture code exported to {code_path}")
    else:
        click.echo(f"No architecture found with ID {architecture_id}", err=True)


@cli.command()
@click.option("--host", default="0.0.0.0", help="Host to run the dashboard server on")
@click.option(
    "--port", default=8050, type=int, help="Port to run the dashboard server on"
)
@click.option(
    "--debug/--no-debug", default=False, help="Run the dashboard in debug mode"
)
def dashboard(host: str, port: int, debug: bool):
    """Launch the Neuromosaic dashboard visualization interface."""
    from neuromosaic.frontend.dashboard import run_dashboard

    click.echo(f"Starting dashboard server at http://{host}:{port}")
    run_dashboard(host=host, port=port, debug=debug)


@cli.command()
@click.option(
    "--host",
    default=None,
    help="Host to run the API server on (overrides config)",
)
@click.option(
    "--port",
    default=None,
    type=int,
    help="Port to run the API server on (overrides config)",
)
@click.option(
    "--reload/--no-reload",
    default=False,
    help="Enable auto-reload for development",
)
def serve_api(host: Optional[str], port: Optional[int], reload: bool):
    """Start the FastAPI server."""
    settings = get_api_settings()

    # Command line options override config
    host = host or settings.api_host
    port = port or settings.api_port

    click.echo(f"Starting API server at http://{host}:{port}")
    uvicorn.run(
        "neuromosaic.api.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info",
    )


def main():
    """Entry point for the CLI"""
    cli()


if __name__ == "__main__":
    main()
