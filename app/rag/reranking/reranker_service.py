

from sentence_transformers import CrossEncoder


class RerankerService:
    """Reranks retrieved document chunks using a local model."""

    MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

    def __init__(self, device: str = "cpu"):
        self.device = device
        self.model = None

    def load_model(self) -> None:
        """Load the reranking model once."""

        if self.model is None:
            print("Loading reranking model...")

            self.model = CrossEncoder(
                self.MODEL_NAME,
                device=self.device
            )

            print("Reranking model loaded successfully.")

    def rerank(
        self,
        query: str,
        results: list[dict],
        top_k: int = 5
    ) -> list[dict]:
        """Reorder retrieved chunks by relevance."""

        if not query.strip():
            raise ValueError("Query cannot be empty.")

        if top_k < 1:
            raise ValueError("top_k must be at least 1.")

        if not results:
            return []

        self.load_model()

        pairs = [
            [query, result["chunk"]["text"]]
            for result in results
        ]

        scores = self.model.predict(pairs)

        reranked_results = []

        for result, score in zip(results, scores):

            reranked_results.append({
                "chunk": result["chunk"],
                "score": float(score)
            })

        reranked_results.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        return reranked_results[:top_k]
