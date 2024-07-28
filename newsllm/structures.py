"""
Author: Aayush Shah
Description: This module defines the News model used for representing news articles in the scraping and summarization pipeline.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field, HttpUrl, field_validator


class News(BaseModel):
    """Model representing a news article."""

    title: str
    raw_content: str
    url: HttpUrl
    id: str = Field(default_factory=lambda: str(uuid4()))
    source: str = Field(default="UNKNOWN")
    scraped_at: str = Field(default_factory=lambda: str(datetime.now().isoformat()))
    published_date: Optional[str] = None
    author: Optional[str] = None
    categories: Optional[List[str]] = Field(default_factory=list)
    tags: Optional[List[str]] = Field(default_factory=list)
    description: Optional[str] = ""
    text_content: str = ""
    summary: str = None
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

    def __hash__(self) -> int:
        """Generate a hash value for the news article based on its id and source."""
        return hash(f"{self.id}-{self.source}")

    def __eq__(self, other: "News") -> bool:
        """Check equality between two news articles based on their id and source.

        Args:
            other (News): The other news article to compare.

        Returns:
            bool: True if the articles are equal, False otherwise.
        """
        return self.id == other.id and self.source == other.source

    @field_validator("id", mode="before")
    @classmethod
    def convert_to_str(cls, value):
        """Convert the id to a string before validation.

        Args:
            value: The value to convert.

        Returns:
            str: The converted string value.
        """
        return str(value)
