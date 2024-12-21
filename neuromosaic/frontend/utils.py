"""
utils.py

Provides shared helper functions and utilities for the frontend package.
These utilities handle data formatting, API communication, and other
common operations needed across the dashboard components.

The module serves as a bridge between the raw data from ResultsDB
and the visualization-ready format needed by the dashboard components.
"""

from typing import Dict, List, Any, Tuple
import numpy as np
import requests
from neuromosaic.results_db import ResultsDB


def format_experiment_data(
    results: List[Dict[str, Any]]
) -> Tuple[np.ndarray, np.ndarray, List[str]]:
    """Format experiment results for visualization.

    Transforms raw experiment results into a format suitable for
    3D visualization. This includes computing embeddings for the
    architecture space and formatting associated metrics.

    Args:
        results (List[Dict[str, Any]]): List of experiment results from ResultsDB.
                                       Each result should contain metrics and
                                       architecture specifications.

    Returns:
        Tuple[np.ndarray, np.ndarray, List[str]]: Returns (points, metrics, labels)
            - points: Nx3 array of point coordinates in the embedded space
            - metrics: N-length array of metric values for coloring
            - labels: N-length list of point labels for tooltips
    """
    # TODO: Implement actual dimensionality reduction from architecture space
    n_points = len(results)
    points = np.random.normal(size=(n_points, 3))  # Placeholder for actual embeddings
    metrics = np.array([r["metrics"].get("accuracy", 0.0) for r in results])
    labels = [f"Architecture #{r['id']}" for r in results]
    return points, metrics, labels


def format_architecture_details(architecture: Dict[str, Any]) -> Dict[str, Any]:
    """Format architecture details for display.

    Transforms raw architecture data into a structured format suitable
    for display in the dashboard's detail panels. Handles formatting of
    metrics, component descriptions, and timestamps.

    Args:
        architecture (Dict[str, Any]): Raw architecture data from ResultsDB
                                     containing metrics, components, and metadata.

    Returns:
        Dict[str, Any]: Formatted architecture details with consistent structure
                       and formatting for display.
    """
    return {
        "id": architecture["id"],
        "metrics": {
            k: f"{v:.3f}" if isinstance(v, float) else v
            for k, v in architecture["metrics"].items()
        },
        "components": architecture.get("components", []),
        "hyperparameters": architecture.get("hyperparameters", {}),
        "timestamp": architecture.get("timestamp", "N/A"),
    }


def get_available_metrics(results_db: ResultsDB) -> List[Dict[str, str]]:
    """Get list of available metrics for dropdown.

    Queries the ResultsDB to determine what metrics are available
    across all experiments. This is used to populate metric selection
    dropdowns in the dashboard.

    Args:
        results_db (ResultsDB): ResultsDB instance for querying available metrics.

    Returns:
        List[Dict[str, str]]: List of metric options in format [{"label": "Name", "value": "key"}]
                             suitable for use in Dash dropdowns.
    """
    # TODO: Query actual available metrics from ResultsDB
    return [
        {"label": "Accuracy", "value": "accuracy"},
        {"label": "Loss", "value": "loss"},
        {"label": "Perplexity", "value": "perplexity"},
        {"label": "Latency", "value": "latency"},
        {"label": "Memory Usage", "value": "memory_usage"},
    ]


def fetch_experiments_data(api_url: str) -> List[Dict[str, Any]]:
    """Fetch experiment data from the backend API.

    Retrieves the full list of experiments with their metrics and
    embeddings from the backend API. Handles connection errors and
    provides appropriate fallbacks.

    Args:
        api_url (str): The base URL for the backend API.

    Returns:
        List[Dict[str, Any]]: List of experiment data dictionaries or
                             empty list on error.
    """
    try:
        response = requests.get(f"{api_url}/experiments")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching experiments: {e}")
        return []
