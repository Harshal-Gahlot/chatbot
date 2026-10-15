import json
from ddgs import DDGS
from utils import printError

tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Searches the web for up to date information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The specific search query",
                    }
                },
                "required": ["query"],
            },
        },
    }
]


def search_web(query: str) -> str:
    """search the web and get top 3 web results"""
    try:
        with DDGS() as search:
            response = list(search.text(query, max_results=8))

        if not response:
            printError("search result:", "No web result found")
            return "No result found."

        formatted = "\n\n".join(
            [
                f"Title: {r['title']}\nBody: {r['body']}\nURL: {r['href']}"
                for r in response
            ]
        )

        printError("formatted response by search web", formatted)
        return formatted if formatted else "No result found"

    except Exception as e:
        printError("Error fetching web results:", str(e))
        return f"Search failed with error: {str(e)}"
