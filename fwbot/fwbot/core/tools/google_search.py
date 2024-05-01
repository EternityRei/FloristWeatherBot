from langchain.tools import tool
from langchain_community.utilities import GoogleSearchAPIWrapper


@tool
def search(prompt: str):
    """Used to collect information all over the web based on provided queries"""

    google_search = GoogleSearchAPIWrapper()
    results = google_search.results(
        query=prompt,
        num_results=10
    )

    return results
