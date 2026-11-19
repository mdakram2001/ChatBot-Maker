
from langchain_text_splitters import RecursiveCharacterTextSplitter

from chatamu.config.settings import settings
from chatamu.logger.logging_config import logger

def clean_text(text: str) -> str:

    text = text.replace("\x00", " ")
    text = "\n".join(
        line.strip()
        for line in text.splitlines()
        if line.strip()
    )

    return text.strip()

def split_documents(documents: list):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    cleaned_documents = []

    for document in documents:

        document.page_content = clean_text(
            document.page_content
        )

        if document.page_content:
            cleaned_documents.append(document)

    chunks = splitter.split_documents(cleaned_documents)

    logger.info(
        f"Created {len(chunks)} chunks from "
        f"{len(cleaned_documents)} documents"
    )

    return chunks