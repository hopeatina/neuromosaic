"""
Visualization module for meta-learning results.

This module provides functions for visualizing and analyzing
neural architecture search results.
"""

from typing import Any, Dict, List, Optional, Union
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


def plot_results(
    metric: str,
    plot_type: str = "scatter",
    output_path: Optional[Union[str, Path]] = None,
    data: Optional[List[Dict[str, Any]]] = None,
) -> plt.Figure:
    """
    Plot search results for a given metric.

    Args:
        metric: Name of the metric to plot
        plot_type: Type of plot ('scatter', 'heatmap', 'history')
        output_path: Path to save the plot
        data: List of result dictionaries

    Returns:
        matplotlib Figure object
    """
    if data is None:
        # Use dummy data for now
        data = [{"trial": i, metric: np.random.random()} for i in range(10)]

    df = pd.DataFrame(data)

    fig, ax = plt.subplots(figsize=(10, 6))

    if plot_type == "scatter":
        sns.scatterplot(data=df, x="trial", y=metric, ax=ax)
        ax.set_title(f"{metric.title()} vs Trial")

    elif plot_type == "heatmap":
        # Reshape data for heatmap if needed
        pivot_data = df.pivot_table(
            values=metric,
            index=df.index // 3,  # Arbitrary grouping for visualization
            columns=df.index % 3,
        )
        sns.heatmap(pivot_data, ax=ax, cmap="viridis")
        ax.set_title(f"{metric.title()} Heatmap")

    elif plot_type == "history":
        sns.lineplot(data=df, x="trial", y=metric, ax=ax)
        ax.set_title(f"{metric.title()} History")

    else:
        raise ValueError(f"Unknown plot type: {plot_type}")

    if output_path:
        save_plot(fig, output_path)

    return fig


def save_plot(fig: plt.Figure, output_path: Union[str, Path]) -> None:
    """
    Save a matplotlib figure to file.

    Args:
        fig: Figure to save
        output_path: Path where to save the figure
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig.savefig(output_path, bbox_inches="tight", dpi=300)
    plt.close(fig)
