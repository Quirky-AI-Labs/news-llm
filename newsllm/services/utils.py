"""
Author: Aayush Shah
Description: Utility code for creating singleton objects using metaclasses.
"""

from abc import ABCMeta
from typing import Any, Dict, Tuple


class SingletonMeta(type):
    """
    A Singleton metaclass that creates a single instance of a class by a specified key.

    This ensures that only one instance of the class is created for each unique key.
    """

    _instances: Dict[Tuple[type, Any], Any] = {}

    def __call__(cls, *args, **kwargs):
        """
        Create or return the existing instance of the class for the given key.

        Args:
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.

        Keyword Args:
            singleton_key: A key to identify the singleton instance (default: "").

        Returns:
            object: The single instance of the class for the given key.
        """
        key = args[0] if args else kwargs.get("queue_name", "")
        if (cls, key) not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[(cls, key)] = instance
        return cls._instances[(cls, key)]


class SingletonMetaBase(ABCMeta, SingletonMeta):
    """
    A base class that combines ABCMeta and SingletonMeta for creating singleton objects with abstract base classes.

    This can be used to ensure that only one instance of an abstract class (and its subclasses) is created for each unique key.
    """

    pass
