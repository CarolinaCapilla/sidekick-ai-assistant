from sidekick.tools.browser import playwright_tools
from sidekick.tools.file_tools import get_file_tools
from sidekick.tools.notifications import get_notification_tool
from sidekick.tools.search_tools import get_search_tools
from sidekick.tools.python_tools import get_python_repl_tool

async def get_all_tools():
    """
    Get all tools available in the sidekick system.
    
    Returns:
        list: A list of all tools, including browser tools, file tools, 
        notification tools, search tools, and Python REPL.
    """
    # Get browser tools first (they require async initialization)
    browser_tools, browser, playwright = await playwright_tools()
    
    # Get all other tools
    file_tools = get_file_tools()
    notification_tool = get_notification_tool()
    search_tools = get_search_tools()
    python_repl = get_python_repl_tool()
    
    # Combine all tools
    all_tools = browser_tools + file_tools + [notification_tool] + search_tools + [python_repl]
    
    return all_tools, browser, playwright
