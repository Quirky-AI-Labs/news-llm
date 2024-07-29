"""
Author: Aayush Shah
Description: This module defines outbound channels for sending news to respective platforms, such as Slack.
"""

import json

import requests
from loguru import logger

from newsllm.services.channel.base import BaseChannel
from newsllm.structures import News


class BaseDispatchChannel(BaseChannel):
    """
    Base class for dispatch channels.

    This class inherits from BaseChannel and overrides the receive method to raise a RuntimeError,
    indicating that dispatch channels cannot receive messages.
    """

    def receive(self, **kwargs) -> str:
        """
        Raises a RuntimeError as dispatch channels do not support receiving messages.

        Args:
            **kwargs: Additional keyword arguments (not used).

        Raises:
            RuntimeError: Always raised as dispatch channels cannot receive messages.
        """
        raise RuntimeError("Dispatch channels cannot receive messages.")


class SlackDispatchChannel(BaseDispatchChannel):
    """
    A dispatch channel for sending news to Slack.

    This class provides functionality to send formatted news messages to a specified Slack webhook URL.
    """

    def __init__(self, webhook_url: str):
        """
        Initialize the SlackDispatchChannel with the given webhook URL.

        Args:
            webhook_url (str): The Slack webhook URL to send messages to.
        """
        self.webhook_url = webhook_url

    def format_message(self, news: News):
        """
        Format the news object into a Slack message payload.

        Args:
            news (News): The news object to format.

        Returns:
            list: A list of blocks representing the formatted Slack message.
        """
        summary_blockquote = "\n".join([f">{line}" for line in news.summary.split("\n")])
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": news.title,
                },
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Source:* {news.source}\n*Date Published:* {news.published_date}\n",
                    }
                ],
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Tags:* _{', '.join(list(map(str,news.tags)))}_\n",
                },
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*Summary*\n{summary_blockquote}"},
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*URL:* <{news.url}>\n"},
            },
        ]
        return blocks

    def send_message(self, message: str):
        """
        Send a message to Slack.

        Args:
            message (str): The formatted message to send.

        Returns:
            requests.Response: The response from the Slack API.

        Raises:
            ValueError: If the Slack webhook URL is not provided.
        """
        logger.debug("Sending message to Slack")
        payload = {"text": "News Update", "blocks": message}
        if not self.webhook_url:
            raise ValueError("Slack webhook URL is required to send message to Slack.")
        response = requests.post(
            self.webhook_url,
            data=json.dumps(payload),
        )
        logger.info("Slack message sent with status code {response.status_code}")
        return response

    def send(self, news: News, **kwargs):
        """
        Send a formatted news object to Slack.

        Args:
            news (News): The news object to send.
            **kwargs: Additional keyword arguments for message formatting.

        Returns:
            requests.Response: The response from the Slack API.
        """
        message = self.format_message(news)
        return self.send_message(message)
