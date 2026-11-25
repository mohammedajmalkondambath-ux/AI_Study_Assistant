
from app.ingestion.metadata_processor import MetadataProcessor


def test_process_chunks_success():
    """Check whether metadata is added correctly."""

    chunks = [
        {
            "chunk_id": 0,
            "page_number": 1,
            "text": "Artificial Intelligence"
        },
        {
            "chunk_id": 1,
            "page_number": 2,
            "text": "Machine Learning"
        }
    ]

    processor = MetadataProcessor()
    result = processor.process_chunks(chunks, "sample.pdf")

    assert len(result) == 2
    assert result[0]["filename"] == "sample.pdf"
    assert result[0]["chunk_id"] == 0
    assert result[0]["page_number"] == 1
    assert result[0]["content_type"] == "text"
    assert result[0]["text"] == "Artificial Intelligence"


def test_same_document_id_for_all_chunks():
    """Check whether all chunks share the same document ID."""

    chunks = [
        {"chunk_id": 0, "page_number": 1, "text": "First chunk"},
        {"chunk_id": 1, "page_number": 2, "text": "Second chunk"}
    ]

    processor = MetadataProcessor()
    result = processor.process_chunks(chunks, "sample.pdf")

    assert result[0]["document_id"] == result[1]["document_id"]


def test_filename_without_folder_path():
    """Check whether only the filename is stored."""

    chunks = [
        {"chunk_id": 0, "page_number": 1, "text": "Test content"}
    ]

    processor = MetadataProcessor()
    result = processor.process_chunks(
        chunks,
        "documents/sample.pdf"
    )

    assert result[0]["filename"] == "sample.pdf"


def test_empty_chunks():
    """Check whether empty input returns an empty list."""

    processor = MetadataProcessor()
    result = processor.process_chunks([], "sample.pdf")

    assert result == []
