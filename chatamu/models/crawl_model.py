
from pydantic import BaseModel
from typing import Literal


class CrawlSummary(BaseModel):

    root_url: str

    status: Literal[
        "completed",
        "failed"
    ]

    pages_discovered: int = 0

    pages_processed: int = 0

    pages_failed: int = 0

    pdf_urls: list[str] = []

    failed_urls: list[str] = []
