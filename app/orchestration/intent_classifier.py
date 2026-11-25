
import re


class IntentClassifier:
    """Identifies what the user wants from their message."""

    def classify(self, question: str) -> str:
        """Classify the user's question into an intent."""

        if not question or not question.strip():
            raise ValueError("Question cannot be empty.")

        text = question.lower().strip()

        # Check for summarization requests
        summary_patterns = [
            r"\bsummarize\b",
            r"\bsummary\b",
            r"\bgive me a summary\b",
            r"\bkey points\b"
        ]

        if any(re.search(pattern, text) for pattern in summary_patterns):
            return "summarization"

        # Check for current or external information
        web_patterns = [
            r"\blatest\b",
            r"\bcurrent\b",
            r"\btoday\b",
            r"\bnews\b",
            r"\brecent\b",
            r"\b2026\b"
        ]

        if any(re.search(pattern, text) for pattern in web_patterns):
            return "web_search"

        # Check for document-related questions
        document_patterns = [
            r"\baccording to the document\b",
            r"\baccording to the pdf\b",
            r"\bin the document\b",
            r"\bin the pdf\b",
            r"\bfrom my document\b",
            r"\buploaded document\b"
        ]

        if any(re.search(pattern, text) for pattern in document_patterns):
            return "document_question"

        # Default intent
        return "general_question"
