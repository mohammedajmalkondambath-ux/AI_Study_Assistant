
from groq import Groq

from app.core.config import settings


class LLMService:
    """Generates AI responses using the Groq API."""

    MODEL_NAME = "openai/gpt-oss-120b"

    def __init__(self):
        if not settings.GROQ_API_KEY:
            raise ValueError("Groq API key is missing.")

        self.client = Groq(
            api_key=settings.GROQ_API_KEY
        )

    def generate_answer(
        self,
        question: str,
        context: str = ""
    ) -> str:
        """Generate an answer using the question and context."""

        if not question.strip():
            raise ValueError("Question cannot be empty.")

        if context.strip():
            system_prompt = (
                "You are a helpful AI Study Assistant. "
                "Answer the user's question using the provided "
                "document context. If the answer is not available "
                "in the context, clearly say so. Do not invent "
                "information. Include source references when available."
            )
        else:
            system_prompt = (
                "You are a helpful AI Study Assistant. "
                "Answer the user's general question clearly and accurately."
            )

        user_message = (
            f"Document Context:\n{context}\n\n"
            f"Question:\n{question}"
        )

        response = self.client.chat.completions.create(
            model=self.MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            temperature=0.2
        )

        return response.choices[0].message.content
