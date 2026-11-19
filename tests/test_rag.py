
from langchain_core.documents import Document

from chatamu.core.text_processor import split_documents

def test_document_chunking():

    documents = [
        Document(
            page_content="This is sample website content. " * 200,
            metadata={"source": "https://example.com"}
        )
    ]

    chunks = split_documents(documents)

    assert len(chunks) > 1

    for chunk in chunks:
        assert chunk.page_content
        assert chunk.metadata["source"] == "https://example.com"