
import uuid
from typing import Any

from qdrant_client import QdrantClient, models


class QdrantService:
    """Manages vector storage and search using Qdrant."""

    COLLECTION_NAME = "study_documents"
    VECTOR_SIZE = 1024

    def __init__(self, url: str = "http://localhost:6333"):
        self.client = QdrantClient(url=url)

    def create_collection(self) -> None:
        """Create the collection if it does not exist."""

        if self.client.collection_exists(self.COLLECTION_NAME):
            print("Qdrant collection already exists.")
            return

        self.client.create_collection(
            collection_name=self.COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=self.VECTOR_SIZE,
                distance=models.Distance.COSINE
            )
        )

        print("Qdrant collection created successfully.")

    def store_chunks(
        self,
        chunks: list[dict],
        embeddings: Any
    ) -> None:
        """Store document chunks and their embeddings."""

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Number of chunks and embeddings must match."
            )

        self.create_collection()

        points = []

        for chunk, embedding in zip(chunks, embeddings):

            point_id = str(
                uuid.uuid5(
                    uuid.NAMESPACE_URL,
                    f"{chunk['document_id']}_{chunk['chunk_id']}"
                )
            )

            points.append(
                models.PointStruct(
                    id=point_id,
                    vector=embedding.tolist(),
                    payload=chunk
                )
            )

        if points:
            self.client.upsert(
                collection_name=self.COLLECTION_NAME,
                points=points,
                wait=True
            )

        print(f"Successfully stored {len(points)} chunks in Qdrant.")

    def get_collection_info(self) -> Any:
        """Return collection information."""

        return self.client.get_collection(
            collection_name=self.COLLECTION_NAME
        )

    def close(self) -> None:
        """Close the Qdrant connection."""

        self.client.close()
