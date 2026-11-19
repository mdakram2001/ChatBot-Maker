
from langchain_core.documents import Document

from chatamu.core import crawler


def test_recursive_crawling(monkeypatch):

    def fake_extract(url):

        html = ""

        if url == "https://example.com":
            html = '<a href="/about">About</a>'

        return (
            Document(
                page_content="Sample website content",
                metadata={"source": url}
            ),
            html
        )

    def fake_classify(url, root_url, anchor_text=""):

        from chatamu.models.url_model import URLClassification

        return URLClassification(
            url=url,
            decision="approve",
            url_type="webpage",
            reason="Relevant webpage"
        )

    monkeypatch.setattr(
        crawler,
        "extract_page",
        fake_extract
    )

    monkeypatch.setattr(
        crawler,
        "classify_url",
        fake_classify
    )

    documents, summary = crawler.crawl_website(
        "https://example.com"
    )

    assert len(documents) == 2
    assert summary.pages_processed == 2
    assert summary.status == "completed"
