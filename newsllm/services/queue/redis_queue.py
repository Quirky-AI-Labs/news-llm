"""
Author: Aayush Shah
Description: Implementation of a queue using Redis with logging and singleton pattern.
"""

from typing import Any, Generator, Optional

import redis
from loguru import logger

from newsllm.config import Config
from newsllm.services.queue.base import AbstractQueue
from newsllm.services.utils import SingletonMetaBase


class RedisQueue(AbstractQueue, metaclass=SingletonMetaBase):
    """
    A queue implementation using Redis with logging support.

    This class follows the singleton pattern, ensuring that only one instance
    of RedisQueue exists for each unique queue name.
    """

    def __init__(self, queue_name: str = "", url: str = Config.REDIS_QUEUE_URL):
        """
        Initialize the RedisQueue with a queue name and Redis URL.

        Args:
            queue_name (str): The name of the queue. Defaults to an empty string.
            url (str): The Redis server URL. Defaults to Config.REDIS_QUEUE_URL.
        """
        super().__init__(queue_name)
        self.client = redis.from_url(url)
        logger.info(f"RedisQueue {self.queue_name} initialized for client URL {url}")

    def enqueue(self, item: Any) -> None:
        """
        Add an item to the Redis queue and log the operation.

        Args:
            item (Any): The item to be added to the queue.
        """
        logger.info(f"Enqueue {str(item)[:10]} to {self.queue_name}")
        self.client.lpush(self.queue_name, item)

    def dequeue(self) -> Optional[Any]:
        """
        Remove and return an item from the Redis queue.

        Returns:
            Optional[Any]: The item removed from the queue, or None if the queue is empty.
        """
        item = self.client.rpop(self.queue_name)
        if item:
            logger.info(f"Dequeue {str(item)[:10]} from {self.queue_name}")
        return item

    def dequeue_generator(self) -> Generator[Any, None, None]:
        """
        Create a generator to dequeue items from the Redis queue one at a time.

        Yields:
            Any: The next item from the queue.
        """
        while True:
            item = self.client.lpop(self.queue_name)
            if item is None:
                break
            logger.info(f"Yield {str(item)[:10]} from {self.queue_name}")
            yield item

    def size(self) -> int:
        """
        Get the number of items in the Redis queue.

        Returns:
            int: The number of items in the queue.
        """
        size = self.client.llen(self.queue_name)
        logger.info(f"Size of {self.queue_name} is {size}")
        return size

    def clear(self) -> None:
        """
        Remove all items from the Redis queue and log the operation.
        """
        self.client.delete(self.queue_name)
        logger.info(f"Cleared all items from {self.queue_name}")

    def __del__(self):
        """
        Close the Redis client connection when the instance is deleted.
        """
        self.client.close()
        logger.info(f"Closed Redis client for {self.queue_name}")
