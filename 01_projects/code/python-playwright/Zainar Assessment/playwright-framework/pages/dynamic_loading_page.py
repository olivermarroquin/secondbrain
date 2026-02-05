from pages.base_page import BasePage
from playwright.sync_api import Page
from config.config import config
from utils.logger import logger

class DynamicLoadingPage(BasePage):
    
    START_BUTTON = "#start button"
    LOADING_INDICATOR = "#loading"
    FINISH_MESSAGE = "#finish h4"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def load(self) -> None:
        url = config.get_url("dynamic_loading/1")
        logger.step("Loading Dynamic Loading page")
        self.navigate_to(url)
    
    def click_start_button(self) -> None:
        logger.step("Clicking start button")
        self.click(self.START_BUTTON)
    
    def wait_for_finish_message(self, timeout: int = 10000) -> None:
        logger.debug(f"Waiting for finish message (timeout: {timeout}ms)")
        self.page.wait_for_selector(self.FINISH_MESSAGE, state="visible", timeout=timeout)
    
    def is_finish_message_visible(self) -> bool:
        return self.is_visible(self.FINISH_MESSAGE)
    
    def get_finish_message_text(self) -> str:
        logger.debug("Getting finish message text")
        return self.get_text(self.FINISH_MESSAGE)
    
    def is_loading_indicator_visible(self) -> bool:
        return self.is_visible(self.LOADING_INDICATOR)
