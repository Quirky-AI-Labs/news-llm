"""
Author: Aayush Shah
Description: Implementation of a queue using a list (deque) with logging and singleton pattern.
"""

from collections import deque
from typing import Any, Generator, Optional

from loguru import logger

from newsllm.services.queue.base import AbstractQueue
from newsllm.services.utils import SingletonMetaBase


class ListQueue(AbstractQueue, metaclass=SingletonMetaBase):
    """
    A queue implementation using a deque (double-ended queue) with logging support.

    This class follows the singleton pattern, ensuring that only one instance
    of ListQueue exists for each unique queue name.
    """

    def __init__(self, queue_name: str = ""):
        """
        Initialize the ListQueue with an optional name.

        Args:
            queue_name (str): The name of the queue. Defaults to an empty string.
        """
        super().__init__(queue_name)
        self.queue = deque()
        logger.debug(f"ListQueue {self.queue_name} initialized")

    def enqueue(self, item: Any) -> None:
        """
        Add an item to the queue and log the operation.

        Args:
            item (Any): The item to be added to the queue.
        """
        logger.debug(f"Enqueue {str(item)[:30]} to ListQueue {self.queue_name}")
        self.queue.append(item)

    def dequeue(self) -> Optional[Any]:
        """
        Remove and return an item from the queue. Log the operation.

        Returns:
            Optional[Any]: The item removed from the queue, or None if the queue is empty.
        """
        if not self.queue:
            return None
        item = self.queue.popleft()
        logger.debug(f"Dequeue {str(item)[:30]} from ListQueue {self.queue_name}")
        return item

    def dequeue_generator(self) -> Generator[Any, None, None]:
        """
        Create a generator to dequeue items from the queue one at a time.

        Yields:
            Any: The next item from the queue.
        """
        while self.queue:
            yield self.dequeue()

    def size(self) -> int:
        """
        Get the number of items in the queue.

        Returns:
            int: The number of items in the queue.
        """
        return len(self.queue)

    def clear(self) -> None:
        """
        Remove all items from the queue and log the operation.
        """
        self.queue.clear()
        logger.debug(f"ListQueue {self.queue_name} cleared")
