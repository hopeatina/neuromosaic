"""
frontend/__init__.py

This file indicates that 'frontend' is a Python package.
It provides access to the main dashboard functionality and its components.
The package handles visualization and interaction with the Neuromosaic
architecture search results.
"""

from neuromosaic.frontend.dashboard import create_dashboard, run_dashboard

__all__ = ["create_dashboard", "run_dashboard"]
