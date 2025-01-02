"""
components/__init__.py

This file indicates that 'components' is a Python package for 
various dashboard UI parts. It provides access to the core building
blocks of the Neuromosaic dashboard:

- Layout: Overall dashboard structure and UI organization
- Callbacks: Interactive behavior handlers
- Plots: Visualization components and utilities

The components work together to create a cohesive and interactive
dashboard experience for exploring neural architecture search results.
"""

from neuromosaic.frontend.components.layout import create_layout
from neuromosaic.frontend.components.callbacks import register_callbacks
from neuromosaic.frontend.components.plots import (
    create_3d_scatter,
    create_metric_timeline,
    create_parallel_coordinates,
)

__all__ = [
    "create_layout",
    "register_callbacks",
    "create_3d_scatter",
    "create_metric_timeline",
    "create_parallel_coordinates",
]
