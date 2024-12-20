"""
Custom exceptions for the Neuramosaic project.

This module defines all custom exceptions used throughout the project.
Exceptions are organized by component and include error codes for
easier tracking and documentation.

Example:
    >>> try:
    ...     architecture = generate_architecture()
    ... except InvalidArchitectureError as e:
    ...     logger.error(f"Architecture error {e.code}: {e}")
"""

from typing import Optional, Any, Dict
from enum import Enum


class ErrorCode(Enum):
    """Enumeration of error codes by component."""

    # Architecture Space (1000-1999)
    INVALID_ARCHITECTURE = 1000
    DIMENSION_MISMATCH = 1001
    INVALID_BOUNDS = 1002
    ENCODING_ERROR = 1003

    # LLM Code Generation (2000-2999)
    GENERATION_FAILED = 2000
    VALIDATION_FAILED = 2001
    INVALID_PROMPT = 2002
    MODEL_UNAVAILABLE = 2003

    # Container Management (3000-3999)
    CONTAINER_CREATE_FAILED = 3000
    CONTAINER_RUN_FAILED = 3001
    RESOURCE_EXCEEDED = 3002
    TIMEOUT = 3003

    # Training & Evaluation (4000-4999)
    TRAINING_FAILED = 4000
    EVALUATION_FAILED = 4001
    INVALID_METRICS = 4002
    DATA_ERROR = 4003

    # Storage & Data Management (5000-5999)
    STORAGE_FULL = 5000
    FILE_NOT_FOUND = 5001
    PERMISSION_DENIED = 5002
    INVALID_CHECKPOINT = 5003

    # Search Strategy (6000-6999)
    SEARCH_EXHAUSTED = 6000
    INVALID_STRATEGY = 6001
    OPTIMIZATION_FAILED = 6002

    # General/Other (9000-9999)
    CONFIGURATION_ERROR = 9000
    DEPENDENCY_ERROR = 9001
    INTERNAL_ERROR = 9999


class NeuramosaicException(Exception):
    """Base exception class for all Neuramosaic errors."""

    def __init__(
        self, message: str, code: ErrorCode, details: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize exception.

        Args:
            message: Error description
            code: Error code enum
            details: Optional additional error details
        """
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(f"[{code.name}] {message}")


# Architecture Space Exceptions


class ArchitectureError(NeuramosaicException):
    """Base class for architecture-related errors."""

    pass


class InvalidArchitectureError(ArchitectureError):
    """Raised when an architecture specification is invalid."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, ErrorCode.INVALID_ARCHITECTURE, details)


class DimensionMismatchError(ArchitectureError):
    """Raised when vector dimensions don't match."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, ErrorCode.DIMENSION_MISMATCH, details)


# LLM Code Generation Exceptions


class CodeGenerationError(NeuramosaicException):
    """Base class for code generation errors."""

    pass


class GenerationFailedError(CodeGenerationError):
    """Raised when code generation fails."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, ErrorCode.GENERATION_FAILED, details)


class ValidationFailedError(CodeGenerationError):
    """Raised when generated code fails validation."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, ErrorCode.VALIDATION_FAILED, details)


# Container Management Exceptions


class ContainerError(NeuramosaicException):
    """Base class for container-related errors."""

    pass


class ContainerCreateError(ContainerError):
    """Raised when container creation fails."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, ErrorCode.CONTAINER_CREATE_FAILED, details)


class ResourceExceededError(ContainerError):
    """Raised when container exceeds resource limits."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, ErrorCode.RESOURCE_EXCEEDED, details)


# Training & Evaluation Exceptions


class TrainingError(NeuramosaicException):
    """Base class for training-related errors."""

    pass


class TrainingFailedError(TrainingError):
    """Raised when model training fails."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, ErrorCode.TRAINING_FAILED, details)


class DataError(TrainingError):
    """Raised when there are issues with training data."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, ErrorCode.DATA_ERROR, details)


# Storage & Data Management Exceptions


class StorageError(NeuramosaicException):
    """Base class for storage-related errors."""

    pass


class StorageFullError(StorageError):
    """Raised when storage quota is exceeded."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, ErrorCode.STORAGE_FULL, details)


class CheckpointError(StorageError):
    """Raised when there are issues with checkpoints."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, ErrorCode.INVALID_CHECKPOINT, details)


# Search Strategy Exceptions


class SearchError(NeuramosaicException):
    """Base class for search-related errors."""

    pass


class SearchExhaustedError(SearchError):
    """Raised when search space is exhausted."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, ErrorCode.SEARCH_EXHAUSTED, details)


class OptimizationError(SearchError):
    """Raised when optimization fails."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, ErrorCode.OPTIMIZATION_FAILED, details)


# Configuration Exceptions


class ConfigurationError(NeuramosaicException):
    """Raised when there are configuration issues."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, ErrorCode.CONFIGURATION_ERROR, details)


# Utility Functions


def format_error_details(details: Dict[str, Any]) -> str:
    """Format error details for logging."""
    lines = []
    for key, value in details.items():
        lines.append(f"  {key}: {value}")
    return "\n".join(lines)


def handle_exception(
    exc: Exception, logger: Any, raise_error: bool = True
) -> Optional[Dict[str, Any]]:
    """
    Handle an exception with proper logging.

    Args:
        exc: The caught exception
        logger: Logger instance
        raise_error: Whether to re-raise the exception

    Returns:
        Optional error details dictionary
    """
    if isinstance(exc, NeuramosaicException):
        error_info = {
            "code": exc.code.name,
            "message": exc.message,
            "details": exc.details,
        }
        logger.error(
            f"Error {exc.code.name}: {exc.message}\n"
            f"Details:\n{format_error_details(exc.details)}"
        )
    else:
        error_info = {
            "code": ErrorCode.INTERNAL_ERROR.name,
            "message": str(exc),
            "details": {"type": type(exc).__name__},
        }
        logger.error(f"Internal error: {exc}")

    if raise_error:
        raise exc

    return error_info
