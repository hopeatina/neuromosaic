"""
Environment management module for Neuromosaic.

This module handles container and environment management for running experiments.
"""

from .container_manager import ContainerManager
from .providers import DockerContainerManager

__all__ = ["ContainerManager", "DockerContainerManager"]
