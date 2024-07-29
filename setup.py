from setuptools import find_packages, setup

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="newsllm",
    version="0.1.0",
    author="Aayush Shah Kanu",
    author_email="aayushshah196@gmail.com",
    description="A package for scraping, summarizing, and dispatching news articles using LLMs.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Quirky-AI-Labs/news-llm",
    packages=find_packages(),
    install_requires=required,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
