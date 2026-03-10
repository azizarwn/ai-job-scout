from agents import function_tool
from tavily.tavily import TavilyClient

from app.core.settings import settings

tavily_client = TavilyClient(api_key=settings.TAVILY_API_KEY)


@function_tool
def search_web(message: str):
    """
    Search for job listings on the web using Tavily.
    Use this to find real, current job postings for a given role and location.
    """
    query = f"{message} 2026 hiring"
    results = tavily_client.search(
        query=query,
        search_depth="advanced",
        max_results=5,
        include_answer=True,
    )
    return results


@function_tool
def analyze_job_market(job_description: str) -> str:
    """
    Research salary ranges, demand trends, and market insights for a given role and location.

    Args:
        role: The job role to analyze (e.g. 'Frontend Developer', 'React Developer')
        location: The city or country to analyze (e.g. 'Singapore', 'Dubai')
    """
    client = TavilyClient(api_key=settings.TAVILY_API_KEY)
    query = f"{job_description} salary range market demand 2025 2026"

    results = client.search(
        query=query,
        search_depth="advanced",
        max_results=5,
        include_answer=True,
    )

    output = f"## Market Analysis: {job_description}\n\n"

    if results.get("answer"):
        output += f"**Market Summary:** {results['answer']}\n\n"

    output += "### Detailed Insights:\n"
    for i, r in enumerate(results.get("results", []), 1):
        output += f"\n**Source {i}: {r.get('title', 'N/A')}**\n"
        output += f"   {r.get('content', '')[:400]}...\n"

    return output
