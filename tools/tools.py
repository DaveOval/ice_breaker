from langchain_community.tools.tavily_search import TavilySearchResults

def get_profile_url_travily(name: str):
    """Searches for linkedin or Twitter Profile Page"""
    search = TavilySearchResults()
    res = search.run(f"{name}")
    return res