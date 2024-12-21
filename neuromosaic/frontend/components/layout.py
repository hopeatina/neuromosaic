"""
layout.py

Defines the top-level Dash layout for the NeuraMosaic dashboard.
Organizes main containers, sidebars, and placeholders for interactive
plots and data displays. The layout is built using Bootstrap components
for a responsive and modern design.

The layout is organized into several main sections:
- Control sidebar with filters and experiment launch
- Main visualization area with 3D architecture space
- Detail panels for experiment information
"""

from dash import html, dcc
import dash_bootstrap_components as dbc


def create_sidebar():
    """Create the sidebar with controls and filters.

    The sidebar contains:
    - Metric selection dropdown
    - Architecture space complexity filter
    - Experiment launch controls

    Returns:
        dbc.Col: A Bootstrap column containing the sidebar elements
    """
    return dbc.Col(
        [
            html.H4("Controls", className="mb-3"),
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5("Experiment Filters", className="mb-3"),
                        dcc.Dropdown(
                            id="metric-selector",
                            options=[
                                {"label": "Accuracy", "value": "accuracy"},
                                {"label": "Loss", "value": "loss"},
                                {"label": "Perplexity", "value": "perplexity"},
                            ],
                            value="accuracy",
                            className="mb-3",
                        ),
                        html.H5("Architecture Space", className="mb-3"),
                        dcc.RangeSlider(
                            id="complexity-range",
                            min=0,
                            max=100,
                            step=1,
                            value=[0, 100],
                            marks={0: "Simple", 50: "Medium", 100: "Complex"},
                            className="mb-3",
                        ),
                        dbc.Button(
                            "Launch Experiment",
                            id="launch-btn",
                            color="primary",
                            className="w-100",
                        ),
                    ]
                )
            ),
        ],
        width=3,
        className="bg-light",
    )


def create_main_content():
    """Create the main content area with visualizations.

    The main content includes:
    - 3D scatter plot of the architecture space
    - Detailed view of selected architectures
    - Performance metrics and analysis

    Returns:
        dbc.Col: A Bootstrap column containing the main content elements
    """
    return dbc.Col(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H3("Architecture Search Space", className="mb-3"),
                            dcc.Graph(
                                id="architecture-space-plot",
                                style={"height": "600px"},
                                config={
                                    "displayModeBar": True,
                                    "scrollZoom": True,
                                },
                            ),
                        ]
                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H4("Selected Architecture Details", className="mb-3"),
                            html.Div(id="architecture-details"),
                        ]
                    )
                ]
            ),
        ],
        width=9,
    )


def create_layout():
    """Create the main dashboard layout.

    Assembles the complete dashboard layout by combining:
    - Header with title
    - Sidebar with controls
    - Main content area with visualizations

    Returns:
        dbc.Container: The complete dashboard layout wrapped in a Bootstrap container
    """
    return dbc.Container(
        [
            dbc.Row([html.H1("Neuromosaic Dashboard", className="text-center mb-4")]),
            dbc.Row([create_sidebar(), create_main_content()]),
        ],
        fluid=True,
        className="p-4",
    )
