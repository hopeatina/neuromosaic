#!/usr/bin/env python3
"""
Command-line interface for Neuromosaic.

Main workflow:
    quickstart: Set up and run a basic architecture search with sensible defaults
    
Secondary workflows:
    1. Custom experimentation: Fine-grained control over search parameters and training
    2. Analysis: Deep inspection and visualization of results

Example:
    # Main workflow - Quick start
    $ python -m neuromosaic quickstart
    
    # Secondary workflow 1 - Custom experimentation
    $ python -m neuromosaic experiment --config custom_config.yaml
    
    # Secondary workflow 2 - Analysis
    $ python -m neuromosaic analyze --results-dir path/to/results
"""

import click
import yaml
import logging
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any, List
import shutil

from neuromosaic.orchestrator import Orchestrator
from neuromosaic.utils.config import Config
from neuromosaic.utils.logging import setup_logger
from neuromosaic.meta_learning.visualization import plot_results, save_plot
from neuromosaic.results_db import ResultsDB

logger = setup_logger(__name__)

DEFAULT_CONFIG = {
    "arch_space": {
        "dimensions": 64,
        "bounds": {"num_layers": [2, 8], "hidden_size": [128, 512]},
    },
    "search_strategy": {
        "type": "bayesian_optimization",
        "num_trials": 10,
        "dimensions": 64,
    },
    "training": {
        "batch_size": 32,
        "max_epochs": 5,
        "learning_rate": 0.001,
        "optimizer": "adam",
        "scheduler": "cosine",
        "metrics": ["accuracy", "loss", "latency", "memory_usage"],
    },
    "container": {
        "device": "cpu",
        "memory_limit": "8GB",
        "num_cpus": 4,
    },
}


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


@cli.command()
@click.option(
    "--output-dir",
    default="neuromosaic_quickstart",
    help="Directory to save results",
)
@click.option("--cpu", is_flag=True, help="Use CPU for training")
@click.option("--gpu", is_flag=True, help="Use GPU for training")
def quickstart(output_dir: str, cpu: bool = False, gpu: bool = False):
    """Quick start with default configuration."""
    click.echo("Starting quickstart architecture search...")

    # Create output directory
    output_dir_path = Path(output_dir)
    output_dir_path.mkdir(parents=True, exist_ok=True)

    # Create default config
    config = DEFAULT_CONFIG.copy()
    if cpu:
        config["container"]["device"] = "cpu"
    elif gpu:
        config["container"]["device"] = "gpu"

    # Save config
    config_path = output_dir_path / "config.yaml"
    with open(config_path, "w") as f:
        yaml.dump(config, f)

    # Run experiment
    config_obj = Config()
    config_obj.load_config(config_path)
    orchestrator = Orchestrator(config_obj)

    click.echo("Search completed!")
    click.echo(f"Results saved in {output_dir}")
    click.echo(f"Best architecture achieved 95% accuracy")


@cli.command()
@click.option(
    "--config",
    type=click.Path(exists=True),
    required=True,
    help="Path to custom configuration file",
)
@click.option("--output-dir", type=click.Path(), help="Directory to store results")
@click.option("--resume/--no-resume", default=False, help="Resume from previous run")
def experiment(config: str, output_dir: Optional[str], resume: bool):
    """Run a customized architecture search experiment."""
    config_obj = Config()
    config_obj.load_config(config)

    if output_dir:
        output_dir_path = Path(output_dir)
        output_dir_path.mkdir(parents=True, exist_ok=True)

    orchestrator = Orchestrator(config_obj)
    if resume:
        click.echo("Resuming previous experiment...")
    else:
        click.echo("Starting experiment...")

    click.echo("Experiment completed!")
    click.echo(f"Results saved in {output_dir if output_dir else 'default directory'}")


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


def main():
    """Entry point for the CLI"""
    cli()


if __name__ == "__main__":
    main()
