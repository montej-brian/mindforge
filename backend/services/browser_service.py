"""
MINDFORGE — Browser Service
Singleton Selenium WebDriver session manager. Supports both local Chrome
and remote Selenium Grid (via SELENIUM_REMOTE_URL).
"""
import logging
import os
from pathlib import Path
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from config import settings

logger = logging.getLogger(__name__)

SCREENSHOTS_DIR = Path("screenshots")
SCREENSHOTS_DIR.mkdir(exist_ok=True)


class BrowserService:
    """Manages a single Selenium WebDriver session."""

    _instance: Optional["BrowserService"] = None
    _driver: Optional[webdriver.Chrome] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def driver(self) -> webdriver.Chrome:
        if self._driver is None or not self._is_alive():
            self._driver = self._create_driver()
        return self._driver

    def _create_driver(self) -> webdriver.Chrome:
        """Instantiate and configure a Chrome WebDriver."""
        options = Options()
        if settings.browser_headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        if settings.selenium_remote_url:
            driver = webdriver.Remote(
                command_executor=settings.selenium_remote_url,
                options=options,
            )
        else:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)

        driver.set_page_load_timeout(settings.browser_timeout)
        logger.info("✅ Chrome WebDriver session started")
        return driver

    def _is_alive(self) -> bool:
        try:
            _ = self._driver.title
            return True
        except Exception:
            return False

    def navigate(self, url: str) -> None:
        self.driver.get(url)

    def get_title(self) -> str:
        return self.driver.title

    def get_current_url(self) -> str:
        return self.driver.current_url

    def get_page_text(self) -> str:
        return self.driver.find_element(By.TAG_NAME, "body").text

    def click(self, selector: str) -> None:
        wait = WebDriverWait(self.driver, settings.browser_timeout)
        el = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        el.click()

    def fill(self, selector: str, value: str) -> None:
        wait = WebDriverWait(self.driver, settings.browser_timeout)
        el = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        el.clear()
        el.send_keys(value)

    def wait_for(self, selector: str, timeout: int = 10) -> None:
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))

    def screenshot(self, filename: str = "screenshot.png") -> str:
        path = str(SCREENSHOTS_DIR / filename)
        self.driver.save_screenshot(path)
        return path

    def quit(self) -> None:
        if self._driver:
            self._driver.quit()
            self._driver = None
            logger.info("Chrome WebDriver session closed")
