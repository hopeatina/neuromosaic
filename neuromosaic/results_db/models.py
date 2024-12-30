"""SQLAlchemy models for the results database."""

from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Architecture(Base):
    """
    Stores unique architecture vectors, ensuring we do not retrain the same architecture
    if we already have data for it. The vector is hashed to produce 'vector_hash'.
    """

    __tablename__ = "architectures"

    vector_hash = Column(String, primary_key=True)
    arch_spec = Column(
        Text, nullable=False
    )  # Stored as JSON string for SQLite compatibility
    code_commit = Column(String, nullable=True)
    creation_time = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    # Relationship to runs
    runs = relationship("Run", back_populates="architecture")


class Experiment(Base):
    """
    Represents a top-level experiment, which can contain multiple runs.
    """

    __tablename__ = "experiments"

    id = Column(String, primary_key=True)
    status = Column(String, nullable=True)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    config = Column(
        Text, nullable=True
    )  # Stored as JSON string for SQLite compatibility

    # Relationship to runs
    runs = relationship("Run", back_populates="experiment")


class Run(Base):
    """
    Each 'run' is a training/evaluation instance involving a particular architecture.
    """

    __tablename__ = "runs"

    id = Column(String, primary_key=True)
    experiment_id = Column(String, ForeignKey("experiments.id"), nullable=True)
    architecture_id = Column(
        String, ForeignKey("architectures.vector_hash"), nullable=True
    )
    metrics = Column(
        Text, nullable=True
    )  # Stored as JSON string for SQLite compatibility
    timestamp = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    # Relationships
    experiment = relationship("Experiment", back_populates="runs")
    architecture = relationship("Architecture", back_populates="runs")
