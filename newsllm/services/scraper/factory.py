import importlib
import pkgutil
from typing import List, Type

from loguru import logger

import newsllm
from newsllm.services.queue.factory import get_queue
from newsllm.services.scraper.base import BaseScraper
from newsllm.structures import News


class ScraperFactory:
    """
    Factory class to handle scraping operations.

    Attributes:
        scrapers (List[BaseScraper]): List of scraper instances.
        queue (Queue): Queue for processing scraped news.
    """

    def __init__(self, **kwargs):
        self.scrapers = self.get_scrapers(**kwargs)
        self.queue = get_queue("llm-queue")

    @staticmethod
    def get_scraper_list() -> List[Type[BaseScraper]]:
        """
        Dynamically imports and returns a list of scraper classes that inherit from BaseScraper.

        Returns:
            List[Type[BaseScraper]]: List of scraper classes.
        """
        scrapers = []
        package = newsllm.services.scraper
        prefix = package.__name__ + "."

        for importer, modname, ispkg in pkgutil.iter_modules(package.__path__, prefix):
            module = importlib.import_module(modname)
            for attribute_name in dir(module):
                attribute = getattr(module, attribute_name)
                if isinstance(attribute, type) and issubclass(attribute, BaseScraper) and attribute is not BaseScraper:
                    if getattr(attribute, "include_in_factory", True):
                        scrapers.append(attribute)

        return scrapers

    def get_scrapers(self, **kwargs) -> List[BaseScraper]:
        """
        Instantiates scraper classes.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            List[BaseScraper]: List of scraper instances.
        """
        scrapers = self.get_scraper_list()
        return [scraper(**kwargs) for scraper in scrapers]

    async def scrape(self, limit: int, **kwargs):
        """
        Scrapes news using the available scrapers.

        Args:
            limit (int): Maximum number of news items to scrape per scraper. if None, returns all news.
            **kwargs: Additional keyword arguments.

        Returns:
            List[News]: List of scraped news items.
        """
        news_list: List[News] = []
        logger.debug(f"Scraping news from {len(self.scrapers)} scrapers with post limit {limit}")
        for scraper in self.scrapers:
            scraped_news = await scraper.scrape(**kwargs)
            logger.debug(f"Scraped {len(scraped_news)} news from {scraper.scraper_name}!!!")
            if limit is not None:
                scraped_news = scraped_news[:limit]
            news_list.extend(scraped_news)
            [self.queue.enqueue(news.model_dump_json()) for news in scraped_news]
        logger.debug(f"Total scraped news: {len(news_list)}!!!")
        return news_list
