"""
Main orchestrator class that manages the neural architecture search lifecycle.

The Orchestrator is the central control unit of the neural architecture search process.
It coordinates between different components:
- Requests new architectures from search strategies
- Triggers code generation via LLM
- Schedules training runs in containers
- Records and analyzes results

Example:
    >>> config = Config()
    >>> orchestrator = Orchestrator(config)
    >>> orchestrator.run_cycle()  # Runs one complete search cycle
"""

from typing import Dict, Any, Optional, List
from pathlib import Path
import asyncio
import logging

from ..arch_space import ArchitectureVector
from ..llm_code_gen import CodeGenerator
from ..env_manager import ContainerManager
from ..results_db import ResultsDB
from ..utils.logging import setup_logger
from ..utils.version_control import VersionControl

logger = setup_logger(__name__)


class Orchestrator:
    """
    Manages the lifecycle of experiments: requests new architectures,
    triggers code generation, schedules training runs, and records results.

    The orchestrator implements the main control loop of the architecture search:
    1. Get next architecture from search strategy
    2. Generate code via LLM
    3. Run experiment in container
    4. Record results and update search strategy

    Attributes:
        config (Dict[str, Any]): Configuration dictionary containing:
            - search_strategy: Strategy class name or instance
            - llm_provider: LLM provider configuration
            - container_config: Container runtime settings
            - experiment_defaults: Default training parameters
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the orchestrator with configuration.

        Args:
            config: Configuration dictionary with all necessary settings
        """
        self.config = config
        self._setup_components()

    def _setup_components(self) -> None:
        """Initialize all required components from configuration."""
        # Initialize search strategy
        strategy_type = self.config._config.get("search_strategy", {}).get(
            "type", "random"
        )
        if strategy_type == "random":
            from .strategies import RandomSearch

            self._search_strategy = RandomSearch(
                self.config._config.get("search_strategy", {})
            )
        elif strategy_type == "bayesian_optimization":
            from .strategies import BayesianOptimization

            self._search_strategy = BayesianOptimization(
                self.config._config.get("search_strategy", {})
            )
        else:
            raise ValueError(f"Unknown search strategy type: {strategy_type}")

        # Initialize code generator if not already set (e.g. by tests)
        if not hasattr(self, "_code_generator"):
            llm_config = self.config._config.get("llm", {})
            provider = llm_config.get("provider", "openai")

            if provider == "openai":
                from ..llm_code_gen.providers import OpenAICodeGenerator

                self._code_generator = OpenAICodeGenerator(llm_config)
            else:
                raise ValueError(f"Unknown LLM provider: {provider}")

        # Initialize container manager if not already set (e.g. by tests)
        if not hasattr(self, "_container_manager"):
            container_config = self.config._config.get("container", {})
            runtime = container_config.get("runtime", "docker")

            if runtime == "docker":
                from ..env_manager.providers import DockerContainerManager

                self._container_manager = DockerContainerManager(container_config)
            else:
                raise ValueError(f"Unknown container runtime: {runtime}")

    @property
    def code_generator(self) -> CodeGenerator:
        """Get the code generator instance."""
        return self._code_generator

    @code_generator.setter
    def code_generator(self, generator: CodeGenerator) -> None:
        """Set the code generator instance."""
        self._code_generator = generator

    @property
    def container_manager(self) -> ContainerManager:
        """Get the container manager instance."""
        return self._container_manager

    @container_manager.setter
    def container_manager(self, manager: ContainerManager) -> None:
        """Set the container manager instance."""
        self._container_manager = manager

    async def run_cycle(self) -> Dict[str, Any]:
        """
        Run a single cycle of the neural architecture search.

        A cycle consists of:
        1. Getting next architecture to evaluate
        2. Generating implementation code
        3. Running the experiment
        4. Recording results

        Returns:
            Dict containing cycle results including:
            - architecture_id: Unique identifier for the architecture
            - metrics: Performance metrics from training
            - code_version: Git commit hash of generated code

        Raises:
            RuntimeError: If any component fails critically
        """
        try:
            # Get next architecture
            arch_info = await self.get_next_architecture()
            arch_vector = arch_info["vector"]
            arch_spec = arch_vector.decode()

            # Generate code
            code = await self._code_generator.generate_code(arch_spec)

            # Save code and get version
            code_version = await self._version_control.commit_code(code)

            # Create and run container
            container_id = await self._container_manager.create_container(code)
            try:
                run_results = await self._container_manager.run_container(container_id)
                if run_results["status"] != "success":
                    raise RuntimeError(f"Container run failed: {run_results}")

                # Process and store results
                metrics = run_results["results"]
                architecture_id = f"arch_{code_version[:8]}"

                results = {
                    "architecture_id": architecture_id,
                    "metrics": metrics,
                    "code_version": code_version,
                    "arch_spec": arch_spec,
                }

                await self.submit_results(results)
                return results

            finally:
                # Always cleanup container
                await self._container_manager.cleanup_container(container_id)

        except Exception as e:
            logger.error(f"Cycle failed: {str(e)}")
            raise

    async def get_next_architecture(self) -> Dict[str, Any]:
        """
        Get the next architecture to evaluate from the search strategy.

        Returns:
            Dict containing:
            - vector: The architecture vector
            - metadata: Any strategy-specific metadata

        Raises:
            ValueError: If strategy returns invalid architecture
        """
        # Get next architecture from search strategy
        arch_vector = await self._search_strategy.suggest_architecture()

        # Validate the architecture
        if not isinstance(arch_vector, ArchitectureVector):
            raise ValueError("Strategy returned invalid architecture type")

        # Return with optional metadata
        return {
            "vector": arch_vector,
            "metadata": {
                "strategy": self._search_strategy.__class__.__name__,
                "iteration": len(self._search_strategy.history),
            },
        }

    async def submit_results(self, results: Dict[str, Any]) -> None:
        """
        Submit results from a completed experiment.

        Args:
            results: Dictionary containing:
                - architecture_id: ID of the evaluated architecture
                - metrics: Dictionary of performance metrics
                - training_time: Time taken for training
                - resource_usage: CPU/GPU/memory usage stats
        """
        # Validate required fields
        required_fields = ["architecture_id", "metrics"]
        for field in required_fields:
            if field not in results:
                raise ValueError(f"Missing required field in results: {field}")

        # Store results in database
        await self._results_db.save_run_info(results)

        # Update search strategy with results
        await self._search_strategy.update_with_results(results)

        # Log results summary
        logger.info(f"Stored results for architecture {results['architecture_id']}")
        logger.info(f"Metrics: {results['metrics']}")

    async def run_batch(
        self, batch_size: int, parallel: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Run multiple architecture evaluations in parallel.

        Args:
            batch_size: Number of architectures to evaluate
            parallel: If True, run evaluations concurrently

        Returns:
            List of results from each evaluation
        """
        # Create tasks for each evaluation
        tasks = [self.run_cycle() for _ in range(batch_size)]

        if parallel:
            # Run evaluations concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Handle any exceptions
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"Batch task {i} failed: {str(result)}")
                    results[i] = {"status": "failed", "error": str(result)}
        else:
            # Run evaluations sequentially
            results = []
            for i, task in enumerate(tasks):
                try:
                    result = await task
                    results.append(result)
                except Exception as e:
                    logger.error(f"Batch task {i} failed: {str(e)}")
                    results.append({"status": "failed", "error": str(e)})

        return results
