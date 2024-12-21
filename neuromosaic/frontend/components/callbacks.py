"""
callbacks.py

Defines all Dash callbacks for interactivity within the NeuraMosaic dashboard.
Handles events such as:
- Clicking points in the 3D scatter plot
- Updating metric visualizations
- Launching new experiments
- Displaying architecture details

The callbacks coordinate with the ResultsDB to fetch and display real-time
experiment data and metrics.
"""

from dash import Input, Output, State, html
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import numpy as np
from neuromosaic.results_db import ResultsDB
from neuromosaic.frontend.utils import (
    format_experiment_data,
    format_architecture_details,
)


def register_callbacks(app):
    """Register all callbacks for the dashboard.

    Sets up the interactive behavior of the dashboard by connecting
    UI elements to their corresponding data and update functions.

    Args:
        app (dash.Dash): The Dash application instance to register callbacks with.
    """

    @app.callback(
        Output("architecture-space-plot", "figure"),
        [Input("metric-selector", "value"), Input("complexity-range", "value")],
    )
    def update_architecture_plot(metric, complexity_range):
        """Update the 3D architecture space visualization.

        Creates or updates the 3D scatter plot based on:
        - Selected metric for color coding
        - Complexity range filter
        - Available experiment data

        Args:
            metric (str): The metric to use for point coloring
            complexity_range (List[float]): Range of complexity values to filter by

        Returns:
            plotly.graph_objects.Figure: Updated 3D scatter plot

        Raises:
            PreventUpdate: If no valid data is available
        """
        if not metric:
            raise PreventUpdate("No metric selected")

        # TODO: Replace with actual data from ResultsDB
        n_points = 50
        np.random.seed(42)

        x = np.random.normal(size=n_points)
        y = np.random.normal(size=n_points)
        z = np.random.normal(size=n_points)
        colors = np.random.uniform(low=0.3, high=1.0, size=n_points)

        fig = go.Figure(
            data=[
                go.Scatter3d(
                    x=x,
                    y=y,
                    z=z,
                    mode="markers",
                    marker=dict(
                        size=8,
                        color=colors,
                        colorscale="Viridis",
                        opacity=0.8,
                        colorbar=dict(title=metric.capitalize()),
                    ),
                    hovertemplate="<b>Architecture %{text}</b><br>"
                    + "X: %{x:.2f}<br>"
                    + "Y: %{y:.2f}<br>"
                    + "Z: %{z:.2f}<br>"
                    + f"{metric}: %{{customdata:.2f}}",
                    text=[f"#{i}" for i in range(n_points)],
                    customdata=colors,
                )
            ]
        )

        fig.update_layout(
            scene=dict(
                xaxis_title="Dimension 1",
                yaxis_title="Dimension 2",
                zaxis_title="Dimension 3",
            ),
            margin=dict(l=0, r=0, b=0, t=0),
            showlegend=False,
        )

        return fig

    @app.callback(
        Output("architecture-details", "children"),
        [Input("architecture-space-plot", "clickData")],
    )
    def display_architecture_details(clickData):
        """Display details for the selected architecture point.

        When a point is clicked in the 3D plot, fetches and displays:
        - Architecture specifications
        - Performance metrics
        - Component details

        Args:
            clickData (dict): Data about the clicked point from the plot

        Returns:
            List[Component]: Dash components showing architecture details

        Raises:
            PreventUpdate: If no point was clicked
        """
        if not clickData:
            return "Click a point to see architecture details"

        # TODO: Replace with actual architecture details from ResultsDB
        point_index = int(clickData["points"][0]["text"].replace("#", ""))

        return [
            html.H5(f"Architecture #{point_index}"),
            html.Hr(),
            html.P(
                [
                    html.Strong("Performance Metrics:"),
                    html.Br(),
                    f"Accuracy: {np.random.uniform(0.7, 0.95):.3f}",
                    html.Br(),
                    f"Loss: {np.random.uniform(0.1, 0.5):.3f}",
                    html.Br(),
                    f"Perplexity: {np.random.uniform(1.5, 4.0):.3f}",
                ]
            ),
            html.P(
                [
                    html.Strong("Architecture Components:"),
                    html.Br(),
                    "• Sparse Attention Layer",
                    html.Br(),
                    "• Feedback Connections",
                    html.Br(),
                    "• Cortical Column Inspired Structure",
                ]
            ),
        ]

    @app.callback(Output("launch-btn", "disabled"), [Input("launch-btn", "n_clicks")])
    def handle_experiment_launch(n_clicks):
        """Handle launching a new experiment.

        Triggered when the launch button is clicked. Will:
        1. Validate current parameter settings
        2. Submit new experiment to the backend
        3. Update UI to show experiment status

        Args:
            n_clicks (int): Number of times button has been clicked

        Returns:
            bool: Whether the button should be disabled
        """
        if n_clicks is None:
            return False

        # TODO: Implement experiment launch logic
        return False
