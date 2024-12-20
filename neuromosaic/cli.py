#!/usr/bin/env python3
"""
Command-line interface for Neuromosaic.

This module provides commands for:
1. Running architecture searches
2. Managing experiments
3. Visualizing results
4. Configuring the system

Example:
    $ python cli.py search --config config.yaml --num-trials 100
    $ python cli.py visualize --metric accuracy --output plot.png
    $ python cli.py export-results --format csv --output results.csv
"""

import click
import yaml
import logging
import asyncio
from pathlib import Path
from typing import Optional

from neuromosaic.orchestrator import Orchestrator
from neuromosaic.utils.config import Config
from neuromosaic.utils.logging import setup_logger
from neuromosaic.meta_learning.visualization import plot_results, save_plot
from neuromosaic.results_db import ResultsDB

logger = setup_logger(__name__)


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
    "--num-trials", type=int, default=10, help="Number of architectures to evaluate"
)
@click.option(
    "--parallel/--sequential",
    default=True,
    help="Run trials in parallel or sequentially",
)
async def search(num_trials: int, parallel: bool):
    """Run neural architecture search"""
    config = Config()
    orchestrator = Orchestrator(config)

    if parallel:
        results = await orchestrator.run_batch(num_trials, parallel=True)
    else:
        results = []
        for _ in range(num_trials):
            result = await orchestrator.run_cycle()
            results.append(result)

    logger.info(f"Completed {len(results)} trials")
    best_result = max(results, key=lambda x: x["results"]["accuracy"])
    logger.info(f"Best architecture: {best_result}")


@cli.command()
@click.option("--metric", type=str, required=True, help="Metric to visualize")
@click.option("--output", type=click.Path(), required=True, help="Output file path")
@click.option(
    "--plot-type",
    type=click.Choice(["scatter", "heatmap", "history"]),
    default="scatter",
    help="Type of visualization",
)
def visualize(metric: str, output: str, plot_type: str):
    """Visualize search results"""
    config = Config()
    fig = plot_results(metric, plot_type)
    save_plot(fig, output)
    logger.info(f"Saved visualization to {output}")


@cli.command()
@click.option(
    "--format", type=click.Choice(["csv", "json"]), default="csv", help="Export format"
)
@click.option("--output", type=click.Path(), required=True, help="Output file path")
def export_results(format: str, output: str):
    """Export search results to file"""
    config = Config()
    db = ResultsDB(config)
    results = db.list_all_runs()

    if format == "csv":
        import pandas as pd

        df = pd.DataFrame(results)
        df.to_csv(output, index=False)
    else:
        import json

        with open(output, "w") as f:
            json.dump(results, f, indent=2)

    logger.info(f"Exported {len(results)} results to {output}")


@cli.command()
@click.argument("architecture_id")
def inspect(architecture_id: str):
    """Inspect a specific architecture"""
    config = Config()
    db = ResultsDB(config)
    result = db.get_run_info(architecture_id)

    if result:
        click.echo("Architecture Details:")
        click.echo(f"ID: {architecture_id}")
        click.echo(f"Metrics: {result['metrics']}")
        click.echo(f"Code Version: {result['code_version']}")
        click.echo("\nGenerated Code:")
        click.echo(result["code"])
    else:
        click.echo(f"No architecture found with ID {architecture_id}")


def main():
    """Entry point for the CLI"""
    cli()


if __name__ == "__main__":
    main()
