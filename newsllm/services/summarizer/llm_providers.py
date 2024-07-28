"""
Author: Aayush Shah
Description: Provider classes for different summarization APIs, inherited from the base provider class.
"""

import os

from newsllm.services.summarizer.base import BaseLLMProvider, ModelNotFoundError


class OpenRouterProvider(BaseLLMProvider):
    """
    Provider class for OpenRouter API.

    Attributes:
        DEFAULT_MODEL (str): Default model name for the OpenRouter API.
    """

    DEFAULT_MODEL = "google/gemini-flash-1.5"

    def __init__(self, api_key: str = None):
        """
        Initialize the OpenRouterProvider with API key.

        Args:
            api_key (str, optional): API key for the OpenRouter API. If not provided, it will be fetched from the environment variable 'OPENROUTER_API_KEY'.
        """
        api_key = api_key or os.getenv("OPENROUTER_API_KEY", "")
        if not api_key:
            raise ValueError("API key is required for OpenRouterProvider.")
        super().__init__(
            api_key,
            "https://openrouter.ai/api/v1",
        )


class OpenAIProvider(BaseLLMProvider):
    """
    Provider class for OpenAI API.

    Attributes:
        DEFAULT_MODEL (str): Default model name for the OpenAI API.
    """

    DEFAULT_MODEL = "gpt-4o"

    def __init__(self, api_key: str = None):
        """
        Initialize the OpenAIProvider with API key.

        Args:
            api_key (str, optional): API key for the OpenAI API. If not provided, it will be fetched from the environment variable 'OPENAI_API_KEY'.
        """
        api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        if not api_key:
            raise ValueError("API key is required for OpenAIProvider.")
        super().__init__(api_key, "https://api.openai.com/v1")


class ProviderFactory:
    """
    Factory class to get provider instances based on provider name.
    """

    PROVIDERS = {
        "openrouter": OpenRouterProvider,
        "openai": OpenAIProvider,
    }

    @classmethod
    def get_provider(cls, provider_name: str) -> BaseLLMProvider:
        """
        Get a provider instance based on the provider name.

        Args:
            provider_name (str): Name of the provider.

        Returns:
            Provider: An instance of the requested provider.

        Raises:
            ModelNotFoundError: If the provider is not found in the PROVIDERS dictionary.
        """
        provider = cls.PROVIDERS.get(provider_name)
        if not provider:
            raise ModelNotFoundError(f"Provider {provider_name} not found.")
        return provider
