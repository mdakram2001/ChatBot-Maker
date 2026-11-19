
from io import BytesIO

import requests
from pypdf import PdfReader
from langchain_core.documents import Document

from chatamu.config.settings import settings
from chatamu.exception.custom_exceptions import (
    PDFExtractionException
)
from chatamu.logger.logging_config import logger


def extract_pdf(url: str) -> Document:

    try:
        logger.info(f"Downloading PDF: {url}")

        response = requests.get(
            url,
            timeout=settings.REQUEST_TIMEOUT,
            headers={
                "User-Agent": "ChatAMU/1.0"
            },
            allow_redirects=False,
            verify=False
        )

        response.raise_for_status()

        # Validate PDF content
        content_type = response.headers.get(
            "Content-Type", ""
        ).lower()

        if (
            "application/pdf" not in content_type
            and not response.content.startswith(b"%PDF-")
        ):
            raise PDFExtractionException(
                "URL does not contain a valid PDF"
            )

        # Read PDF
        pdf = PdfReader(BytesIO(response.content))

        if pdf.is_encrypted:
            raise PDFExtractionException(
                "Encrypted PDFs are not supported"
            )

        # Extract text from all pages
        extracted_text = []

        for page_number, page in enumerate(pdf.pages, start=1):

            text = page.extract_text()

            if text:
                extracted_text.append(
                    f"Page {page_number}\n{text}"
                )

        content = "\n\n".join(extracted_text)

        if not content.strip():
            raise PDFExtractionException(
                "No extractable text found in PDF"
            )

        # Convert into LangChain Document
        document = Document(
            page_content=content,
            metadata={
                "source": url,
                "document_type": "pdf",
                "page_count": len(pdf.pages)
            }
        )

        logger.info(f"Successfully extracted PDF: {url}")

        return document

    except PDFExtractionException:
        raise

    except Exception as e:

        logger.error(f"PDF extraction failed: {url} | {e}")

        raise PDFExtractionException(
            f"Failed to process PDF: {url}"
        ) from e
