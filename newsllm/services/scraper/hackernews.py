"""
Author: Aayush Shah
Description: This module provides the HackerNews scraper which scrapes news from Hacker News.
"""

import os
from datetime import datetime
from typing import List

from loguru import logger

from newsllm.services.scraper.base import BaseScraper, ScraperMixins
from newsllm.structures import News
from newsllm.utils import log_traceback, timeit


class HackerNewsScraper(BaseScraper, ScraperMixins):
    """
    Scraper for Hacker News.

    Attributes:
        scraper_name (str): Name of the scraper.
        base_url (str): Base URL for the scraper.
    """

    scraper_name = "HackerNews"
    base_url = "https://news.ycombinator.com"
    include_in_factory = True

    def get_item_url(self, item_id: str) -> str:
        """
        Constructs the URL for a specific item.

        Args:
            item_id (str): The item ID.

        Returns:
            str: The URL for the item.
        """
        return f"https://news.ycombinator.com/item?id={item_id}"

    @timeit("HackerNews single post scraping")
    async def _get_single_post(self, post, **kwargs) -> News:
        """
        Fetches and processes a single post from Hacker News.

        Args:
            post (dict): The post data.
            **kwargs: Additional keyword arguments.

        Returns:
            News: The processed news item.
        """
        logger.info(f"Getting single post from {self.__class__.__name__} | post: {post}")
        id = post["id"]
        date_published = str(datetime.fromtimestamp(post["time"]))
        status = "published"
        post_link = post.get("url", self.get_item_url(id))
        author = post.get("by", "unknown author")
        post_title = post.get("title", "")
        raw_content = await self.fetch_html_content(post_link)
        raw_content = raw_content if raw_content else ""
        text_content = await self.get_text_content(raw_content, "body") if raw_content else ""
        categories = post.get("categories", [])
        tags = post.get("tags", [])

        post_json = dict(
            id=id,
            published_date=date_published,
            status=status,
            url=post_link,
            title=post_title,
            author=author,
            raw_content=raw_content,
            text_content=text_content,
            categories=categories,
            tags=tags,
        )
        news = News(**post_json)
        return news

    async def _get_standard_data_list(self, post_collection, **kwargs) -> List[News]:
        """
        Processes a collection of posts into a standardized list of news items.

        Args:
            post_collection (list): A list of post data.
            **kwargs: Additional keyword arguments.

        Returns:
            List[News]: A list of processed news items.
        """
        posts = []
        for post in post_collection:
            try:
                post_json = await self._get_single_post(post)
                post_json.source = self.scraper_name
                post_json.scraped_at = str(datetime.now())
                posts.append(post_json)
            except Exception as e:
                logger.error(f"Error on getting single post from {self.__class__.__name__}")
                logger.error(f"Error: {e}")
                log_traceback()
        return posts

    async def _scrape(self, **kwargs) -> List[News]:
        """
        Scrapes the top stories from Hacker News.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            List[News]: A list of scraped news items.
        """
        top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
        post_ids = await self._handle_site_request(top_stories_url)
        post_collection = []
        news_limit = int(kwargs.get("limit", os.getenv("NEWS_LIMIT", 5)))
        for post_id in post_ids[:news_limit]:
            news_url = f"https://hacker-news.firebaseio.com/v0/item/{post_id}.json?print=pretty"
            post_data = await self._handle_site_request(news_url)
            if post_data:
                post_collection.append(post_data)
        posts = await self._get_standard_data_list(post_collection, **kwargs)
        return posts
