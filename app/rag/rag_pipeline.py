

from app.rag.context_builder import ContextBuilder
from app.rag.reranking.reranker_service import RerankerService
from app.rag.retrieval.bm25_retriever import BM25Retriever
from app.rag.retrieval.hybrid_retriever import HybridRetriever
from app.rag.retrieval.semantic_retriever import SemanticRetriever
from app.services.llm_service import LLMService


class RAGPipeline:
    """Connects retrieval, reranking, context building and LLM."""

    def __init__(self):
        self.bm25_retriever = BM25Retriever()
        self.semantic_retriever = SemanticRetriever()
        self.hybrid_retriever = HybridRetriever()
        self.reranker = RerankerService()
        self.context_builder = ContextBuilder()
        self.llm_service = LLMService()

    
    def index_documents(self, chunks: list) -> None:
        """Load document chunks into the BM25 search index."""

        self.bm25_retriever.index_documents(chunks)

        print("Documents indexed successfully for BM25.")


    def answer_question(
        self,
        question: str,
        document_id: str | None = None,
        top_k: int = 5
    ) -> dict:
        """Generate an answer using uploaded document content."""

        if not question.strip():
            raise ValueError("Question cannot be empty.")

        # Step 1: Retrieve keyword-based results
        bm25_results = self.bm25_retriever.search(
            question,
            top_k=10,
            document_id=document_id
        )

        # Step 2: Retrieve semantic results
        semantic_results = self.semantic_retriever.search(
            question,
            top_k=10,
            document_id=document_id
        )

        # Step 3: Combine retrieval results
        hybrid_results = self.hybrid_retriever.fuse_results(
            bm25_results,
            semantic_results,
            top_k=10
        )

        if not hybrid_results:
            return {
                "answer": "No relevant information was found in the uploaded documents.",
                "citations": []
            }

        # Step 4: Rerank results
        reranked_results = self.reranker.rerank(
            question,
            hybrid_results,
            top_k=top_k
        )

        # Step 5: Build context and citations
        context_data = self.context_builder.build_context(
            reranked_results,
            max_chunks=top_k
        )

        # Step 6: Generate final answer
        answer = self.llm_service.generate_answer(
            question,
            context_data["context"]
        )

        return {
            "answer": answer,
            "citations": context_data["citations"]
        }

    def close(self) -> None:
        """Close database connections."""

        self.semantic_retriever.close()
