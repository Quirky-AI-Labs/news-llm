"""
Author: Aayush Shah
Description: This module defines the abstract base class for message channels used in the channels package.
"""

from abc import ABC, abstractmethod

from newsllm.structures import News


class BaseChannel(ABC):
    """
    Abstract base class for message channels.

    This class defines the basic interface that all message channels must implement, including methods for sending and
    receiving messages.

    Methods:
        send(news: News, **kwargs): Send a news object to the channel.
        receive(**kwargs) -> str: Receive a message from the channel.
    """

    @abstractmethod
    def send(self, news: News, **kwargs):
        """
        Send a news object to the channel.

        Args:
            news (News): The news object to send.
            **kwargs: Additional keyword arguments for channel-specific options.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        raise NotImplementedError

    @abstractmethod
    def receive(self, **kwargs) -> str:
        """
        Receive a message from the channel.

        Args:
            **kwargs: Additional keyword arguments for channel-specific options.

        Returns:
            str: The received message.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        raise NotImplementedError
