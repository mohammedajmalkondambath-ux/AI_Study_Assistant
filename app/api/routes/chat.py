
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.orchestration.graph import AssistantGraph

router = APIRouter()

# Create the AI assistant
assistant = AssistantGraph()


class ChatRequest(BaseModel):
    """Structure of the user's chat request."""

    question: str
    document_id: str | None = None


@router.post("/chat")
def chat(request: ChatRequest):
    """Process a user's question using LangGraph."""

    try:
        result = assistant.run(
            question=request.question,
            document_id=request.document_id
        )

        return {
            "question": request.question,
            "intent": result.get("intent"),
            "answer": result.get("answer"),
            "citations": result.get("citations", []),
            "search_results": result.get("search_results", [])
        }

    except (ValueError, RuntimeError) as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        ) from error
