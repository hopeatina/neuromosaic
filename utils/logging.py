"""
Logging utilities for the project.
"""

import logging
from typing import Optional
from pathlib import Path


def setup_logger(
    name: str, log_file: Optional[str] = None, level: int = logging.INFO
) -> logging.Logger:
    """
    Set up a logger with console and optional file handlers.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create formatters
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Create file handler if log_file is specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
