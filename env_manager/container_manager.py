"""
Container management for isolated experiment execution.
"""

from typing import Dict, Any, Optional
from abc import ABC, abstractmethod


class ContainerManager(ABC):
    """
    Abstract base class for container management.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    async def create_container(self, spec: Dict[str, Any]) -> str:
        """Create a new container with given specifications."""
        pass

    @abstractmethod
    async def run_container(self, container_id: str, command: str) -> Dict[str, Any]:
        """Run a command in the specified container."""
        pass

    @abstractmethod
    async def cleanup_container(self, container_id: str) -> None:
        """Clean up a container after experiment completion."""
        pass
