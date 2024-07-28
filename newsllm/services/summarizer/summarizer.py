"""
Author: Aayush Shah
Description: Summarizer module for generating summaries of text content using various providers.
"""

import json
import os
import re

from loguru import logger

from newsllm.services.summarizer.base import BaseLLMProvider
from newsllm.services.summarizer.llm_providers import LLMProviderFactory

DEFAULT_PROVIDER = os.getenv("SUMMARY_PROVIDER", "openrouter")
SUMMARIZER_MODEL = os.getenv("SUMMARIZER_MODEL", "google/gemini-flash-1.5")

DEFAULT_SUMMARY_PROVIDER: BaseLLMProvider = LLMProviderFactory.get_provider(DEFAULT_PROVIDER)


class Summarizer:
    """
    Summarizer class to generate summaries using specified provider and model.
    """

    def __init__(self, provider: str = None, model: str = None):
        """
        Initialize the Summarizer with the specified provider and model.

        Args:
            provider (str, optional): Name of the provider to use. Defaults to environment variable 'SUMMARY_PROVIDER'.
            model (str, optional): Name of the model to use. Defaults to environment variable 'SUMMARIZER_MODEL'.
        """
        self.provider: BaseLLMProvider = DEFAULT_SUMMARY_PROVIDER
        self.model = SUMMARIZER_MODEL

        if provider:
            self.provider = ProviderFactory.get_provider(provider)

        if model:
            self.model = model

    def summarize(self, text_content: str) -> dict:
        """
        Generate a summary for the given text content.

        Args:
            text_content (str): The text content to summarize.

        Returns:
            dict: A dictionary containing the summary and tags.
        """
        try:
            summary = self.provider.call(model_name=self.model, user_prompt=text_content)
            summary_data = self.normalize_text(summary)
            summary_data = self.extract_json(summary_data)
            llm_res_dict = {}

            if summary_data:
                llm_res_dict = self.load_json(summary_data)

            return llm_res_dict
        except Exception as e:
            logger.error(f"Error in summarizing content: {e}")
            return {}

    @staticmethod
    def normalize_text(text: str) -> str:
        """
        Normalize the given text by removing extra whitespace.

        Args:
            text (str): The text to normalize.

        Returns:
            str: The normalized text.
        """
        text = re.sub(r"(\s)\1+", r"\1", text)
        return text.strip()

    @staticmethod
    def extract_json(text: str):
        """
        Extract JSON content from the given text.

        Args:
            text (str): The text containing JSON content.

        Returns:
            Union[str, None]: The extracted JSON string or None if not found.
        """
        pattern = re.compile(r"```json(.*?)```|```(.*?)```", re.DOTALL)
        match = pattern.search(text)
        if match:
            return match.group(1).strip() if match.group(1) else match.group(2).strip()
        return None

    @staticmethod
    def load_json(text: str) -> dict:
        """
        Load a JSON string into a dictionary.

        Args:
            text (str): The JSON string to load.

        Returns:
            dict: The loaded dictionary.
        """
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            logger.error(f"Error loading JSON: {e}")
            return {}
