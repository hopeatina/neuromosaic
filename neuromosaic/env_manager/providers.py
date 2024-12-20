"""
Docker-based container management implementation.
"""

import asyncio
import logging
from typing import Dict, Any, Optional
import docker
from docker.errors import DockerException

from .container_manager import ContainerManager
from ..utils.logging import setup_logger

logger = setup_logger(__name__)


class DockerContainerManager(ContainerManager):
    """
    Docker-based implementation of container management.

    Handles creation, execution, and cleanup of Docker containers for running
    neural architecture experiments.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Docker client and configuration.

        Args:
            config: Dictionary containing Docker-specific settings:
                - image: Base Docker image to use
                - gpu: Whether to enable GPU support
                - memory_limit: Container memory limit
                - timeout: Container execution timeout
        """
        super().__init__(config)
        self.client = docker.from_env()
        self.image = config.get("image", "python:3.9")
        self.gpu = config.get("gpu", False)
        self.memory_limit = config.get("memory_limit", "4g")
        self.timeout = config.get("timeout", 3600)  # 1 hour default

    async def create_container(self, spec: Dict[str, Any]) -> str:
        """
        Create a new Docker container for experiment execution.

        Args:
            spec: Dictionary containing:
                - code: Python code to execute
                - requirements: Python package requirements
                - data_path: Path to mount training data

        Returns:
            Container ID as string

        Raises:
            RuntimeError: If container creation fails
        """
        try:
            # Create container config
            container_config = {
                "image": self.image,
                "command": "sleep infinity",  # Keep container running
                "detach": True,
                "mem_limit": self.memory_limit,
                "working_dir": "/workspace",
                "volumes": {
                    spec.get("data_path", "/tmp"): {"bind": "/data", "mode": "ro"}
                },
            }

            # Add GPU configuration if enabled
            if self.gpu:
                container_config["device_requests"] = [
                    docker.types.DeviceRequest(count=-1, capabilities=[["gpu"]])
                ]

            # Create and start container
            container = self.client.containers.run(**container_config)
            logger.info(f"Created container {container.id[:12]}")

            # Copy code and requirements
            self._copy_to_container(container.id, spec["code"], "/workspace/main.py")
            if "requirements" in spec:
                self._copy_to_container(
                    container.id, spec["requirements"], "/workspace/requirements.txt"
                )
                # Install requirements
                exit_code, output = container.exec_run(
                    "pip install -r requirements.txt", workdir="/workspace"
                )
                if exit_code != 0:
                    raise RuntimeError(f"Failed to install requirements: {output}")

            return container.id

        except DockerException as e:
            logger.error(f"Failed to create container: {str(e)}")
            raise RuntimeError(f"Container creation failed: {str(e)}")

    async def run_container(
        self, container_id: str, command: str = "python main.py"
    ) -> Dict[str, Any]:
        """
        Run a command in the specified container.

        Args:
            container_id: ID of container to run command in
            command: Command to execute (defaults to running main.py)

        Returns:
            Dictionary containing:
                - status: "success" or "error"
                - output: Command output
                - error: Error message if status is "error"
                - exit_code: Command exit code

        Raises:
            RuntimeError: If command execution fails
        """
        try:
            container = self.client.containers.get(container_id)

            # Execute command with timeout
            exit_code, output = container.exec_run(
                command, workdir="/workspace", demux=True
            )

            if exit_code != 0:
                logger.error(f"Command failed with exit code {exit_code}")
                return {
                    "status": "error",
                    "error": output[1].decode() if output[1] else "Unknown error",
                    "exit_code": exit_code,
                }

            return {
                "status": "success",
                "output": output[0].decode() if output[0] else "",
                "exit_code": exit_code,
            }

        except DockerException as e:
            logger.error(f"Failed to run container: {str(e)}")
            raise RuntimeError(f"Container execution failed: {str(e)}")

    async def cleanup_container(self, container_id: str) -> None:
        """
        Clean up a container after experiment completion.

        Args:
            container_id: ID of container to clean up

        Raises:
            RuntimeError: If cleanup fails
        """
        try:
            container = self.client.containers.get(container_id)
            container.stop(timeout=10)
            container.remove(force=True)
            logger.info(f"Cleaned up container {container_id[:12]}")

        except DockerException as e:
            logger.error(f"Failed to cleanup container: {str(e)}")
            raise RuntimeError(f"Container cleanup failed: {str(e)}")

    def _copy_to_container(
        self, container_id: str, content: str, dest_path: str
    ) -> None:
        """
        Helper method to copy content into a container.

        Args:
            container_id: Target container ID
            content: Content to copy
            dest_path: Destination path in container

        Raises:
            RuntimeError: If copy operation fails
        """
        try:
            container = self.client.containers.get(container_id)
            container.put_archive(
                "/workspace",
                self._create_tar(dest_path.split("/")[-1], content.encode()),
            )
        except DockerException as e:
            raise RuntimeError(f"Failed to copy to container: {str(e)}")

    def _create_tar(self, name: str, content: bytes) -> bytes:
        """
        Create a tar archive containing a single file.

        Args:
            name: Name of file in archive
            content: File content as bytes

        Returns:
            Tar archive as bytes
        """
        import tarfile
        import io

        tar_stream = io.BytesIO()
        with tarfile.open(fileobj=tar_stream, mode="w:gz") as tar:
            file_data = io.BytesIO(content)
            info = tarfile.TarInfo(name=name)
            info.size = len(content)
            tar.addfile(info, file_data)

        return tar_stream.getvalue()
