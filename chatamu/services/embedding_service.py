
from chatamu.core.text_processor import split_documents
from chatamu.core.embedding import embedding_model

from chatamu.logger.logging_config import logger

def generate_embeddings(documents: list):

    logger.info("Starting embedding generation")

    # Split documents into chunks
    chunks = split_documents(documents)

    if not chunks:
        return [], []

    # Generate embeddings
    texts = [
        chunk.page_content for chunk in chunks
    ]

    embeddings = embedding_model.embed_documents(texts)

    logger.info(
        f"Generated {len(embeddings)} embeddings"
    )

    return chunks, embeddings