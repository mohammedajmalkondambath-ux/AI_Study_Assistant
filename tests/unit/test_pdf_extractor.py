
from pathlib import Path

import pymupdf
import pytest

from app.ingestion.pdf_extractor import PDFExtractor


def create_test_pdf(file_path: Path):
    """Create a small PDF for testing."""

    document = pymupdf.open()

    page = document.new_page()
    page.insert_text((50, 50), "Artificial Intelligence")

    document.save(file_path)
    document.close()


def test_extract_text_success(tmp_path):
    """Check whether text is extracted from a PDF."""

    pdf_path = tmp_path / "sample.pdf"
    create_test_pdf(pdf_path)

    extractor = PDFExtractor()
    pages = extractor.extract_text(str(pdf_path))

    assert len(pages) == 1
    assert pages[0]["page_number"] == 1
    assert "Artificial Intelligence" in pages[0]["text"]


def test_file_not_found():
    """Check whether a missing PDF raises an error."""

    extractor = PDFExtractor()

    with pytest.raises(FileNotFoundError):
        extractor.extract_text("missing.pdf")


def test_invalid_file_extension(tmp_path):
    """Check whether non-PDF files are rejected."""

    text_file = tmp_path / "sample.txt"
    text_file.write_text("This is a test file.")

    extractor = PDFExtractor()

    with pytest.raises(ValueError):
        extractor.extract_text(str(text_file))


def test_empty_pdf(tmp_path):
    """Check whether an empty PDF returns no pages."""

    pdf_path = tmp_path / "empty.pdf"

    document = pymupdf.open()
    document.new_page()
    document.save(pdf_path)
    document.close()

    extractor = PDFExtractor()
    pages = extractor.extract_text(str(pdf_path))

    assert pages == []
