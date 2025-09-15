from langchain.agents import Tool
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from config.settings import SERPER_API_KEY

# Initialize search utilities
serper = GoogleSerperAPIWrapper(serper_api_key=SERPER_API_KEY)
wikipedia = WikipediaAPIWrapper()

def get_search_tool():
    """Get a tool for web search using Google Serper API"""
    return Tool(
        name="search",
        func=serper.run,
        description="Use this tool when you want to get the results of an online web search"
    )

def get_wikipedia_tool():
    """Get a tool for searching Wikipedia"""
    wiki_tool = WikipediaQueryRun(api_wrapper=wikipedia)
    return wiki_tool

def get_search_tools():
    """Get all search-related tools"""
    return [get_search_tool(), get_wikipedia_tool()]
