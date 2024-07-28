"""
Author: Aayush Shah
Description: Factory module for creating queue instances based on specified type and environment configuration.
"""

import importlib
import os
import pkgutil
import sys
from typing import Dict, Type

from newsllm.services.queue.base import AbstractQueue

# Automatically import all modules in the 'queue' package
package = sys.modules[__name__].__package__
package_path = os.path.join(os.path.dirname(__file__))
for _, module_name, _ in pkgutil.iter_modules([package_path]):
    importlib.import_module(f"{package}.{module_name}")

# Create a dictionary of available queue classes
QUEUE_CLASSES: Dict[str, Type[AbstractQueue]] = {cls.queue_type: cls for cls in AbstractQueue.__subclasses__()}


def get_queue(queue_name: str = "", queue_type: str = "list") -> AbstractQueue:
    """
    Factory function to get a queue instance based on the specified type and environment configuration.

    This function allows selecting between different queue implementations based on the queue_type argument.

    Args:
        queue_name (str): The name of the queue. Defaults to an empty string.
        queue_type (str): The type of the queue. Should match the `queue_type` attribute of a queue class.

    Returns:
        AbstractQueue: An instance of the specified queue type.

    Raises:
        ValueError: If the specified queue_type is not supported or required environment variables are missing.
    """
    if queue_type not in QUEUE_CLASSES:
        raise ValueError(f"Unsupported queue type: {queue_type}")

    QueueClass = QUEUE_CLASSES[queue_type]
    if queue_type == "redis":
        redis_url = os.getenv("REDIS_QUEUE_URL", None)
        if not redis_url:
            raise ValueError("REDIS_QUEUE_URL environment variable not set")
        return QueueClass(queue_name=queue_name, url=redis_url)

    return QueueClass(queue_name=queue_name)
