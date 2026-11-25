
import pytest

from app.orchestration.intent_classifier import IntentClassifier


def test_summarization_intent():
    classifier = IntentClassifier()

    result = classifier.classify("Summarize this PDF")

    assert result == "summarization"


def test_web_search_intent():
    classifier = IntentClassifier()

    result = classifier.classify("What is the latest AI news?")

    assert result == "web_search"


def test_document_question_intent():
    classifier = IntentClassifier()

    result = classifier.classify(
        "What is AI according to the document?"
    )

    assert result == "document_question"


def test_general_question_intent():
    classifier = IntentClassifier()

    result = classifier.classify("What is Python?")

    assert result == "general_question"


def test_empty_question():
    classifier = IntentClassifier()

    with pytest.raises(ValueError):
        classifier.classify("")


def test_whitespace_question():
    classifier = IntentClassifier()

    with pytest.raises(ValueError):
        classifier.classify("   ")
