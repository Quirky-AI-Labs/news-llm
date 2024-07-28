"""
Author: Aayush Shah
Description: Initialization file for the channels package. Sets up imports for channel classes and factory functions.
"""

from newsllm.services.channel.base import BaseChannel
from newsllm.services.channel.dispatch import BaseDispatchChannel, SlackDispatchChannel
from newsllm.services.channel.inbound import BaseInboundChannel

__all__ = [
    "BaseChannel",
    "BaseDispatchChannel",
    "SlackDispatchChannel",
    "BaseInboundChannel",
]
