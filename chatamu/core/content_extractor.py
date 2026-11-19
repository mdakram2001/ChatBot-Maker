import requests
import certifi
import os

from langchain_community.document_loaders import WebBaseLoader

from chatamu.config.settings import settings
from chatamu.exception.custom_exceptions import (
    WebExtractionException
)
from chatamu.logger.logging_config import logger

os.environ["USER_AGENT"] = "ChatAMU/1.0"

headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            ),
            "Accept": (
                "text/html,application/xhtml+xml,"
                "application/xml;q=0.9,image/avif,image/webp,"
                "image/apng,*/*;q=0.8"
            ),
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "sec-ch-ua": '"Chromium";v="131", "Google Chrome";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"'
        }



def extract_page(url: str):

    try:
        logger.info(f"Extracting webpage: {url}")

        # Retrieve HTML for URL discovery
        response = requests.get(
            url,
            timeout=settings.REQUEST_TIMEOUT,
            headers = headers,
            allow_redirects=False,
            # verify = certifi.where()
            verify = False
        )

        response.raise_for_status()

        content_type = response.headers.get(
            "Content-Type", ""
        ).lower()

        if "text/html" not in content_type:
            raise WebExtractionException(
                f"Unsupported content type: {content_type}"
            )

        html = response.text

        # Extract content using LangChain
        loader = WebBaseLoader(
            web_path=url,
            requests_kwargs={
                "timeout": settings.REQUEST_TIMEOUT,
                "headers": headers,
                "verify": False
            }
        )

        documents = loader.load()

        if not documents:
            raise WebExtractionException(
                "No content extracted"
            )

        document = documents[0]

        # Ensure source metadata is available
        document.metadata["source"] = url

        logger.info(f"Successfully extracted: {url}")

        return document, html

    except Exception as e:

        logger.error(f"Extraction failed for {url}: {e}")

        raise WebExtractionException(
            f"Failed to extract {url}: {str(e)}"
        ) from e
