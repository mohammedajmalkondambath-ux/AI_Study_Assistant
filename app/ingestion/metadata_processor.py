
import uuid
from pathlib import Path


class MetadataProcessor:
    """Adds document information to text chunks."""

    def process_chunks(
        self,
        chunks: list[dict],
        filename: str
    ) -> list[dict]:

        document_id = str(uuid.uuid4())
        processed_chunks = []

        for chunk in chunks:

            metadata = {
                "document_id": document_id,
                "filename": Path(filename).name,
                "chunk_id": chunk["chunk_id"],
                "page_number": chunk["page_number"],
                "content_type": "text",
                "text": chunk["text"]
            }

            processed_chunks.append(metadata)

        return processed_chunks
