
import shutil
import uuid
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile

from app.api.routes.chat import assistant
from app.ingestion.metadata_processor import MetadataProcessor
from app.ingestion.pdf_extractor import PDFExtractor
from app.ingestion.text_chunker import TextChunker
from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService
from app.services.mongodb_service import MongoDBService
from app.services.qdrant_service import QdrantService

router = APIRouter()


@router.post("/documents")
def upload_document(file: UploadFile):
    """Upload and process a PDF document."""

    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    upload_dir = Path("uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)

    safe_filename = Path(file.filename).name
    saved_filename = f"{uuid.uuid4()}_{safe_filename}"
    file_path = upload_dir / saved_filename

    try:
        # Step 1: Save the PDF
        with file_path.open("wb") as destination:
            shutil.copyfileobj(file.file, destination)

        # Step 2: Extract PDF text
        extractor = PDFExtractor()
        pages = extractor.extract_text(str(file_path))

        if not pages:
            raise ValueError("No readable text found in the PDF.")

        # Step 3: Create text chunks
        chunker = TextChunker()
        chunks = chunker.create_chunks(pages)

        if not chunks:
            raise ValueError("No text chunks were created.")

        # Step 4: Add metadata
        processor = MetadataProcessor()
        chunks = processor.process_chunks(chunks, safe_filename)

        document_id = chunks[0]["document_id"]

        # Step 5: Generate embeddings
        embedding_service = EmbeddingService()
        embeddings = embedding_service.generate_embeddings(
            [chunk["text"] for chunk in chunks]
        )

        # Step 6: Store chunks in Qdrant
        qdrant_service = QdrantService()

        try:
            qdrant_service.store_chunks(chunks, embeddings)
        finally:
            qdrant_service.close()

        # Step 7: Index chunks for BM25 retrieval
        assistant.index_documents(chunks)

        # Step 8: Save document details in MongoDB
        mongodb_service = MongoDBService()

        try:
            collection = mongodb_service.get_collection("documents")

            collection.insert_one({
                "document_id": document_id,
                "filename": safe_filename,
                "total_pages": len(pages),
                "total_chunks": len(chunks),
                "file_path": str(file_path)
            })
        finally:
            mongodb_service.close()

        return {
            "message": "Document uploaded and processed successfully.",
            "document_id": document_id,
            "filename": safe_filename,
            "total_pages": len(pages),
            "total_chunks": len(chunks)
        }

    except (ValueError, OSError, RuntimeError) as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        ) from error

    finally:
        file.file.close()


@router.get("/documents")
def list_documents():
    """Retrieve all uploaded documents from MongoDB."""

    mongodb_service = MongoDBService()

    try:
        collection = mongodb_service.get_collection("documents")

        documents = list(
            collection.find({}, {"_id": 0})
        )

        return {
            "total_documents": len(documents),
            "documents": documents
        }

    except (ValueError, RuntimeError) as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        ) from error

    finally:
        mongodb_service.close()


@router.post("/documents/{document_id}/summary")
def summarize_document(document_id: str):
    """Generate a summary of an uploaded PDF."""

    mongodb_service = MongoDBService()

    try:
        # Step 1: Find the document in MongoDB
        collection = mongodb_service.get_collection("documents")

        document = collection.find_one({
            "document_id": document_id
        })

        if not document:
            raise HTTPException(
                status_code=404,
                detail="Document not found."
            )

        # Step 2: Get the saved PDF path
        file_path = Path(document["file_path"])

        if not file_path.exists():
            raise HTTPException(
                status_code=404,
                detail="The uploaded PDF file could not be found."
            )

        # Step 3: Generate the summary
        summary_service = DocumentService()
        summary = summary_service.summarize_pdf(str(file_path))

        # Step 4: Return the summary
        return {
            "document_id": document_id,
            "filename": document["filename"],
            "summary": summary
        }

    except HTTPException:
        raise

    except (ValueError, OSError, RuntimeError) as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        ) from error

    finally:
        mongodb_service.close()
