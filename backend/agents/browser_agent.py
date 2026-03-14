"""
MINDFORGE — Browser Agent Tools
LangChain tool definitions wrapping the Selenium browser service.
"""
import logging
from typing import List

from langchain_core.tools import tool

from services.browser_service import BrowserService

logger = logging.getLogger(__name__)
_browser = BrowserService()


@tool
def navigate_to_url(url: str) -> str:
    """Navigate the browser to the given URL. Returns page title on success."""
    try:
        _browser.navigate(url)
        return f"Navigated to: {url} | Title: {_browser.get_title()}"
    except Exception as e:
        return f"ERROR navigating to {url}: {e}"


@tool
def get_page_text() -> str:
    """Extract and return all visible text content from the current page."""
    try:
        return _browser.get_page_text()
    except Exception as e:
        return f"ERROR extracting page text: {e}"


@tool
def click_element(selector: str) -> str:
    """Click an element on the page using a CSS selector or XPath."""
    try:
        _browser.click(selector)
        return f"Clicked element: {selector}"
    except Exception as e:
        return f"ERROR clicking {selector}: {e}"


@tool
def fill_input(selector: str, value: str) -> str:
    """Fill a text input field identified by a CSS selector with the given value."""
    try:
        _browser.fill(selector, value)
        return f"Filled '{selector}' with value."
    except Exception as e:
        return f"ERROR filling {selector}: {e}"


@tool
def submit_form(selector: str) -> str:
    """Submit a form by clicking the submit button identified by a CSS selector."""
    try:
        _browser.click(selector)
        return f"Submitted form via: {selector}"
    except Exception as e:
        return f"ERROR submitting form: {e}"


@tool
def take_screenshot(filename: str = "screenshot.png") -> str:
    """Take a screenshot of the current browser state and save it."""
    try:
        path = _browser.screenshot(filename)
        return f"Screenshot saved to: {path}"
    except Exception as e:
        return f"ERROR taking screenshot: {e}"


@tool
def get_current_url() -> str:
    """Return the current URL of the browser."""
    try:
        return _browser.get_current_url()
    except Exception as e:
        return f"ERROR getting URL: {e}"


@tool  
def wait_for_element(selector: str, timeout: int = 10) -> str:
    """Wait for an element to appear on the page. Returns status."""
    try:
        _browser.wait_for(selector, timeout)
        return f"Element '{selector}' is now visible."
    except Exception as e:
        return f"TIMEOUT waiting for '{selector}': {e}"


def get_browser_tools() -> List:
    """Return all browser tools for the orchestrator."""
    return [
        navigate_to_url,
        get_page_text,
        click_element,
        fill_input,
        submit_form,
        take_screenshot,
        get_current_url,
        wait_for_element,
    ]
