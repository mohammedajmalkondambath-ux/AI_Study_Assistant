


class TextChunker:
    """Divides extracted PDF text into smaller chunks."""

    def __init__(
        self,
        chunk_size: int = 1200,
        chunk_overlap: int = 150
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def create_chunks(
        self,
        pages: list[dict]
    ) -> list[dict]:
        """Create chunks while preserving page information."""

        chunks = []
        chunk_id = 0

        for page in pages:

            page_number = page["page_number"]
            text = page["text"]

            paragraphs = [
                paragraph.strip()
                for paragraph in text.split("\n\n")
                if paragraph.strip()
            ]

            current_chunk = ""

            for paragraph in paragraphs:

                if len(paragraph) > self.chunk_size:
                    if current_chunk:
                        chunks.append({
                            "chunk_id": chunk_id,
                            "page_number": page_number,
                            "text": current_chunk.strip()
                        })
                        chunk_id += 1
                        current_chunk = ""

                    start = 0

                    while start < len(paragraph):
                        end = start + self.chunk_size

                        chunks.append({
                            "chunk_id": chunk_id,
                            "page_number": page_number,
                            "text": paragraph[start:end].strip()
                        })

                        chunk_id += 1
                        start += self.chunk_size - self.chunk_overlap

                    continue

                if (
                    current_chunk
                    and len(current_chunk) + len(paragraph) + 2
                    > self.chunk_size
                ):
                    chunks.append({
                        "chunk_id": chunk_id,
                        "page_number": page_number,
                        "text": current_chunk.strip()
                    })

                    chunk_id += 1

                    overlap_text = current_chunk[
                        -self.chunk_overlap:
                    ]

                    current_chunk = overlap_text + "\n\n" + paragraph

                else:
                    if current_chunk:
                        current_chunk += "\n\n" + paragraph
                    else:
                        current_chunk = paragraph

            if current_chunk.strip():
                chunks.append({
                    "chunk_id": chunk_id,
                    "page_number": page_number,
                    "text": current_chunk.strip()
                })

                chunk_id += 1

        return chunks
