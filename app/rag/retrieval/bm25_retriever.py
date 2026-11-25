
import re

from rank_bm25 import BM25Okapi


class BM25Retriever:
    """Performs keyword-based document retrieval using BM25."""

    def __init__(self):
        self.documents: list[dict] = []
        self.bm25 = None

    def tokenize(self, text: str) -> list[str]:
        """Convert text into lowercase words."""

        return re.findall(r"\b\w+\b", text.lower())

    def index_documents(self, chunks: list[dict]) -> None:
        """Build a BM25 index from document chunks."""

        if not chunks:
            raise ValueError("Document chunks cannot be empty.")

        valid_chunks = [
            chunk for chunk in chunks
            if chunk.get("text", "").strip()
        ]

        if not valid_chunks:
            raise ValueError("No valid text found in document chunks.")

        tokenized_documents = [
            self.tokenize(chunk["text"])
            for chunk in valid_chunks
        ]

        self.documents = valid_chunks
        self.bm25 = BM25Okapi(tokenized_documents)

        print(f"BM25 index created with {len(valid_chunks)} chunks.")

    def search(
        self,
        query: str,
        top_k: int = 5,
        document_id: str | None = None
    ) -> list[dict]:
        """Find the most relevant chunks using keyword matching."""

        if self.bm25 is None:
            raise ValueError("Please index documents before searching.")

        if not query.strip():
            raise ValueError("Search query cannot be empty.")

        if top_k < 1:
            raise ValueError("top_k must be at least 1.")

        query_tokens = self.tokenize(query)

        if not query_tokens:
            return []

        scores = self.bm25.get_scores(query_tokens)

        results = []

        for index, score in enumerate(scores):

            chunk = self.documents[index]

            if (
                document_id is not None
                and chunk.get("document_id") != document_id
            ):
                continue

            results.append({
                "chunk": chunk,
                "score": float(score)
            })

        results.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        return results[:top_k]
