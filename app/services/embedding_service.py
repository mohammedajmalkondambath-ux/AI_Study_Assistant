

import numpy as np
from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """
    Handles text embedding generation using BGE-M3.
    """

    MODEL_NAME = "BAAI/bge-m3"
    EMBEDDING_DIMENSION = 1024

    def __init__(self, device: str = "cpu"):
        self.device = device
        self.model = None

    def load_model(self) -> None:
        """Load the embedding model once."""

        if self.model is None:
            print(f"Loading embedding model: {self.MODEL_NAME}")

            self.model = SentenceTransformer(
                self.MODEL_NAME,
                device=self.device
            )

            print("Embedding model loaded successfully.")

    def generate_embeddings(
        self,
        texts: list[str]
    ) -> np.ndarray:
        """
        Convert multiple text inputs into embeddings.
        """

        if not texts:
            raise ValueError("Text list cannot be empty.")

        if any(not isinstance(text, str) or not text.strip() for text in texts):
            raise ValueError("All inputs must be non-empty strings.")

        self.load_model()

        embeddings = self.model.encode(
            texts,
            batch_size=8,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False
        )

        return embeddings

    def generate_query_embedding(self, query: str) -> np.ndarray:
        """Generate an embedding for a search query."""

        if not isinstance(query, str) or not query.strip():
            raise ValueError("Query cannot be empty.")

        return self.generate_embeddings([query])[0]
