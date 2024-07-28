"""
Author: Aayush Shah
Description: This module provides the base classes for web scraping, including BaseScraper and ScraperMixins.
"""

from abc import ABC, abstractmethod
from typing import List

import requests
from bs4 import BeautifulSoup
from loguru import logger
from playwright.async_api import Browser, Page, async_playwright

from newsllm.structures import News
from newsllm.utils import log_traceback


class BaseScraper(ABC):
    """
    Abstract base class for web scrapers.

    Attributes:
        scraper_name (str): Name of the scraper.
        base_url (str): Base URL for the scraper.
    """

    scraper_name = "BaseScraper"
    base_url = None

    async def scrape(self, **kwargs) -> List[News]:
        """
        Scrapes data and returns a list of news articles.

        Args:
            **kwargs: Additional keyword arguments for scraping options.

        Returns:
            List[News]: A list of news articles.
        """
        verbose = kwargs.get("verbose", True)
        if verbose:
            logger.info(f"Starting the data scraping from {self.__class__.__name__}")
        news_list: List[News] = []
        try:
            news_list = await self._scrape(**kwargs)
        except Exception as e:
            logger.error(f"Error occurred in {self.__class__.__name__} | {e}")
            log_traceback()
        return news_list

    @classmethod
    def inheritors(cls):
        """
        Returns a list of subclasses of the current class.

        Returns:
            List[type]: A list of subclasses.
        """
        subclasses = cls.__subclasses__()
        logger.info(f"Subclasses of {cls.__name__}: {subclasses}")
        return subclasses

    @abstractmethod
    async def _scrape(self, **kwargs) -> List[News]:
        """
        Abstract method to be implemented by subclasses for specific scraping logic.

        Args:
            **kwargs: Additional keyword arguments for scraping options.
        """
        raise NotImplementedError


class ScraperMixins:
    """
    Mixins class providing utility methods for scrapers.
    """

    @staticmethod
    async def get_text_content(raw_content: str, find_by: str = None) -> str:
        """
        Extracts text content from raw HTML using BeautifulSoup.

        Args:
            raw_content (str): Raw HTML content.
            find_by (str, optional): HTML tag to find and extract text from. Defaults to None.

        Returns:
            str: Extracted text content.
        """
        bs4_obj = BeautifulSoup(raw_content, "html.parser")
        text_content = ""
        if find_by:
            target_component = bs4_obj.find(find_by)
            text_content = target_component.get_text() if target_component else ""
        else:
            text_content = bs4_obj.get_text()

        return text_content

    @staticmethod
    async def fetch_html_content(url: str) -> str:
        """
        Fetches HTML content from a URL using Playwright.

        Args:
            url (str): URL to fetch content from.
            browser_type (str): Browser type to use with Playwright (default is "chromium").

        Returns:
            str: Fetched HTML content.
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            html_content = None
            try:
                await page.goto(url, timeout=60000)  # 60 seconds timeout
                await page.wait_for_load_state("networkidle")
                html_content = await page.content()
            except requests.exceptions.Timeout as e:
                logger.warning(f"Timeout error fetching {url}: {e}")
            except requests.exceptions.RequestException as e:
                logger.warning(f"Request error fetching {url}: {e}")
            except Exception as e:
                logger.warning(f"Error fetching {url}: {e}")
            finally:
                await browser.close()
            return html_content
