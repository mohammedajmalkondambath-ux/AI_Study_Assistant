

from app.services.summary_service import SummaryService


class MapReduceSummary:
    """Summarizes large documents using Map-Reduce."""

    def __init__(self):
        self.summary_service = SummaryService()

    def split_text(
        self,
        text: str,
        chunk_size: int = 6000
    ) -> list[str]:
        """Divide document text into smaller sections."""

        if not text or not text.strip():
            raise ValueError("Document text cannot be empty.")

        return [
            text[i:i + chunk_size]
            for i in range(0, len(text), chunk_size)
        ]

    def summarize_large_document(self, text: str) -> str:
        """Summarize a large document using Map-Reduce."""

        # MAP: Split document into smaller sections
        chunks = self.split_text(text)

        # MAP: Summarize each section
        summaries = []

        for index, chunk in enumerate(chunks, start=1):
            print(f"Summarizing section {index}/{len(chunks)}...")

            summary = self.summary_service.summarize(chunk)

            summaries.append(summary)

        # REDUCE: Combine all section summaries
        combined_summary = "\n\n".join(summaries)

        # Generate the final summary
        if len(summaries) == 1:
            return combined_summary

        print("Combining section summaries...")

        final_summary = self.summary_service.summarize(
            combined_summary
        )

        return final_summary
