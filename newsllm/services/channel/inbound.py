"""
Author: Aayush Shah
Description: This module defines inbound channels for receiving messages from various sources.
"""

from newsllm.services.channel.base import BaseChannel


class BaseInboundChannel(BaseChannel):
    """
    Base class for inbound channels.

    This class inherits from BaseChannel and overrides the receive method to raise a RuntimeError,
    indicating that dispatch channels cannot receive messages.
    """

    def receive(self, **kwargs) -> str:
        """
        Raises a RuntimeError as inbound channels do not support dispatch functionality.

        Args:
            **kwargs: Additional keyword arguments (not used).

        Raises:
            RuntimeError: Always raised as dispatch channels cannot receive messages.
        """
        raise RuntimeError("Dispatch channels cannot receive messages.")
