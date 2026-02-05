from playwright.sync_api import Page
from typing import Optional
from config.config import config
from utils.logger import logger
from utils import SafeActions

class BasePage:
    
    def __init__(self, page: Page):
        self.page = page
        self.timeout = config.DEFAULT_TIMEOUT
    
    def navigate_to(self, url: str) -> None:
        logger.info(f"Navigating to: {url}")
        self.page.goto(url, wait_until="domcontentloaded")
    
    def click(self, selector: str) -> None:
        logger.debug(f"Clicking: {selector}")
        locator = self.page.locator(selector)
        SafeActions.safe_click(locator, self.timeout)
    
    def get_text(self, selector: str) -> str:
        locator = self.page.locator(selector)
        return SafeActions.safe_get_text(locator, self.timeout)
    
    def is_visible(self, selector: str) -> bool:
        return self.page.locator(selector).is_visible()
    
    def wait_for_selector(self, selector: str, state: str = "visible") -> None:
        logger.debug(f"Waiting for: {selector}")
        self.page.wait_for_selector(selector, state=state, timeout=self.timeout)
    
    def get_element_count(self, selector: str) -> int:
        return self.page.locator(selector).count()
    
    def get_attribute(self, selector: str, attribute: str) -> Optional[str]:
        return self.page.locator(selector).get_attribute(attribute)
