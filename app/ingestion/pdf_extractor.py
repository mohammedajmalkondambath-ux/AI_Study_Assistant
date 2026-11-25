
from pathlib import Path

import pymupdf


class PDFExtractor:
    """Extracts text from PDF documents."""

    def extract_text(self, pdf_path: str) -> list[dict]:
        """Extract text page by page."""

        file_path = Path(pdf_path)

        if not file_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        if file_path.suffix.lower() != ".pdf":
            raise ValueError("Only PDF files are supported.")

        pages = []

        with pymupdf.open(file_path) as document:

            for page_number, page in enumerate(document, start=1):

                text = page.get_text("text").strip()

                if text:
                    pages.append({
                        "page_number": page_number,
                        "text": text
                    })

        return pages
