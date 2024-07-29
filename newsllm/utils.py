"""
Author: Aayush Shah
Description: Utility functions for logging and performance measurement.
"""

import time
import traceback
from functools import wraps
from typing import Any, Callable, Union

from loguru import logger

MessageType = Union[str, Callable[[Any], str]]


def log_traceback():
    """Log the current traceback using loguru logger."""
    logger.error(f"Traceback: {traceback.format_exc()}")


def str_to_bool(val: str) -> bool:
    """Convert a string representation of truth to boolean.

    Args:
        val (str): The string to convert.

    Returns:
        bool: True if val is in ('yes', 'true', 't', '1'), False otherwise.
    """
    return val.lower() in ("yes", "true", "t", "1")


def timeit(message: MessageType = "Execution Time") -> Callable:
    """Decorator to measure the execution time of a function and log it.

    Args:
        message (MessageType): A static message or a callable returning a message to log.

    Returns:
        Callable: The decorated function with execution time logging.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time
            if callable(message):
                msg = message(args[0])
            else:
                msg = message
            logger.debug(f"{msg}: {func.__name__} took {elapsed_time:.4f} seconds to execute")
            return result

        return wrapper

    return decorator
