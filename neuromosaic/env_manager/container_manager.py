"""
Container management for isolated experiment execution.
"""

import logging
from typing import Dict, Any
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class ContainerManager(ABC):
    """
    Abstract base class for container management.
    Provides interface for creating, running, and cleaning up containers
    for experiment execution.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize container manager with configuration.

        Args:
            config: Dictionary containing container-specific settings such as:
                - base_image: Base container image to use
                - gpu: Whether to enable GPU support
                - memory_limit: Container memory limit
                - timeout: Container execution timeout
                - network: Network configuration
                - environment: Environment variables dict
                - health_check: Health check configuration
        """
        self.config = config
        self.image = config.get("base_image")
        self.gpu = config.get("gpu", False)
        self.memory_limit = config.get("memory_limit")
        self.timeout = config.get("timeout", 3600)  # 1 hour default
        self.network = config.get("network")
        self.environment = config.get("environment", {})
        self.health_check = config.get("health_check", {})
        self._validate_config()

    def _validate_config(self) -> None:
        """Validate the configuration parameters."""
        if not self.image:
            raise ValueError("Container base_image must be specified in config")

        if self.memory_limit and not isinstance(self.memory_limit, (int, str)):
            raise ValueError("Memory limit must be an integer or string")

        if not isinstance(self.timeout, (int, float)):
            raise ValueError("Timeout must be a number")

        if not isinstance(self.environment, dict):
            raise ValueError("Environment must be a dictionary")

    def _validate_spec(self, spec: Dict[str, Any]) -> None:
        """Validate the container specification."""
        required_fields = ["code"]
        missing_fields = [field for field in required_fields if field not in spec]
        if missing_fields:
            raise ValueError(f"Missing required fields in spec: {missing_fields}")

        if "environment" in spec and not isinstance(spec["environment"], dict):
            raise ValueError("Environment in spec must be a dictionary")

    @abstractmethod
    async def create_container(self, spec: Dict[str, Any]) -> str:
        """
        Create a new container for experiment execution.

        Args:
            spec: Dictionary containing:
                - code: Code to execute
                - requirements: Package requirements
                - data_path: Path to mount training data
                - environment: Additional environment variables
                - network: Custom network settings

        Returns:
            Container ID as string

        Raises:
            RuntimeError: If container creation fails
        """
        self._validate_spec(spec)

    @abstractmethod
    async def run_container(
        self, container_id: str, command: str = "python main.py"
    ) -> Dict[str, Any]:
        """
        Run a command in the specified container.

        Args:
            container_id: ID of container to run command in
            command: Command to execute

        Returns:
            Dictionary containing:
                - status: "success" or "error"
                - output: Command output
                - error: Error message if status is "error"
                - exit_code: Command exit code
                - metrics: Resource usage metrics
                - execution_time: Time taken to execute

        Raises:
            RuntimeError: If command execution fails
        """
        pass

    @abstractmethod
    async def cleanup_container(self, container_id: str) -> None:
        """
        Clean up a container after experiment completion.

        Args:
            container_id: ID of container to clean up

        Raises:
            RuntimeError: If cleanup fails
        """
        pass
