"""
plots.py

Functions to create or update various Plotly figures used in the dashboard.
These visualization utilities support the interactive exploration of the
architecture search space and experiment results.

Key visualizations include:
- 3D scatter plots of architecture embeddings
- Timeline plots of metric evolution
- Parallel coordinates plots for hyperparameter exploration
"""

import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from typing import List, Dict, Any, Tuple


def create_3d_scatter(
    points: np.ndarray, metrics: np.ndarray, labels: List[str], metric_name: str
) -> go.Figure:
    """Create a 3D scatter plot of architecture points.

    Creates an interactive 3D visualization where each point represents
    an architecture in the embedded space. Points are colored by their
    performance metrics and include hover information.

    Args:
        points (np.ndarray): Nx3 array of point coordinates from dimensionality
                           reduction of architecture specifications
        metrics (np.ndarray): N-length array of metric values for coloring points
        labels (List[str]): N-length list of point labels for hover text
        metric_name (str): Name of the metric being displayed (for colorbar)

    Returns:
        go.Figure: Interactive 3D scatter plot figure
    """
    fig = go.Figure(
        data=[
            go.Scatter3d(
                x=points[:, 0],
                y=points[:, 1],
                z=points[:, 2],
                mode="markers",
                marker=dict(
                    size=8,
                    color=metrics,
                    colorscale="Viridis",
                    opacity=0.8,
                    colorbar=dict(title=metric_name),
                ),
                text=labels,
                hovertemplate="<b>%{text}</b><br>"
                + "X: %{x:.2f}<br>"
                + "Y: %{y:.2f}<br>"
                + "Z: %{z:.2f}<br>"
                + f"{metric_name}: %{marker.color:.3f}",
            )
        ]
    )

    fig.update_layout(
        scene=dict(
            xaxis_title="Dimension 1",
            yaxis_title="Dimension 2",
            zaxis_title="Dimension 3",
            camera=dict(
                up=dict(x=0, y=0, z=1),
                center=dict(x=0, y=0, z=0),
                eye=dict(x=1.5, y=1.5, z=1.5),
            ),
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        showlegend=False,
    )

    return fig


def create_metric_timeline(
    timestamps: List[str], metrics: Dict[str, List[float]]
) -> go.Figure:
    """Create a timeline plot of metrics.

    Visualizes how different metrics evolve over time during the
    architecture search process. Supports multiple metrics for
    comparison.

    Args:
        timestamps (List[str]): List of timestamp strings for x-axis
        metrics (Dict[str, List[float]]): Dictionary mapping metric names
                                        to their values over time

    Returns:
        go.Figure: Interactive line plot of metric evolution
    """
    fig = go.Figure()

    for metric_name, values in metrics.items():
        fig.add_trace(
            go.Scatter(
                x=timestamps,
                y=values,
                mode="lines+markers",
                name=metric_name,
                hovertemplate=f"{metric_name}: %{y:.3f}<br>Time: %{x}",
            )
        )

    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Metric Value",
        hovermode="x unified",
        showlegend=True,
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
    )

    return fig


def create_parallel_coordinates(
    data: Dict[str, List[float]], dimensions: List[str]
) -> go.Figure:
    """Create a parallel coordinates plot for architecture parameters.

    Visualizes relationships between different architecture parameters
    and their impact on performance metrics. Useful for understanding
    parameter interactions and trade-offs.

    Args:
        data (Dict[str, List[float]]): Dictionary mapping parameter names
                                     to their values across experiments
        dimensions (List[str]): List of dimension names to include in
                              the visualization

    Returns:
        go.Figure: Interactive parallel coordinates plot
    """
    fig = px.parallel_coordinates(
        data,
        dimensions=dimensions,
        color=dimensions[-1],
        color_continuous_scale=px.colors.sequential.Viridis,
    )

    fig.update_layout(
        margin=dict(l=80, r=80, b=30, t=30),
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=True,
    )

    return fig
