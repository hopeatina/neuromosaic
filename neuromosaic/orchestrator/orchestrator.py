"""
Main orchestrator class that manages the neural architecture search lifecycle.

The Orchestrator is the central control unit of the neural architecture search process.
It coordinates between different components:
- Requests new architectures from search strategies
- Triggers code generation via LLM
- Schedules training runs in containers
- Records and analyzes results

Improvements:
- Enhanced error handling and logging
- Resilient concurrency in run_batch
- Strict checks on missing fields or invalid returns
"""

from typing import Dict, Any, Optional, List, Union, TYPE_CHECKING
from pathlib import Path
import asyncio
import logging
from datetime import datetime
from dataclasses import asdict

from ..arch_space import ArchitectureVector
from ..llm_code_gen import CodeGenerator
from ..env_manager import ContainerManager
from ..results_db.db import ResultsDB as ResultsDBImpl
from ..utils.logging import setup_logger
from ..utils.version_control import VersionControl
from .interface import IOrchestrator

# Use TYPE_CHECKING to avoid circular imports
if TYPE_CHECKING:
    from ..utils.config import Config
    from .strategies import RandomSearch, BayesianOptimization

logger = setup_logger(__name__)

_orchestrator_instance: Optional[IOrchestrator] = None


def get_orchestrator_instance(
    config: Optional[Union[Dict[str, Any], "Config"]] = None
) -> IOrchestrator:
    """
    Get or create a global orchestrator instance (singleton pattern).

    Args:
        config: Optional configuration for the orchestrator (dict or Config object).

    Returns:
        IOrchestrator: The orchestrator interface instance.

    Notes:
        - If config is None, we load default config from environment.
        - If config is a dict, we create a base config from environment and potentially
          merge the dict (skipped in this minimal example).
    """
    global _orchestrator_instance

    if _orchestrator_instance is None:
        if config is None:
            from ..utils.config import Config

            config = Config.from_env()
        elif isinstance(config, dict):
            from ..utils.config import Config

            base_config = Config.from_env()
            # TODO: merge config dict with base_config if desired
            config = base_config

        _orchestrator_instance = Orchestrator(config)

    return _orchestrator_instance


class Orchestrator(IOrchestrator):
    """
    Manages the lifecycle of experiments: requests new architectures,
    triggers code generation, schedules training runs, and records results.

    Steps in the main loop:
        1) get_next_architecture() from search strategy
        2) generate_code() via LLM provider
        3) run experiment in container
        4) record results, update strategy

    Attributes:
        config (Config): Configuration object with search_strategy, llm, container, etc.
    """

    def __init__(self, config: "Config"):
        """
        Initialize the orchestrator with configuration.

        Args:
            config: Configuration object with all necessary settings.
        """
        self.config = config
        self._setup_components()
        # Track actively running or scheduled experiments
        self._running_experiments: Dict[str, Dict[str, Any]] = {}

    def _setup_components(self) -> None:
        """
        Initialize all required components from configuration:
        - search_strategy
        - code_generator
        - container_manager
        - results DB
        - version control

        Uses lazy imports to avoid circular dependencies.
        """
        from .strategies import RandomSearch, BayesianOptimization

        # 1. Search Strategy
        if isinstance(
            self.config.search_strategy, (RandomSearch, BayesianOptimization)
        ):
            self._search_strategy = self.config.search_strategy
        else:
            strategy_config = self.config.search_strategy
            strategy_type = strategy_config.get("type", "bayesian_optimization")

            if strategy_type == "random":
                self._search_strategy = RandomSearch(strategy_config)
            elif strategy_type == "bayesian_optimization":
                self._search_strategy = BayesianOptimization(strategy_config)
            else:
                raise ValueError(f"Unknown search strategy type: {strategy_type}")

        # 2. Code Generator
        if not hasattr(self, "_code_generator"):
            from ..llm_code_gen.providers import (
                MockCodeGenerator,
                OpenAICodeGenerator,
                LlamaCodeGenerator,
            )

            if self.config.environment == "development":
                # Use a mock generator in dev mode
                self._code_generator = LlamaCodeGenerator(asdict(self.config.llm))
            else:
                provider = self.config.llm.get("provider", "openai")
                if provider == "openai":
                    self._code_generator = OpenAICodeGenerator(asdict(self.config.llm))
                elif provider == "llama":
                    self._code_generator = LlamaCodeGenerator(asdict(self.config.llm))
                else:
                    raise ValueError(f"Unknown LLM provider: {provider}")
            logger.info(
                "Initialized code generator: %s",
                self._code_generator.__class__.__name__,
            )

        # 3. Container Manager
        if not hasattr(self, "_container_manager"):
            from ..env_manager.providers import DockerContainerManager

            self._container_manager = DockerContainerManager(self.config.container)

        # 4. Results DB
        if not hasattr(self, "_results_db"):
            self._results_db = ResultsDBImpl(self.config)

        # 5. Version Control
        if not hasattr(self, "_version_control"):
            self._version_control = VersionControl()

    @property
    def code_generator(self) -> CodeGenerator:
        """Returns the code generator instance."""
        return self._code_generator

    @code_generator.setter
    def code_generator(self, generator: CodeGenerator) -> None:
        """Sets the code generator instance."""
        self._code_generator = generator

    @property
    def container_manager(self) -> ContainerManager:
        """Returns the container manager instance."""
        return self._container_manager

    @container_manager.setter
    def container_manager(self, manager: ContainerManager) -> None:
        """Sets the container manager instance."""
        self._container_manager = manager

    async def run_cycle(self) -> Dict[str, Any]:
        """
        Run a single cycle of the neural architecture search.

        Steps:
            1) get_next_architecture()
            2) generate_code()
            3) create & run container
            4) store results, update strategy

        Returns:
            Dictionary with keys:
                - architecture_id
                - metrics
                - code_version
                - arch_spec

        Raises:
            RuntimeError: If any sub-step fails.
        """
        try:
            arch_info = await self.get_next_architecture()  # step 1
            arch_vector = arch_info["vector"]
            arch_spec = arch_vector.decode()

            # Generate code (step 2)
            code = await self._code_generator.generate_code(arch_spec)

            # Commit code to version control
            code_version = await self._version_control.commit_code(code)

            # Create container (step 3)
            container_spec = {
                "code": code,
                # Potentially add "requirements" or "data_path"
                # or environment overrides if needed
            }
            container_id = await self._container_manager.create_container(
                container_spec
            )

            try:
                run_results = await self._container_manager.run_container(container_id)
                if run_results["status"] != "success":
                    # We consider this a critical error
                    raise RuntimeError(f"Container run failed: {run_results}")

                # Step 4: process results
                metrics = run_results.get("results", {})
                architecture_id = f"arch_{code_version[:8]}"

                final_results = {
                    "architecture_id": architecture_id,
                    "metrics": metrics,
                    "code_version": code_version,
                    "arch_spec": arch_spec,
                }
                await self.submit_results(final_results)
                return final_results

            finally:
                # Always attempt to clean up container
                await self._container_manager.cleanup_container(container_id)

        except Exception as e:
            logger.error(f"run_cycle failed: {e}")
            raise

    async def get_next_architecture(self) -> Dict[str, Any]:
        """
        Retrieves the next architecture to evaluate from the search strategy.

        Returns:
            A dictionary with:
                - vector: ArchitectureVector
                - metadata: dict with strategy name, iteration, etc.

        Raises:
            ValueError: If the strategy returns an invalid type (not ArchitectureVector).
        """
        arch_vector = await self._search_strategy.suggest_architecture()
        if not isinstance(arch_vector, ArchitectureVector):
            raise ValueError("Strategy returned invalid architecture type")

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

        Required fields in 'results':
            - architecture_id
            - metrics

        Steps:
            1) Save run info to DB
            2) Update search strategy with results
            3) Log outcome

        Raises:
            ValueError: If required fields are missing.
            Any DB or search strategy exceptions that might bubble up.
        """
        required_fields = ["architecture_id", "metrics"]
        for field in required_fields:
            if field not in results:
                raise ValueError(f"submit_results: missing required field '{field}'")

        # Persist results
        await self._results_db.save_run_info(results)

        # Update search strategy with outcome
        await self._search_strategy.update_with_results(results)

        # Logging
        logger.info(f"Submitted results for {results['architecture_id']}")
        logger.info(f"Metrics: {results['metrics']}")

    async def run_batch(
        self, batch_size: int, parallel: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Run multiple architecture evaluations in batch.

        Args:
            batch_size (int): Number of architectures to evaluate
            parallel (bool): If True, run all cycles concurrently.
                             If False, run them sequentially.

        Returns:
            A list of results dictionaries. Each element may be either:
                - A successful results dict from run_cycle(), or
                - A dict with status="failed" and an "error" message
                  if that particular cycle failed.

        Notes:
            - Even if parallel=True, some tasks might fail while others succeed.
        """
        tasks = [self.run_cycle() for _ in range(batch_size)]

        if parallel:
            # Run concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for i, r in enumerate(results):
                if isinstance(r, Exception):
                    logger.error(f"Parallel run {i} failed: {r}")
                    results[i] = {"status": "failed", "error": str(r)}
            return results
        else:
            # Run sequentially to avoid partial failures messing concurrency
            aggregated = []
            for i, task in enumerate(tasks):
                try:
                    res = await task
                    aggregated.append(res)
                except Exception as e:
                    logger.error(f"Sequential run {i} failed: {e}")
                    aggregated.append({"status": "failed", "error": str(e)})
            return aggregated

    def schedule_experiment(self, experiment_id: str) -> None:
        """
        Schedule an experiment asynchronously, tracking status in self._running_experiments.

        Args:
            experiment_id (str): Unique identifier for the scheduled experiment.

        Raises:
            ValueError: If experiment is already running or scheduled.
        """
        if experiment_id in self._running_experiments:
            raise ValueError(
                f"Experiment {experiment_id} is already running or scheduled"
            )

        self._running_experiments[experiment_id] = {
            "status": "scheduled",
            "start_time": None,
            "logs": [],
        }

        asyncio.create_task(self._run_experiment(experiment_id))

    async def _run_experiment(self, experiment_id: str) -> None:
        """
        Internal method to run a scheduled experiment.
        Updates the experiment's status as it goes.

        Args:
            experiment_id: The ID of the experiment to run.

        Raises:
            Exceptions bubble up but are caught to mark experiment as failed in state.
        """
        try:
            self._running_experiments[experiment_id]["status"] = "running"
            self._running_experiments[experiment_id][
                "start_time"
            ] = datetime.utcnow().isoformat()

            result = await self.run_cycle()

            self._running_experiments[experiment_id]["status"] = "completed"
            self._running_experiments[experiment_id]["results"] = result

        except Exception as e:
            self._running_experiments[experiment_id]["status"] = "failed"
            self._running_experiments[experiment_id]["error"] = str(e)
            logger.error(f"Experiment {experiment_id} failed: {e}")

    def stop_experiment(self, experiment_id: str) -> None:
        """
        Mark experiment as stopping (TODO: actual container or job cancellation).

        Args:
            experiment_id: ID of the experiment.

        Raises:
            ValueError: If experiment is not found in _running_experiments.
        """
        if experiment_id not in self._running_experiments:
            raise ValueError(f"Experiment {experiment_id} is not running or scheduled")

        self._running_experiments[experiment_id]["status"] = "stopping"
        # TODO: implement actual container/job stop logic if feasible

    def get_experiment_status(self, experiment_id: str) -> Dict[str, Any]:
        """
        Retrieve the current status of a running or scheduled experiment.

        Args:
            experiment_id: ID of the experiment.

        Returns:
            A dictionary with keys like 'status', 'start_time', 'results', 'error', etc.

        Raises:
            ValueError: If the experiment ID is unknown.
        """
        if experiment_id not in self._running_experiments:
            raise ValueError(f"Experiment {experiment_id} not found")
        return self._running_experiments[experiment_id]

    def list_running_experiments(self) -> List[str]:
        """
        List all experiment IDs currently tracked (running or scheduled).

        Returns:
            A list of experiment IDs.
        """
        return list(self._running_experiments.keys())

    def get_experiment_logs(
        self, experiment_id: str, start_time: Optional[str] = None
    ) -> List[str]:
        """
        Fetch logs for a given experiment from the local tracking dictionary.

        Args:
            experiment_id: ID of the experiment
            start_time: If provided, only return logs after that timestamp.

        Returns:
            A list of log entries (strings).
        """
        if experiment_id not in self._running_experiments:
            raise ValueError(f"Experiment {experiment_id} not found")

        logs = self._running_experiments[experiment_id]["logs"]
        if start_time:
            dt = datetime.fromisoformat(start_time)
            return [l for l in logs if l["timestamp"] > dt]
        return logs
