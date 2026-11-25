
from app.ingestion.pdf_extractor import PDFExtractor
from app.services.map_reduce_summary import MapReduceSummary
from app.services.summary_service import SummaryService


class DocumentService:
    """Handles PDF extraction and summarization."""

    def __init__(self):
        self.pdf_extractor = PDFExtractor()
        self.summary_service = SummaryService()
        self.map_reduce_summary = MapReduceSummary()

    def summarize_pdf(self, pdf_path: str) -> str:
        """Extract text from a PDF and generate its summary."""

        # Step 1: Extract text from PDF
        pages = self.pdf_extractor.extract_text(pdf_path)

        if not pages:
            raise ValueError("No readable text found in the PDF.")

        # Step 2: Combine all page text
        document_text = "\n\n".join(
            page["text"] for page in pages
        )

        # Step 3: Choose summarization method
        if len(document_text) <= 6000:

            summary = self.summary_service.summarize(
                document_text
            )

        else:

            summary = self.map_reduce_summary.summarize_large_document(
                document_text
            )

        return summary
