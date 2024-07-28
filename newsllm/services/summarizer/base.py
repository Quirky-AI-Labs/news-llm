"""
Author: Aayush Shah
Description: Base classes and functionality for the summarizer module.
"""

from loguru import logger
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_random_exponential

from newsllm.utils import timeit

SYSTEM_PROMPT = """
You are a professional content writer with a lot of experience. You are writing summaries of different articles for a client. The purpose of the summary is to provide the client with an overall context of the article so that they can decide whether the article is worth reading or not.
You will now have to create a list of tags that the article is relevant to. Ensure you don't give duplicates or synonyms. Each tag should be 1-3 words. The tags can be Artificial Intelligence, Software Programming, Coding, Finance, Startups, Design, Health, Sustainability, etc.
The output should be a JSON object with keys as summary and tags. The summary should be the summary of the article and tags should be the list of tags.
Output:
```json
{
    "summary": "The summary of the article",
    "tags": ["tag1", "tag2", "tag3"]
}
```
"""


class ModelNotFoundError(Exception):
    """Custom exception for when a specified model is not found."""

    pass


class BaseLLMProvider:
    """Base class for all providers to interact with language models."""

    def __init__(self, api_key: str, base_url: str):
        """
        Initialize the Provider with API key and base URL.

        Args:
            api_key (str): The API key for authentication.
            base_url (str): The base URL for the API.
        """
        self._api_key = api_key
        self._base_url = base_url
        self._client = self._create_client(api_key, base_url)

    @staticmethod
    def _create_client(api_key: str, base_url: str) -> OpenAI:
        """
        Create an OpenAI client.

        Args:
            api_key (str): The API key for authentication.
            base_url (str): The base URL for the API.

        Returns:
            OpenAI: An instance of the OpenAI client.
        """
        return OpenAI(api_key=api_key, base_url=base_url)

    @property
    def api_key(self) -> str:
        """API key property."""
        return self._api_key

    @property
    def base_url(self) -> str:
        """Base URL property."""
        return self._base_url

    @property
    def client(self) -> OpenAI:
        """Client property."""
        return self._client

    def _check_model_exists(self, model_name: str) -> bool:
        """
        Check if a model exists in the provider's model list.

        Args:
            model_name (str): The name of the model to check.

        Returns:
            bool: True if the model exists, False otherwise.
        """
        model_list = self._client.models.list()
        model_list = [model.name.split(":")[-1].strip().lower() for model in model_list]
        return model_name.lower() in model_list

    @retry(
        wait=wait_random_exponential(min=2, max=6),
        stop=stop_after_attempt(2),
    )
    @timeit("Provider call")
    def call(self, model_name: str, user_prompt: str, **kwargs) -> str:
        """
        Call the model to generate a summary and tags for the given prompt.

        Args:
            model_name (str): The name of the model to use.
            user_prompt (str): The user prompt containing the article text.

        Returns:
            str: The generated summary and tags in JSON format.

        Raises:
            ModelNotFoundError: If the specified model is not found.
        """
        if not self._check_model_exists(model_name):
            logger.error(f"Model {model_name} not found.")
            raise ModelNotFoundError(f"Model {model_name} not found.")

        logger.debug(f"Using {self.__class__.__name__} with model {model_name}.")
        try:
            res = self._client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                **kwargs,
            )
            return res.choices[0].message.content
        except Exception as e:
            logger.error(f"Error: {e}")
            return ""
