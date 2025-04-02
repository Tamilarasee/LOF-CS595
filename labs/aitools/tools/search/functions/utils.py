import requests
from agents import function_tool


@function_tool
def search_duckduckgo(query: str) -> str:
    """
    TODO:
    Instructions for implementing search_duckduckgo function:
    1. Make a GET request to DuckDuckGo's API endpoint
    2. Configure request parameters:
       - q: Search query string
       - format: Request JSON response
       - no_html: Exclude HTML from results
       - skip_disambig: Skip disambiguation pages
    3. Process the API response:
       - Extract Abstract for main summary
       - Get up to 3 RelatedTopics for additional context
    4. Format the results:
       - Start with Abstract as "Summary" if available
       - Add bullet points for RelatedTopics
       - Return "No relevant information" if no results found
    5. Handle errors gracefully with error message

    Search the web using DuckDuckGo for information related to the query.

    Args:
        query: The search query string

    Returns:
        Formatted string with search results
    """
    url = "https://api.duckduckgo.com/"