


class ContextBuilder:
    """Builds context from retrieved document chunks."""

    def build_context(
        self,
        results: list[dict],
        max_chunks: int = 5
    ) -> dict:
        """Prepare document context and citation information."""

        if max_chunks < 1:
            raise ValueError("max_chunks must be at least 1.")

        selected_results = results[:max_chunks]

        context_parts = []
        citations = []

        for index, result in enumerate(selected_results, start=1):

            chunk = result["chunk"]

            text = chunk["text"]
            filename = chunk.get("filename", "Unknown document")
            page_number = chunk.get("page_number", "Unknown")

            context_parts.append(
                f"[Source {index}]\n"
                f"Document: {filename}\n"
                f"Page: {page_number}\n"
                f"Content:\n{text}"
            )

            citations.append({
                "source": index,
                "document_id": chunk.get("document_id"),
                "filename": filename,
                "page_number": page_number,
                "chunk_id": chunk.get("chunk_id")
            })

        context = "\n\n".join(context_parts)

        return {
            "context": context,
            "citations": citations
        }
