from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from playwright.async_api import async_playwright
import os
import logging

logger = logging.getLogger(__name__)

async def playwright_tools():
    """
    Initialize Playwright tools with appropriate browser settings.
    
    Returns:
        tuple: (tools, browser, playwright) - The browser tools, browser instance, and playwright instance.
    """
    try:
        # Get headless mode from environment or default to True for reliability
        headless = os.getenv("PLAYWRIGHT_HEADLESS", "true").lower() == "true"
        
        playwright = await async_playwright().start()
        
        # Try to launch browser
        try:
            browser = await playwright.chromium.launch(headless=headless)
            logger.info(f"Browser launched successfully in {'headless' if headless else 'non-headless'} mode")
        except Exception as e:
            # If non-headless fails, try headless as fallback
            if not headless:
                logger.warning(f"Failed to launch browser in non-headless mode: {e}")
                logger.info("Trying headless mode as fallback")
                browser = await playwright.chromium.launch(headless=True)
                logger.info("Browser launched successfully in headless mode (fallback)")
            else:
                # If headless also fails, re-raise the exception
                raise
        
        toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=browser)
        return toolkit.get_tools(), browser, playwright
    except Exception as e:
        logger.error(f"Failed to initialize Playwright tools: {e}")
        # Return empty tools list if browser initialization fails
        return [], None, None