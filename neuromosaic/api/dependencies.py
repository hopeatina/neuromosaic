"""
FastAPI dependencies for dependency injection.

Provides FastAPI dependency injection functions, including 
on_startup and on_shutdown events, database sessions, orchestrators, etc.
"""

from typing import Generator, Optional
import os

from fastapi import Depends

from neuromosaic.results_db.interface import IResultsDB
from neuromosaic.results_db.db import get_db_instance
from neuromosaic.orchestrator.interface import IOrchestrator
from neuromosaic.orchestrator.orchestrator import get_orchestrator_instance
from neuromosaic.arch_space.vector_representation import IArchitectureEncoder
from neuromosaic.arch_space.encoder import get_encoder_instance
from neuromosaic.utils.config import Config

# Global instances
_db_instance: Optional[IResultsDB] = None
_orchestrator_instance: Optional[IOrchestrator] = None
_encoder_instance: Optional[IArchitectureEncoder] = None


async def on_startup():
    """
    FastAPI startup event handler. Initializes the global
    database instance and orchestrator if needed.
    """
    global _db_instance, _orchestrator_instance, _encoder_instance

    # Load configuration from environment
    if "NEUROMOSAIC_CONFIG" not in os.environ:
        raise RuntimeError("NEUROMOSAIC_CONFIG environment variable not set")

    config = Config.from_env()
    config.load_config(os.environ["NEUROMOSAIC_CONFIG"])

    _db_instance = get_db_instance(config)
    _orchestrator_instance = get_orchestrator_instance()
    _encoder_instance = get_encoder_instance()


async def on_shutdown():
    """
    FastAPI shutdown event handler. Cleans up DB connections,
    orchestrator threads, etc.
    """
    global _db_instance, _orchestrator_instance, _encoder_instance

    if _db_instance:
        # Add cleanup if needed
        _db_instance = None

    if _orchestrator_instance:
        # Add cleanup if needed
        _orchestrator_instance = None

    if _encoder_instance:
        # Add cleanup if needed
        _encoder_instance = None


def get_db() -> Generator[IResultsDB, None, None]:
    """
    Dependency to get a database session.

    Yields:
        IResultsDB: Database interface instance
    """
    if not _db_instance:
        raise RuntimeError("Database not initialized")
    try:
        yield _db_instance
    finally:
        # Add any cleanup if needed
        pass


def get_orchestrator() -> Generator[IOrchestrator, None, None]:
    """
    Dependency to get an orchestrator instance.

    Yields:
        IOrchestrator: Orchestrator interface instance
    """
    if not _orchestrator_instance:
        raise RuntimeError("Orchestrator not initialized")
    try:
        yield _orchestrator_instance
    finally:
        # Add any cleanup if needed
        pass


def get_arch_space() -> Generator[IArchitectureEncoder, None, None]:
    """
    Dependency to get an architecture encoder instance.

    Yields:
        IArchitectureEncoder: Architecture encoder interface instance
    """
    if not _encoder_instance:
        raise RuntimeError("Architecture encoder not initialized")
    try:
        yield _encoder_instance
    finally:
        # Add any cleanup if needed
        pass


# Common dependency chains
def get_db_orchestrator(
    db: IResultsDB = Depends(get_db),
    orchestrator: IOrchestrator = Depends(get_orchestrator),
) -> tuple[IResultsDB, IOrchestrator]:
    """
    Combined dependency for both database and orchestrator.

    Args:
        db: Database instance from dependency
        orchestrator: Orchestrator instance from dependency

    Returns:
        tuple[IResultsDB, IOrchestrator]: Tuple of both instances
    """
    return db, orchestrator
