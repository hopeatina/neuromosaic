"""
dashboard.py

This file initializes the Dash application for the NeuraMosaic frontend.
It sets up the layout, registers the callbacks, and provides an entry point
to run the server. The dashboard provides an interactive visualization of
the architecture search space and experiment results.

Key Features:
- 3D visualization of architecture search space
- Real-time experiment monitoring
- Interactive architecture exploration
- Metric visualization and comparison
"""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from neuromosaic.frontend.components.layout import create_layout
from neuromosaic.frontend.components.callbacks import register_callbacks


def create_dashboard(debug=False):
    """Create and configure the Dash application.

    This function initializes a new Dash application with the appropriate
    theme, layout, and callbacks. It serves as the main entry point for
    creating the dashboard interface.

    Args:
        debug (bool): Whether to run the app in debug mode. Enables hot reloading
                     and more detailed error messages.

    Returns:
        dash.Dash: Configured dashboard application ready to be served.
    """
    app = dash.Dash(
        __name__,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        title="Neuromosaic Dashboard",
        suppress_callback_exceptions=True,
    )

    app.layout = create_layout()
    register_callbacks(app)

    return app


def run_dashboard(host="0.0.0.0", port=8050, debug=False):
    """Run the dashboard server.

    This function creates and starts the Dash server with the specified
    configuration. It's the main function called by the CLI to launch
    the dashboard interface.

    Args:
        host (str): Host to run the server on. Defaults to "0.0.0.0" for
                   access from any network interface.
        port (int): Port to run the server on. Defaults to 8050, the
                   standard Dash port.
        debug (bool): Whether to run in debug mode. Enables features like
                     hot reloading and detailed error messages.
    """
    app = create_dashboard(debug=debug)
    app.run_server(host=host, port=port, debug=debug)


if __name__ == "__main__":
    run_dashboard()
