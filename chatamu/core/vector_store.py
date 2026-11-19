
import chromadb

from chatamu.config.settings import settings
from chatamu.logger.logging_config import logger

class VectorStore:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_DB_PATH
        )

        self.collection = self.client.get_or_create_collection(
            name="chatamu_documents",
            metadata={"hnsw:space": "cosine"}
        )

        logger.info("ChromaDB initialized")

    def add_documents(self, chunks: list, embeddings: list):

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Chunks and embeddings count mismatch"
            )

        if not chunks:
            return

        ids = [
            f"chunk_{self.collection.count() + i}"
            for i in range(len(chunks))
        ]

        self.collection.add(
            ids=ids,
            documents=[
                chunk.page_content for chunk in chunks
            ],
            embeddings=embeddings,
            metadatas=[
                chunk.metadata for chunk in chunks
            ]
        )

        logger.info(f"Stored {len(chunks)} chunks")

    def search(self, query_embedding: list, top_k: int = 5):

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(
                top_k,
                self.collection.count()
            )
        )

        return results

vector_store = VectorStore()