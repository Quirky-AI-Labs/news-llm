"""
Author: Aayush Shah
Description: Configuration file for setting up environment variables and default values for the application. 
"""

import os


class Config:
    """
    Configuration class to encapsulate environment variables and provide default values.
    """

    REDIS_QUEUE_URL = os.getenv("REDIS_QUEUE_URL", None)
    DATABASE = os.getenv("DATABASE", "news-llm")
    MONGO_HOST = os.getenv("MONGO_HOST", "0.0.0.0")
    MONGO_PORT = os.getenv("MONGO_PORT", "27017")
    MONGO_USERNAME = os.getenv("MONGO_USERNAME", "")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
