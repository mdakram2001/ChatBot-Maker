
from chatamu.core.vector_store import vector_store
from chatamu.core.embedding import embedding_model

from chatamu.services.embedding_service import (
    generate_embeddings
)

from chatamu.logger.logging_config import logger

def index_documents(documents: list):

    logger.info("Starting document indexing")

    chunks, embeddings = generate_embeddings(documents)

    vector_store.add_documents(
        chunks,
        embeddings
    )

    return {
        "chunks_processed": len(chunks),
        "status": "completed"
    }

def search_documents(query: str, top_k: int = 5):

    query_embedding = embedding_model.embed_query(query)

    results = vector_store.search(
        query_embedding,
        top_k
    )

    return results