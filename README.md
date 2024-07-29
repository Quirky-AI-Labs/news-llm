# newsllm

<div align="center">
<br>
<h1>newsllm</h1>
<p>A package for scraping, summarizing, and dispatching news articles using LLMs.</p>
<br/>
</div>

## Features

<!-- start features -->

📰 _Comprehensive News Handling_

- Scrapes news from multiple sources.
- Summarizes articles using advanced LLMs.
- Dispatches news summaries to various channels.

🧠 _Powered by Large Language Models_

- Utilizes state-of-the-art LLMs for summarization.
- Configurable to use different providers (e.g., OpenAI, OpenRouter).

📦 _Modular Design_

- Easy to extend with custom scrapers and summarizers.
- Clean and well-documented API.

## Installation

```bash
pip install newsllm
```

## Usage

```py
from newsllm.services.scraper import HackerNewsScraper
from newsllm.services.summarizer import Summarizer

# Initialize the scraper
scraper = HackerNewsScraper()

# Initialize the summarizer
summarizer = Summarizer()

# Scrape the top stories from HackerNews
import asyncio
loop = asyncio.get_event_loop()
news_list = loop.run_until_complete(scraper.scrape())

# Print the scraped news
for news in news_list:
    summary_dict = summarizer.summarize(news.text_content)
    news.summary = summary_dict.get("summary", "")
    news.tags = summary_dict.get("tags", [])
```

## Contributing

If you find a bug 🐛, please open a bug report. If you have an idea for an improvement or new feature 🚀, please open a feature request.
