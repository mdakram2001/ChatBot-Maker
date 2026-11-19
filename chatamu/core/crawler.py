from collections import deque

from chatamu.core.content_extractor import extract_page
from chatamu.core.url_discovery import discover_urls
from chatamu.core.url_validator import (
    normalize_url,
    validate_url
)
from chatamu.core.url_classifier import classify_url

from chatamu.config.settings import settings
from chatamu.models.crawl_model import CrawlSummary
from chatamu.logger.logging_config import logger


def crawl_website(root_url: str):

    root_url = normalize_url(root_url)

    # Queue contains (URL, depth)
    queue = deque([(root_url, 0)])

    # Prevent duplicate processing
    visited_urls = set()

    # Store extracted LangChain Documents
    documents = []

    # Store PDF URLs separately
    pdf_urls = []

    # Track failures
    failed_urls = []

    pages_discovered = 1

    while queue and len(documents) < settings.MAX_PAGES:

        current_url, depth = queue.popleft()

        if current_url in visited_urls:
            continue

        visited_urls.add(current_url)

        # Check crawl depth
        if depth > settings.MAX_CRAWL_DEPTH:
            continue

        try:

            logger.info(f"Crawling: {current_url}")

            # Extract webpage
            document, html = extract_page(current_url)

            documents.append(document)

            # Discover URLs
            discovered_urls = discover_urls(
                html,
                current_url
            )

            logger.info(
                f"Discovered {len(discovered_urls)} URLs "
                f"on {current_url}"
            )

            for item in discovered_urls:

                url = item.url

                if url in visited_urls:
                    continue

                # Enforce root-domain boundary
                try:
                    validate_url(url, root_url)

                except Exception:
                    continue

                # Classify URL
                result = classify_url(
                    url=url,
                    root_url=root_url,
                    anchor_text=item.anchor_text
                )

                # Handle PDF separately
                if result.decision == "pdf":

                    if url not in pdf_urls:
                        pdf_urls.append(url)

                    continue

                # Queue approved webpages
                if result.decision == "approve":

                    if len(visited_urls) + len(queue) >= settings.MAX_PAGES:
                        continue

                    queue.append((url, depth + 1))

                    pages_discovered += 1

        except Exception as e:

            logger.error(
                f"Failed to crawl {current_url}: {e}"
            )

            failed_urls.append(current_url)

    # Determine final status
    status = (
        "completed" if documents else "failed"
    )

    summary = CrawlSummary(
        root_url=root_url,
        status=status,
        pages_discovered=pages_discovered,
        pages_processed=len(documents),
        pages_failed=len(failed_urls),
        pdf_urls=pdf_urls,
        failed_urls=failed_urls
    )

    logger.info("Website crawling finished")

    return documents, summary
