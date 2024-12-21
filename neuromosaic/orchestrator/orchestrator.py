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
from datetime import datetime

from ..arch_space import ArchitectureVector
from ..llm_code_gen import CodeGenerator
from ..env_manager import ContainerManager
from ..results_db.db_interface import ResultsDB
from ..results_db.db import ResultsDB as ResultsDBImpl
from ..utils.logging import setup_logger
from ..utils.version_control import VersionControl
from .interface import IOrchestrator
from .strategies import RandomSearch, BayesianOptimization

logger = setup_logger(__name__)

_orchestrator_instance: Optional[IOrchestrator] = None


def get_orchestrator_instance(config: Optional[Dict[str, Any]] = None) -> IOrchestrator:
    """
    Get or create an orchestrator instance.

    Args:
        config: Optional configuration for the orchestrator

    Returns:
        IOrchestrator: Orchestrator interface instance
    """
    global _orchestrator_instance

    if _orchestrator_instance is None:
        if config is None:
            # Create default config
            config = {
                "search_strategy": {
                    "type": "random",
                    "dimensions": 64,
                },
                "llm": {
                    "provider": "openai",
                    "model": "gpt-4",
                },
                "container": {
                    "runtime": "docker",
                    "device": "cpu",
                },
            }
        _orchestrator_instance = Orchestrator(config)

    return _orchestrator_instance


class Orchestrator(IOrchestrator):
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
        self._running_experiments: Dict[str, Dict[str, Any]] = {}

    def _setup_components(self) -> None:
        """Initialize all required components from configuration."""
        # Initialize search strategy
        if isinstance(self.config.search_strategy, RandomSearch):
            self._search_strategy = self.config.search_strategy
        elif isinstance(self.config.search_strategy, BayesianOptimization):
            self._search_strategy = self.config.search_strategy
        else:
            raise ValueError(
                f"Unknown search strategy type: {type(self.config.search_strategy)}"
            )

        # Initialize code generator if not already set (e.g. by tests)
        if not hasattr(self, "_code_generator"):
            # Skip OpenAI initialization in development mode
            if self.config.environment == "development":
                self._code_generator = None
            else:
                from ..llm_code_gen.providers import OpenAICodeGenerator

                self._code_generator = OpenAICodeGenerator(self.config.llm)

        # Initialize container manager if not already set (e.g. by tests)
        if not hasattr(self, "_container_manager"):
            from ..env_manager.providers import DockerContainerManager

            self._container_manager = DockerContainerManager(self.config.container)

        # Initialize results DB if not already set
        if not hasattr(self, "_results_db"):
            self._results_db = ResultsDBImpl(self.config)

        # Initialize version control if not already set
        if not hasattr(self, "_version_control"):
            self._version_control = VersionControl()

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

    def schedule_experiment(self, experiment_id: str) -> None:
        """Implementation of IOrchestrator.schedule_experiment."""
        if experiment_id in self._running_experiments:
            raise ValueError(f"Experiment {experiment_id} is already running")

        # Create experiment state
        self._running_experiments[experiment_id] = {
            "status": "scheduled",
            "start_time": None,
            "logs": [],
        }

        # Schedule the experiment to run asynchronously
        asyncio.create_task(self._run_experiment(experiment_id))

    def stop_experiment(self, experiment_id: str) -> None:
        """Implementation of IOrchestrator.stop_experiment."""
        if experiment_id not in self._running_experiments:
            raise ValueError(f"Experiment {experiment_id} is not running")

        # Update experiment state
        self._running_experiments[experiment_id]["status"] = "stopping"
        # TODO: Implement actual experiment stopping logic

    def get_experiment_status(self, experiment_id: str) -> Dict[str, Any]:
        """Implementation of IOrchestrator.get_experiment_status."""
        if experiment_id not in self._running_experiments:
            raise ValueError(f"Experiment {experiment_id} not found")

        return self._running_experiments[experiment_id]

    def list_running_experiments(self) -> List[str]:
        """Implementation of IOrchestrator.list_running_experiments."""
        return list(self._running_experiments.keys())

    def get_experiment_logs(
        self, experiment_id: str, start_time: Optional[str] = None
    ) -> List[str]:
        """Implementation of IOrchestrator.get_experiment_logs."""
        if experiment_id not in self._running_experiments:
            raise ValueError(f"Experiment {experiment_id} not found")

        logs = self._running_experiments[experiment_id]["logs"]
        if start_time:
            start_dt = datetime.fromisoformat(start_time)
            return [log for log in logs if log["timestamp"] > start_dt]
        return logs

    async def _run_experiment(self, experiment_id: str) -> None:
        """
        Internal method to run an experiment.

        Args:
            experiment_id: Unique identifier for the experiment
        """
        try:
            # Update experiment state
            self._running_experiments[experiment_id].update(
                {
                    "status": "running",
                    "start_time": datetime.utcnow().isoformat(),
                }
            )

            # Run the experiment cycle
            results = await self.run_cycle()

            # Update experiment state with success
            self._running_experiments[experiment_id].update(
                {
                    "status": "completed",
                    "results": results,
                }
            )

        except Exception as e:
            # Update experiment state with failure
            self._running_experiments[experiment_id].update(
                {
                    "status": "failed",
                    "error": str(e),
                }
            )
            logger.error(f"Experiment {experiment_id} failed: {str(e)}")
