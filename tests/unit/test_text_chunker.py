
from app.ingestion.text_chunker import TextChunker


def test_create_chunks():
    """Check whether PDF text is divided into chunks."""

    pages = [
        {
            "page_number": 1,
            "text": "Artificial Intelligence\n\nMachine Learning"
        }
    ]

    chunker = TextChunker(
        chunk_size=1200,
        chunk_overlap=150
    )

    chunks = chunker.create_chunks(pages)

    assert len(chunks) == 1
    assert chunks[0]["page_number"] == 1
    assert "Artificial Intelligence" in chunks[0]["text"]
    assert "Machine Learning" in chunks[0]["text"]


def test_chunk_ids():
    """Check whether chunk IDs are assigned correctly."""

    pages = [
        {
            "page_number": 1,
            "text": "A" * 25
        }
    ]

    chunker = TextChunker(
        chunk_size=10,
        chunk_overlap=2
    )

    chunks = chunker.create_chunks(pages)

    chunk_ids = [chunk["chunk_id"] for chunk in chunks]

    assert chunk_ids == [0, 1, 2, 3]


def test_page_number_preservation():
    """Check whether page numbers are preserved."""

    pages = [
        {"page_number": 1, "text": "First page content"},
        {"page_number": 2, "text": "Second page content"}
    ]

    chunker = TextChunker()

    chunks = chunker.create_chunks(pages)

    assert chunks[0]["page_number"] == 1
    assert chunks[1]["page_number"] == 2


def test_empty_pages():
    """Check whether empty input returns an empty list."""

    chunker = TextChunker()

    chunks = chunker.create_chunks([])

    assert chunks == []
