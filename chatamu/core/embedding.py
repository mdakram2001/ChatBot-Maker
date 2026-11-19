
from sentence_transformers import SentenceTransformer

from chatamu.config.settings import settings
from chatamu.logger.logging_config import logger

class EmbeddingModel:

    def __init__(self):

        logger.info("Loading embedding model")

        self.model = SentenceTransformer(
            settings.EMBEDDING_MODEL
        )

    def embed_documents(self, texts: list[str]):

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False
        )

        return embeddings.tolist()

    def embed_query(self, text: str):

        embedding = self.model.encode(
            text,
            normalize_embeddings=True
        )

        return embedding.tolist()

embedding_model = EmbeddingModel()