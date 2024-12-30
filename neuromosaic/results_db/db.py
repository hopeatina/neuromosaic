"""
Implementation of the results database interface using SQLAlchemy.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import logging
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.dialects.sqlite import insert

from .db_interface import ResultsDB as BaseResultsDB
from .models import Base, Architecture, Experiment, Run

logger = logging.getLogger(__name__)

_db_instance: Optional[BaseResultsDB] = None


def get_db_instance(config: Optional[Dict[str, Any]] = None) -> BaseResultsDB:
    """
    Get or create a database instance.

    Args:
        config: Optional Config object with database configuration

    Returns:
        BaseResultsDB: Database interface instance
    """
    global _db_instance

    if _db_instance is None:
        if config is None:
            raise RuntimeError("Database configuration not provided")
        _db_instance = ResultsDB(config)

    return _db_instance


class ResultsDB(BaseResultsDB):
    """Implementation of the results database interface using SQLAlchemy."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize the results database."""
        super().__init__(config)
        # Get database configuration
        if hasattr(config, "database"):
            db_config = config.database
            self.db_url = db_config.db_url
        else:
            db_config = config.get("database", {})
            self.db_url = db_config.get("db_url", "sqlite:///results.db")

        self.engine = create_engine(self.db_url, echo=False)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def _get_session(self) -> Session:
        """Get a new database session."""
        return self.Session()

    async def list_all_runs(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **filters,
    ) -> List[Dict[str, Any]]:
        """List all runs in the database."""
        with self._get_session() as session:
            query = session.query(Run)

            if start_date:
                query = query.filter(Run.timestamp >= start_date)
            if end_date:
                query = query.filter(Run.timestamp <= end_date)

            for key, value in filters.items():
                if hasattr(Run, key):
                    query = query.filter(getattr(Run, key) == value)

            runs = query.all()
            return [
                {
                    "id": run.id,
                    "experiment_id": run.experiment_id,
                    "architecture_id": run.architecture_id,
                    "metrics": json.loads(run.metrics) if run.metrics else {},
                    "timestamp": run.timestamp.isoformat() if run.timestamp else None,
                }
                for run in runs
            ]

    async def get_best_architectures(
        self, metric: str, limit: int = 10, **filters
    ) -> List[Dict[str, Any]]:
        """Get the best architectures based on a metric."""
        # Get all runs that match filters
        all_runs = await self.list_all_runs(**filters)

        # Filter out runs that have that metric and ensure it's numeric
        valid_runs = []
        for run in all_runs:
            val = run["metrics"].get(metric)
            if isinstance(val, (int, float)):
                valid_runs.append(run)

        # Sort descending by the metric
        valid_runs.sort(key=lambda r: r["metrics"][metric], reverse=True)

        # Return top N
        best = valid_runs[:limit]
        return [
            {"architecture_id": run["architecture_id"], "metrics": run["metrics"]}
            for run in best
        ]

    async def save_run_info(self, run_info: Dict[str, Any]) -> str:
        """Save run information to the database."""
        run_id = run_info.get("id", str(datetime.now().timestamp()))
        architecture_id = run_info["architecture_id"]

        with self._get_session() as session:
            # Upsert architecture if arch_spec is provided
            arch_spec = run_info.get("arch_spec")
            if arch_spec:
                stmt = insert(Architecture).values(
                    vector_hash=architecture_id,
                    arch_spec=json.dumps(arch_spec),
                    code_commit=run_info.get("code_commit"),
                )
                # On conflict do nothing (SQLite 3.24+)
                stmt = stmt.on_conflict_do_nothing(index_elements=["vector_hash"])
                session.execute(stmt)

            run = Run(
                id=run_id,
                experiment_id=run_info.get("experiment_id"),
                architecture_id=architecture_id,
                metrics=json.dumps(run_info["metrics"]),
                timestamp=datetime.now(),
            )
            session.add(run)
            session.commit()
        return run_id

    async def get_experiment_details(
        self, experiment_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get details of a specific experiment."""
        with self._get_session() as session:
            experiment = session.get(Experiment, experiment_id)
            if experiment is None:
                return None
            return {
                "id": experiment.id,
                "status": experiment.status,
                "start_time": (
                    experiment.start_time.isoformat() if experiment.start_time else None
                ),
                "end_time": (
                    experiment.end_time.isoformat() if experiment.end_time else None
                ),
                "config": json.loads(experiment.config) if experiment.config else {},
            }

    async def create_experiment(
        self, name: str, description: Optional[str], config: Dict[str, Any]
    ) -> str:
        """Create a new experiment."""
        experiment_id = str(datetime.now().timestamp())
        with self._get_session() as session:
            experiment = Experiment(
                id=experiment_id,
                status="created",
                start_time=datetime.now(),
                config=json.dumps({"name": name, "description": description, **config}),
            )
            session.add(experiment)
            session.commit()
        return experiment_id

    async def update_experiment_status(self, experiment_id: str, status: str) -> None:
        """Update the status of an experiment."""
        with self._get_session() as session:
            experiment = session.get(Experiment, experiment_id)
            if experiment:
                experiment.status = status
                if status == "completed":
                    experiment.end_time = datetime.now()
                session.commit()
            else:
                logger.warning(f"No experiment found with id={experiment_id}")

    async def delete_experiment(self, experiment_id: str) -> bool:
        """Delete an experiment."""
        with self._get_session() as session:
            experiment = session.get(Experiment, experiment_id)
            if experiment is None:
                return False
            session.delete(experiment)
            session.commit()
            return True

    async def get_experiment(self, experiment_id: str) -> Optional[Dict[str, Any]]:
        """Get experiment details by ID."""
        return await self.get_experiment_details(experiment_id)

    async def get_metrics(
        self,
        experiment_id: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        metric_names: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Get metrics with optional filtering."""
        with self._get_session() as session:
            query = session.query(Run)

            if experiment_id:
                query = query.filter_by(experiment_id=experiment_id)
            if start_time:
                query = query.filter(Run.timestamp >= start_time)
            if end_time:
                query = query.filter(Run.timestamp <= end_time)

            runs = query.all()
            metrics = []
            for run in runs:
                metric_data = json.loads(run.metrics) if run.metrics else {}
                if metric_names:
                    metric_data = {
                        k: v for k, v in metric_data.items() if k in metric_names
                    }
                metrics.append(
                    {
                        "experiment_id": run.experiment_id,
                        "metrics": metric_data,
                        "timestamp": (
                            run.timestamp.isoformat() if run.timestamp else None
                        ),
                    }
                )
            return metrics

    async def get_architecture(self, architecture_id: str) -> Optional[Dict[str, Any]]:
        """Get architecture details by ID."""
        with self._get_session() as session:
            architecture = session.get(Architecture, architecture_id)
            if architecture is None:
                return None
            return {
                "id": architecture.vector_hash,
                "arch_spec": json.loads(architecture.arch_spec),
                "code_commit": architecture.code_commit,
                "creation_time": architecture.creation_time.isoformat(),
            }

    async def list_architectures(
        self, skip: int = 0, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """List architectures with pagination."""
        with self._get_session() as session:
            architectures = (
                session.query(Architecture)
                .order_by(Architecture.creation_time.desc())
                .offset(skip)
                .limit(limit)
                .all()
            )
            return [
                {
                    "id": arch.vector_hash,
                    "arch_spec": json.loads(arch.arch_spec),
                    "code_commit": arch.code_commit,
                    "creation_time": arch.creation_time.isoformat(),
                }
                for arch in architectures
            ]

    async def list_experiments(
        self, skip: int = 0, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """List experiments with pagination."""
        with self._get_session() as session:
            experiments = (
                session.query(Experiment)
                .order_by(Experiment.start_time.desc())
                .offset(skip)
                .limit(limit)
                .all()
            )
            return [
                {
                    "id": exp.id,
                    "status": exp.status,
                    "start_time": (
                        exp.start_time.isoformat() if exp.start_time else None
                    ),
                    "end_time": exp.end_time.isoformat() if exp.end_time else None,
                    "config": json.loads(exp.config) if exp.config else {},
                }
                for exp in experiments
            ]
