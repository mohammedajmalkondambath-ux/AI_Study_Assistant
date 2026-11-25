
from typing import Any, TypedDict


class AssistantState(TypedDict, total=False):
    """Shared state passed between LangGraph nodes."""

    question: str
    document_id: str | None

    intent: str

    retrieved_chunks: list[dict[str, Any]]
    reranked_chunks: list[dict[str, Any]]

    context: str
    answer: str

    citations: list[dict[str, Any]]

    search_results: list[dict[str, Any]]

    summary: str

    error: str | None
