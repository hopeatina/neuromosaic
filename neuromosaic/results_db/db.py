"""
Implementation of the results database interface.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import sqlite3
import json

from .db_interface import ResultsDB as BaseResultsDB


_db_instance: Optional[BaseResultsDB] = None


def get_db_instance(config: Optional[Dict[str, Any]] = None) -> BaseResultsDB:
    """
    Get or create a database instance.

    Args:
        config: Optional database configuration

    Returns:
        BaseResultsDB: Database interface instance
    """
    global _db_instance

    if _db_instance is None:
        _db_instance = ResultsDB(config or {})

    return _db_instance


class ResultsDB(BaseResultsDB):
    """Implementation of the results database interface."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize the results database."""
        super().__init__(config)
        self.db_path = config.database.db_url.replace("sqlite:///", "")
        self._init_db()

    def _init_db(self):
        """Initialize the database schema."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS experiments (
                    id TEXT PRIMARY KEY,
                    status TEXT,
                    start_time TEXT,
                    end_time TEXT,
                    config TEXT
                )
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS runs (
                    id TEXT PRIMARY KEY,
                    experiment_id TEXT,
                    architecture_id TEXT,
                    metrics TEXT,
                    timestamp TEXT,
                    FOREIGN KEY (experiment_id) REFERENCES experiments(id)
                )
            """
            )
            conn.commit()

    async def list_all_runs(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **filters,
    ) -> List[Dict[str, Any]]:
        """List all runs in the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM runs"
            conditions = []
            params = []

            if start_date:
                conditions.append("timestamp >= ?")
                params.append(start_date)
            if end_date:
                conditions.append("timestamp <= ?")
                params.append(end_date)

            for key, value in filters.items():
                conditions.append(f"{key} = ?")
                params.append(value)

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            cursor.execute(query, params)
            rows = cursor.fetchall()
            runs = []
            for row in rows:
                run = {
                    "id": row[0],
                    "experiment_id": row[1],
                    "architecture_id": row[2],
                    "metrics": json.loads(row[3]),
                    "timestamp": row[4],
                }
                runs.append(run)
            return runs

    async def get_best_architectures(
        self, metric: str, limit: int = 10, **filters
    ) -> List[Dict[str, Any]]:
        """Get the best architectures based on a metric."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            query = """
                SELECT architecture_id, metrics
                FROM runs
            """
            conditions = []
            params = []

            for key, value in filters.items():
                conditions.append(f"{key} = ?")
                params.append(value)

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            query += f" ORDER BY json_extract(metrics, '$.{metric}') DESC LIMIT ?"
            params.append(limit)

            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [
                {"architecture_id": row[0], "metrics": json.loads(row[1])}
                for row in rows
            ]

    async def save_run_info(self, run_info: Dict[str, Any]) -> str:
        """Save run information to the database."""
        run_id = run_info.get("id", str(datetime.now().timestamp()))
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO runs (id, experiment_id, architecture_id, metrics, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """,
                (
                    run_id,
                    run_info.get("experiment_id"),
                    run_info["architecture_id"],
                    json.dumps(run_info["metrics"]),
                    datetime.now().isoformat(),
                ),
            )
            conn.commit()
        return run_id

    def get_experiment_details(self, experiment_id: str) -> Optional[Dict[str, Any]]:
        """Get details of a specific experiment."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM experiments WHERE id = ?", (experiment_id,))
            row = cursor.fetchone()
            if row is None:
                return None
            return {
                "id": row[0],
                "status": row[1],
                "start_time": row[2],
                "end_time": row[3],
                "config": json.loads(row[4]),
            }

    def list_experiments(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all experiments, optionally filtered by status."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if status:
                cursor.execute("SELECT * FROM experiments WHERE status = ?", (status,))
            else:
                cursor.execute("SELECT * FROM experiments")
            rows = cursor.fetchall()
            return [
                {
                    "id": row[0],
                    "status": row[1],
                    "start_time": row[2],
                    "end_time": row[3],
                    "config": json.loads(row[4]),
                }
                for row in rows
            ]

    def create_experiment(
        self, name: str, description: Optional[str], config: Dict[str, Any]
    ) -> str:
        """Create a new experiment."""
        experiment_id = str(datetime.now().timestamp())
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO experiments (id, status, start_time, config)
                VALUES (?, ?, ?, ?)
            """,
                (
                    experiment_id,
                    "created",
                    datetime.now().isoformat(),
                    json.dumps({"name": name, "description": description, **config}),
                ),
            )
            conn.commit()
        return experiment_id

    def update_experiment_status(self, experiment_id: str, status: str) -> None:
        """Update the status of an experiment."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if status == "completed":
                cursor.execute(
                    """
                    UPDATE experiments
                    SET status = ?, end_time = ?
                    WHERE id = ?
                """,
                    (status, datetime.now().isoformat(), experiment_id),
                )
            else:
                cursor.execute(
                    """
                    UPDATE experiments
                    SET status = ?
                    WHERE id = ?
                """,
                    (status, experiment_id),
                )
            conn.commit()

    def delete_experiment(self, experiment_id: str) -> bool:
        """Delete an experiment."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM experiments WHERE id = ?", (experiment_id,))
            if cursor.fetchone() is None:
                return False
            cursor.execute("DELETE FROM runs WHERE experiment_id = ?", (experiment_id,))
            cursor.execute("DELETE FROM experiments WHERE id = ?", (experiment_id,))
            conn.commit()
            return True

    def get_experiment(self, experiment_id: str) -> Optional[Dict[str, Any]]:
        """Get experiment details by ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM experiments WHERE id = ?", (experiment_id,))
            row = cursor.fetchone()
            if row is None:
                return None
            return {
                "id": row[0],
                "status": row[1],
                "start_time": row[2],
                "end_time": row[3],
                "config": json.loads(row[4]),
            }

    def get_metrics(
        self,
        experiment_id: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        metric_names: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Get metrics with optional filtering."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            query = "SELECT experiment_id, metrics, timestamp FROM runs"
            conditions = []
            params = []

            if experiment_id:
                conditions.append("experiment_id = ?")
                params.append(experiment_id)
            if start_time:
                conditions.append("timestamp >= ?")
                params.append(start_time.isoformat())
            if end_time:
                conditions.append("timestamp <= ?")
                params.append(end_time.isoformat())

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            cursor.execute(query, params)
            rows = cursor.fetchall()
            metrics = []
            for row in rows:
                metric_data = json.loads(row[1])
                if metric_names:
                    metric_data = {
                        k: v for k, v in metric_data.items() if k in metric_names
                    }
                metrics.append(
                    {
                        "experiment_id": row[0],
                        "metrics": metric_data,
                        "timestamp": row[2],
                    }
                )
            return metrics

    def get_architecture(self, architecture_id: str) -> Optional[Dict[str, Any]]:
        """Get architecture details by ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT architecture_id, metrics, timestamp
                FROM runs
                WHERE architecture_id = ?
                ORDER BY timestamp DESC
                LIMIT 1
            """,
                (architecture_id,),
            )
            row = cursor.fetchone()
            if row is None:
                return None
            return {"id": row[0], "metrics": json.loads(row[1]), "timestamp": row[2]}

    def list_architectures(
        self, skip: int = 0, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """List architectures with pagination."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT DISTINCT architecture_id, metrics, timestamp
                FROM runs
                ORDER BY timestamp DESC
                LIMIT ? OFFSET ?
            """,
                (limit, skip),
            )
            rows = cursor.fetchall()
            return [
                {"id": row[0], "metrics": json.loads(row[1]), "timestamp": row[2]}
                for row in rows
            ]

    def list_experiments(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """List experiments with pagination."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, status, start_time, end_time, config
                FROM experiments
                ORDER BY start_time DESC
                LIMIT ? OFFSET ?
            """,
                (limit, skip),
            )
            rows = cursor.fetchall()
            return [
                {
                    "id": row[0],
                    "status": row[1],
                    "start_time": row[2],
                    "end_time": row[3],
                    "config": json.loads(row[4]),
                }
                for row in rows
            ]
