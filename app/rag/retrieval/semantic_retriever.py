

from app.services.embedding_service import EmbeddingService
from app.services.qdrant_service import QdrantService


class SemanticRetriever:
    """Performs semantic search using BGE-M3 and Qdrant."""

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.qdrant_service = QdrantService()

    def search(
        self,
        query: str,
        top_k: int = 5,
        document_id: str | None = None
    ) -> list[dict]:
        """Find relevant chunks based on semantic meaning."""

        if not query.strip():
            raise ValueError("Search query cannot be empty.")

        if top_k < 1:
            raise ValueError("top_k must be at least 1.")

        query_vector = (
            self.embedding_service.generate_query_embedding(query)
        )

        query_filter = None

        if document_id:
            query_filter = {
                "must": [
                    {
                        "key": "document_id",
                        "match": {"value": document_id}
                    }
                ]
            }

        results = self.qdrant_service.client.query_points(
            collection_name=self.qdrant_service.COLLECTION_NAME,
            query=query_vector.tolist(),
            query_filter=query_filter,
            limit=top_k,
            with_payload=True
        )

        return [
            {
                "chunk": point.payload,
                "score": float(point.score)
            }
            for point in results.points
        ]

    def close(self) -> None:
        """Close database connections."""

        self.qdrant_service.close()
