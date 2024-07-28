"""
Author: Aayush Shah
Description: Abstract base class for queue implementations.
"""

from abc import ABC, abstractmethod
from typing import Any, Generator


class AbstractQueue(ABC):
    """
    An abstract base class representing a generic queue.

    This class provides an interface for queue operations that must be implemented by subclasses.
    """

    def __init__(self, queue_name: str = ""):
        """
        Initialize the queue with an optional name.

        Args:
            queue_name (str): The name of the queue. Defaults to an empty string.
        """
        self.queue_name = queue_name

    @abstractmethod
    def enqueue(self, item: Any) -> None:
        """
        Add an item to the queue.

        Args:
            item (Any): The item to be added to the queue.

        Raises:
            NotImplementedError: This method must be overridden by subclasses.
        """
        raise NotImplementedError

    @abstractmethod
    def dequeue(self) -> Any:
        """
        Remove and return an item from the queue.

        Returns:
            Any: The item removed from the queue.

        Raises:
            NotImplementedError: This method must be overridden by subclasses.
        """
        raise NotImplementedError

    @abstractmethod
    def dequeue_generator(self) -> Generator[Any, None, None]:
        """
        Create a generator to dequeue items from the queue one at a time.

        Yields:
            Any: The next item from the queue.

        Raises:
            NotImplementedError: This method must be overridden by subclasses.
        """
        raise NotImplementedError

    @abstractmethod
    def size(self) -> int:
        """
        Get the number of items in the queue.

        Returns:
            int: The number of items in the queue.

        Raises:
            NotImplementedError: This method must be overridden by subclasses.
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """
        Remove all items from the queue.

        Raises:
            NotImplementedError: This method must be overridden by subclasses.
        """
        pass
