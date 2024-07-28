"""
Author: Aayush Shah
Description: This module provides the TechCrunch scraper which scrapes news from TechCrunch.
"""

from datetime import datetime

from loguru import logger

from newsllm.services.scraper.base import BaseScraper, ScraperMixins
from newsllm.structures import News
from newsllm.utils import log_traceback, timeit


class TechCrunch(BaseScraper, ScraperMixins):
    """
    Scraper for TechCrunch.

    Attributes:
        scraper_name (str): Name of the scraper.
        base_url (str): Base URL for the scraper.
    """

    scraper_name = "TechCrunch"
    base_url = "https://techcrunch.com"

    @timeit("TechCrunch single post scraping")
    async def _get_single_post(self, post, **kwargs) -> News:
        """
        Fetches and processes a single post from TechCrunch.

        Args:
            post (dict): The post data.
            **kwargs: Additional keyword arguments.

        Returns:
            News: The processed news item.
        """
        id = post.get("id", "1234")
        date_published = post.get("date", str(datetime.now()))
        status = post.get("status", "published")
        post_link = post.get("link", "")
        author = post.get("yoast_head_json", {}).get("author", "UNKNOWN AUTHOR")
        post_title = post.get("title", {}).get("rendered", post.get("slug", ""))
        post_description = post.get("yoast_head_json", {}).get("og_description", "")
        raw_content = post.get("content", {}).get("rendered", "")
        categories = post.get("categories", [])
        tags = post.get("tags", [])

        text_content = await self.get_text_content(raw_content)

        post_json = dict(
            id=id,
            published_date=date_published,
            status=status,
            url=post_link,
            title=post_title,
            author=author,
            description=post_description,
            raw_content=raw_content,
            text_content=text_content,
            categories=categories,
            tags=tags,
        )
        news = News(**post_json)
        return news

    async def _get_standard_data_list(self, post_collection, **kwargs):
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
                logger.error(f"Error on processing post in {self.__class__.__name__}")
                logger.error(f"Error: {e}")
                log_traceback()
        return posts

    def _get_metadata(self):
        """
        Returns metadata about the scraping session.

        Returns:
            dict: A dictionary containing metadata about the scraping session.
        """
        return {
            "site": self.__class__.__name__,
            "scraped_at": str(datetime.now()),
        }

    async def _scrape(self, **kwargs):
        """
        Scrapes the latest posts from TechCrunch.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            List[News]: A list of scraped news items.
        """
        url = f"{self.base_url}/wp-json/wp/v2/posts?categories=577047203&limit=50"
        post_collection = self._handle_site_request(url)
        if not post_collection:
            return []
        posts = await self._get_standard_data_list(post_collection, **kwargs)
        return posts
