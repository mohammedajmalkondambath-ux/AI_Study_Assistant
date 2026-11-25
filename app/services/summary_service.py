
from app.services.llm_service import LLMService


class SummaryService:
    """Summarizes document content using Groq."""

    def __init__(self):
        self.llm_service = LLMService()

    def summarize(self, text: str) -> str:
        """Generate a summary of the provided document text."""

        if not text or not text.strip():
            raise ValueError("Document text cannot be empty.")

        prompt = (
            "Summarize the following document in simple English. "
            "Include the main ideas and important points. "
            "Use clear headings and bullet points where appropriate.\n\n"
            f"Document:\n{text}"
        )

        return self.llm_service.generate_answer(
            question=prompt
        )
