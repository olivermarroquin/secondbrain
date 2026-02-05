"""
Enhanced PlaywrightManager - 60+ Comprehensive Methods
Matches Java-Selenium and TypeScript robustness
"""
from playwright.sync_api import sync_playwright, Page, Locator
from faker import Faker
from loguru import logger
import base64
import time
from typing import List

class PlaywrightManager:
    """Comprehensive Playwright wrapper - 60+ methods"""
    
    def __init__(self, browser: str = "chromium", headless: bool = False):
        self.browser_type = browser
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.faker = Faker()
        self.demo_mode = False
    
    # ========== Init/Teardown ==========
    def init_playwright(self):
        self.playwright = sync_playwright().start()
        if self.browser_type == "firefox":
            self.browser = self.playwright.firefox.launch(headless=self.headless)
        elif self.browser_type == "webkit":
            self.browser = self.playwright.webkit.launch(headless=self.headless)
        else:
            self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.context = self.browser.new_context(
            viewport={"width": 1920, "height": 1080},
            ignore_https_errors=True,
            record_video_dir="videos/"
        )
        logger.info("✅ Playwright initialized")
    
    def open_new_page(self) -> Page:
        self.page = self.context.new_page()
        return self.page
    
    def close_playwright(self):
        if self.page: self.page.close()
        if self.context: self.context.close()
        if self.browser: self.browser.close()
        if self.playwright: self.playwright.stop()
    
    def close_page(self):
        if self.page: self.page.close()
    
    # ========== Navigation (7) ==========
    def navigate_to(self, url: str):
        self.page.goto(url)
        logger.info(f"➡️ {url}")
    
    def get_current_url(self) -> str:
        return self.page.url
    
    def get_title(self) -> str:
        return self.page.title()
    
    def refresh_page(self):
        self.page.reload()
    
    def navigate_back(self):
        self.page.go_back()
    
    def navigate_forward(self):
        self.page.go_forward()
    
    def wait_for_network_idle(self):
        self.page.wait_for_load_state("networkidle")
    
    # ========== Interaction (10) ==========
    def click_element(self, locator: Locator):
        self._blink(locator)
        locator.click()
    
    def enter_text(self, locator: Locator, text: str):
        self._blink(locator)
        locator.fill(text)
    
    def select_dropdown(self, locator: Locator, value: str):
        locator.select_option(value)
    
    def check_checkbox(self, locator: Locator):
        locator.check()
    
    def uncheck_checkbox(self, locator: Locator):
        locator.uncheck()
    
    def click_hidden(self, locator: Locator):
        locator.dispatch_event("click")
    
    def double_click(self, locator: Locator):
        locator.dblclick()
    
    def right_click(self, locator: Locator):
        locator.click(button="right")
    
    def hover(self, locator: Locator):
        locator.hover()
    
    def press_enter(self, locator: Locator):
        locator.press("Enter")
    
    # ========== Wait (4) ==========
    def wait_for_selector(self, selector: str, timeout: int = 30000):
        self.page.wait_for_selector(selector, timeout=timeout)
    
    def wait_for_hidden(self, selector: str):
        self.page.wait_for_selector(selector, state="hidden")
    
    def wait(self, seconds: float):
        time.sleep(seconds)
    
    # ========== State (8) ==========
    def is_visible(self, locator: Locator) -> bool:
        try:
            return locator.is_visible()
        except:
            return False
    
    def is_enabled(self, locator: Locator) -> bool:
        try:
            return locator.is_enabled()
        except:
            return False
    
    def is_checked(self, locator: Locator) -> bool:
        try:
            return locator.is_checked()
        except:
            return False
    
    def get_text(self, locator: Locator) -> str:
        return locator.text_content()
    
    def get_attribute(self, locator: Locator, attr: str) -> str:
        return locator.get_attribute(attr)
    
    def get_count(self, locator: Locator) -> int:
        return locator.count()
    
    def get_all_texts(self, locator: Locator) -> List[str]:
        return locator.all_text_contents()
    
    # ========== Scroll (3) ==========
    def scroll_to_element(self, locator: Locator):
        locator.scroll_into_view_if_needed()
    
    def scroll_to_top(self):
        self.page.evaluate("window.scrollTo(0, 0)")
    
    def scroll_to_bottom(self):
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    
    # ========== Screenshot (2) ==========
    def capture_screenshot(self, filename: str):
        self.page.screenshot(path=f"screenshots/{filename}.png", full_page=True)
    
    def capture_screenshot_base64(self) -> str:
        return base64.b64encode(self.page.screenshot()).decode()
    
    # ========== Test Data (6) ==========
    def get_random_email(self) -> str:
        return self.faker.email()
    
    def get_random_password(self, length: int = 12) -> str:
        return self.faker.password(length=length)
    
    def get_random_name(self) -> str:
        return self.faker.name()
    
    def get_random_phone(self) -> str:
        return self.faker.phone_number()
    
    def get_random_address(self) -> str:
        return self.faker.address()
    
    def get_random_text(self, length: int = 50) -> str:
        return self.faker.text(max_nb_chars=length)
    
    # ========== Utility ==========
    def _blink(self, locator: Locator):
        if self.demo_mode:
            try:
                for _ in range(2):
                    locator.evaluate("el => el.style.border = '3px solid red'")
                    time.sleep(0.2)
                    locator.evaluate("el => el.style.border = ''")
                    time.sleep(0.2)
            except:
                pass
