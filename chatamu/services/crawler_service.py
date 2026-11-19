
from chatamu.core.crawler import crawl_website
from chatamu.logger.logging_config import logger


def start_crawl(root_url: str):

    logger.info(f"Starting crawl service: {root_url}")

    documents, summary = crawl_website(root_url)

    logger.info(
        f"Crawl completed: {summary.pages_processed} pages"
    )

    return {
        "summary": summary,
        "documents": documents
    }
