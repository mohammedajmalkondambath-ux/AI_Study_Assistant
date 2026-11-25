
from ddgs import DDGS
from ddgs.exceptions import DDGSException


class WebSearchService:
    """Searches the internet for current information."""

    def search(
        self,
        query: str,
        max_results: int = 5
    ) -> list[dict]:
        """Search the web with a retry if the first attempt fails."""

        if not query or not query.strip():
            raise ValueError("Search query cannot be empty.")

        if max_results < 1:
            raise ValueError("max_results must be at least 1.")

        # Try the search twice
        for attempt in range(2):

            try:
                print(f"Web search attempt: {attempt + 1}")

                with DDGS(timeout=30) as ddgs:

                    search_results = ddgs.text(
                        query,
                        max_results=max_results,
                        backend="auto"
                    )

                    results = []

                    for item in search_results:
                        results.append({
                            "title": item.get("title", ""),
                            "url": item.get("href", ""),
                            "snippet": item.get("body", "")
                        })

                    if results:
                        print(
                            f"Found {len(results)} web search results."
                        )
                        return results

            except DDGSException as error:
                print(f"Search attempt failed: {error}")

        print("Web search failed after 2 attempts.")
        return []
