


class HybridRetriever:
    """Combines BM25 and semantic search using RRF."""

    def __init__(self, k: int = 60):
        self.k = k

    def fuse_results(
        self,
        bm25_results: list[dict],
        semantic_results: list[dict],
        top_k: int = 5
    ) -> list[dict]:
        """Combine search rankings using Reciprocal Rank Fusion."""

        scores = {}
        documents = {}

        for result_list in [bm25_results, semantic_results]:

            for rank, result in enumerate(result_list, start=1):

                chunk = result["chunk"]

                key = (
                    chunk["document_id"],
                    chunk["chunk_id"]
                )

                rrf_score = 1 / (self.k + rank)

                scores[key] = scores.get(key, 0) + rrf_score
                documents[key] = chunk

        ranked_results = []

        for key, score in scores.items():

            ranked_results.append({
                "chunk": documents[key],
                "score": score
            })

        ranked_results.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        return ranked_results[:top_k]
