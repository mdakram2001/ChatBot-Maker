from chatamu.core.pdf_processor import extract_pdf
from chatamu.logger.logging_config import logger


def process_pdf_urls(pdf_urls: list[str]):

    documents = []
    failed_urls = []

    for url in pdf_urls:

        try:
            document = extract_pdf(url)

            documents.append(document)

        except Exception as e:

            logger.error(
                f"Skipping PDF {url}: {e}"
            )

            failed_urls.append(url)

    logger.info(
        f"PDF processing completed: "
        f"{len(documents)} successful, "
        f"{len(failed_urls)} failed"
    )

    return {
        "documents": documents,
        "processed_count": len(documents),
        "failed_urls": failed_urls
    }
