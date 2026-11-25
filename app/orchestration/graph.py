
from typing import Literal

from langgraph.graph import END, START, StateGraph

from app.orchestration.intent_classifier import IntentClassifier
from app.orchestration.state import AssistantState
from app.rag.rag_pipeline import RAGPipeline
from app.services.llm_service import LLMService
from app.services.summary_service import SummaryService
from app.services.web_search_service import WebSearchService


class AssistantGraph:
    """Controls the AI Study Assistant workflow using LangGraph."""

    def __init__(self):

        self.classifier = IntentClassifier()

        self.rag_pipeline = RAGPipeline()

        self.llm_service = LLMService()

        self.summary_service = SummaryService()

        self.web_search_service = WebSearchService()

        workflow = StateGraph(AssistantState)

        # Register workflow nodes
        workflow.add_node(
            "classify_intent",
            self.classify_intent
        )

        workflow.add_node(
            "document_question",
            self.document_question
        )

        workflow.add_node(
            "summarization",
            self.summarization
        )

        workflow.add_node(
            "general_question",
            self.general_question
        )

        workflow.add_node(
            "web_search",
            self.web_search
        )

        # Starting point
        workflow.add_edge(START, "classify_intent")

        # Route based on detected intent
        workflow.add_conditional_edges(
            "classify_intent",
            self.route_intent,
            {
                "document_question": "document_question",
                "summarization": "summarization",
                "general_question": "general_question",
                "web_search": "web_search"
            }
        )

        # End points
        workflow.add_edge("document_question", END)
        workflow.add_edge("summarization", END)
        workflow.add_edge("general_question", END)
        workflow.add_edge("web_search", END)

        self.graph = workflow.compile()

    def classify_intent(
        self,
        state: AssistantState
    ) -> dict:
        """Identify the user's intent."""

        intent = self.classifier.classify(
            state["question"]
        )

        return {
            "intent": intent
        }

    def route_intent(
        self,
        state: AssistantState
    ) -> Literal[
        "document_question",
        "summarization",
        "general_question",
        "web_search"
    ]:
        """Select the correct workflow path."""

        return state["intent"]

    def document_question(
        self,
        state: AssistantState
    ) -> dict:
        """Answer document questions using the RAG pipeline."""

        result = self.rag_pipeline.answer_question(
            question=state["question"],
            document_id=state.get("document_id")
        )

        return {
            "answer": result["answer"],
            "citations": result["citations"]
        }

    def summarization(
        self,
        state: AssistantState
    ) -> dict:
        """Summarize text using the Summary Service."""

        summary = self.summary_service.summarize(
            state["question"]
        )

        return {
            "answer": summary,
            "summary": summary
        }

    def general_question(
        self,
        state: AssistantState
    ) -> dict:
        """Answer general questions using Groq."""

        answer = self.llm_service.generate_answer(
            question=state["question"]
        )

        return {
            "answer": answer
        }

    def web_search(
        self,
        state: AssistantState
    ) -> dict:
        """Search the web and generate an answer using Groq."""

        # Step 1: Search the internet
        search_query = state["question"].strip()

        search_results = self.web_search_service.search(
            query=search_query,
            max_results=5
        )

        if not search_results:
            return {
                "answer": "No relevant web search results were found.",
                "search_results": []
            }

        # Step 2: Prepare search information
        context = "\n\n".join(
            f"Title: {item['title']}\n"
            f"URL: {item['url']}\n"
            f"Description: {item['snippet']}"
            for item in search_results
        )

        # Step 3: Generate an answer using Groq
        answer = self.llm_service.generate_answer(
            question=(
                f"Answer this question using the web search results: "
                f"{state['question']}\n\n"
                "Use the search results as supporting information. "
                "Do not invent facts. Include relevant source URLs."
            ),
            context=context
        )

        return {
            "answer": answer,
            "search_results": search_results
        }

    def index_documents(
        self,
        chunks: list
    ) -> None:
        """Index document chunks for BM25 retrieval."""

        self.rag_pipeline.index_documents(chunks)

    def run(
        self,
        question: str,
        document_id: str | None = None
    ) -> AssistantState:
        """Execute the LangGraph workflow."""

        initial_state: AssistantState = {
            "question": question,
            "document_id": document_id
        }

        return self.graph.invoke(initial_state)

    def close(self) -> None:
        """Close database connections."""

        self.rag_pipeline.close()
