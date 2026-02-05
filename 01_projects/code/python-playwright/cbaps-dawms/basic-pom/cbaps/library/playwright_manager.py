"""
PlaywrightManager: Wrapper around Playwright primitives for Python
Manages Playwright, Browser, BrowserContext, and Page objects
Provides common actions for CBAPS automation
"""

import logging
import base64
import time
from pathlib import Path
from typing import Optional
from playwright.sync_api import Playwright, Browser, BrowserContext, Page, Locator, sync_playwright
from faker import Faker
import string
import secrets

logger = logging.getLogger(__name__)


class PlaywrightManager:
    """
    PlaywrightManager handles browser lifecycle and provides common interaction methods.
    This is the Python equivalent of the Java PlaywrightManager.
    """
    
    def __init__(self):
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        
        # Configuration
        self.browser_type = "chromium"  # Options: "chromium", "firefox", "webkit"
        self.headless = False
        self.maximize = True
        self.ignore_https_errors = True
        self.record_video = True
        self.demo_mode = False
        
    def init_playwright(self):
        """Initialize Playwright with browser and context options"""
        try:
            self.playwright = sync_playwright().start()
            
            # Choose browser
            if self.browser_type == "firefox":
                browser_type = self.playwright.firefox
            elif self.browser_type == "webkit":
                browser_type = self.playwright.webkit
            else:
                browser_type = self.playwright.chromium
            
            # Launch options
            launch_options = {
                "headless": self.headless,
                "args": ["--start-maximized"] if self.maximize else []
            }
            
            self.browser = browser_type.launch(**launch_options)
            
            # Context options
            context_options = {
                "ignore_https_errors": self.ignore_https_errors,
                "viewport": None if self.maximize else {"width": 1280, "height": 720}
            }
            
            if self.record_video:
                context_options["record_video_dir"] = "target/videos/"
                context_options["record_video_size"] = {"width": 1280, "height": 720}
            
            self.context = self.browser.new_context(**context_options)
            
            logger.info(f"Playwright & {self.browser_type} browser initialized successfully.")
            
        except Exception as e:
            logger.error(f"Failed to initialize Playwright: {e}")
            raise
    
    def close_playwright(self):
        """Close Playwright objects"""
        try:
            time.sleep(1)
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
            logger.info("Playwright session closed.")
        except Exception as e:
            logger.error(f"Failed to close Playwright: {e}")
            raise
    
    def open_new_browser_page(self) -> Page:
        """Open new browser page"""
        try:
            self.page = self.context.new_page()
            time.sleep(2)
            logger.info(f"Opened '{self.browser_type}' browser page.")
            return self.page
        except Exception as e:
            logger.error(f"Failed to open browser page: {e}")
            raise
    
    def close_page(self):
        """Close page object"""
        try:
            time.sleep(1)
            if self.page:
                self.page.close()
            logger.info(f"Closed '{self.browser_type}' browser page.")
        except Exception as e:
            logger.error(f"Error closing page: {e}")
            raise
    
    # --- Wrapped helpers used by Page Objects ---
    
    def click(self, locator: Locator):
        """Click element (wrapper)"""
        try:
            self._blink_highlight(locator)
            locator.click()
            logger.info("Element clicked.")
        except Exception as e:
            logger.error(f"Error clicking element: {e}")
            raise
    
    def type(self, locator: Locator, text: str):
        """Enter text (wrapper)"""
        try:
            self._blink_highlight(locator)
            locator.fill(text)
            logger.info(f"Entered text: '{text}'")
        except Exception as e:
            logger.error(f"Error entering text: {e}")
            raise
    
    def wait_visible(self, selector: str):
        """Wait for element visibility"""
        try:
            self.page.wait_for_selector(selector, state="visible")
            logger.info(f"Element is now visible: '{selector}'")
            locator = self.page.locator(selector)
            self._blink_highlight(locator)
        except Exception as e:
            logger.error(f"Error waiting for element visibility: {e}")
            raise
    
    def select_dropdown(self, locator: Locator, value: str):
        """Select dropdown option"""
        try:
            self._blink_highlight(locator)
            locator.select_option(value)
            logger.info(f"Selected dropdown option: '{value}'")
        except Exception as e:
            logger.error(f"Error selecting dropdown: {e}")
            raise
    
    def file_upload(self, locator: Locator, file_path: str):
        """Upload file"""
        try:
            self._blink_highlight(locator)
            locator.set_input_files(file_path)
            logger.info(f"File uploaded: '{file_path}'")
        except Exception as e:
            logger.error(f"Error uploading file: {e}")
            raise
    
    def press_enter(self, locator: Locator):
        """Press Enter key"""
        try:
            self._blink_highlight(locator)
            locator.press("Enter")
            logger.info("Pressed Enter key")
        except Exception as e:
            logger.error(f"Error pressing Enter key: {e}")
            raise
    
    def click_hidden_element(self, locator: Locator):
        """Click hidden element using dispatch event"""
        try:
            self._blink_highlight(locator)
            locator.dispatch_event("click")
            logger.info("DispatchEvent click performed")
        except Exception as e:
            logger.error(f"Error performing dispatchEvent click: {e}")
            raise
    
    def _blink_highlight(self, locator: Locator):
        """Highlight element by blinking (for demo mode)"""
        try:
            if self.demo_mode:
                locator.scroll_into_view_if_needed()
                for _ in range(3):
                    locator.evaluate(
                        "el => { el.style.border = '3px solid red'; el.style.backgroundColor = 'yellow'; }"
                    )
                    time.sleep(0.5)
                    locator.evaluate(
                        "el => { el.style.border = ''; el.style.backgroundColor = ''; }"
                    )
                    time.sleep(0.5)
        except Exception as e:
            logger.error(f"Error in blink highlight: {e}")
    
    def capture_screenshot_full_page(self, screenshot_name: str):
        """Capture full page screenshot"""
        try:
            logger.info("Capturing full page screenshot...")
            Path("target/screenshot").mkdir(parents=True, exist_ok=True)
            screenshot_path = f"target/screenshot/{screenshot_name}.png"
            self.page.screenshot(path=screenshot_path, full_page=True)
            logger.info(f"Screenshot saved: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            logger.error(f"Failed to capture full-page screenshot: {e}")
            raise
    
    def capture_screenshot_base64(self) -> str:
        """Capture Base64 screenshot for embedding in reports"""
        try:
            screenshot_bytes = self.page.screenshot(full_page=True)
            base64_screenshot = base64.b64encode(screenshot_bytes).decode('utf-8')
            logger.debug("Base64 screenshot captured.")
            return base64_screenshot
        except Exception as e:
            logger.error(f"Error capturing Base64 screenshot: {e}")
            raise
    
    # --- Utility methods ---
    
    @staticmethod
    def sleep(seconds: float):
        """Sleep for specified seconds"""
        time.sleep(seconds)
    
    @staticmethod
    def get_random_email() -> str:
        """Generate random email"""
        faker = Faker()
        email = faker.email()
        logger.info(f"Fake email created: {email}")
        return email
    
    @staticmethod
    def get_random_password(length: int = 12, special_chars: str = "@$*") -> str:
        """Generate random password with special characters"""
        characters = string.ascii_letters + string.digits + special_chars
        # Ensure at least one special character
        password = special_chars[0]
        password += ''.join(secrets.choice(characters) for _ in range(length - 1))
        # Shuffle
        password_list = list(password)
        secrets.SystemRandom().shuffle(password_list)
        password = ''.join(password_list)
        logger.info(f"Generated password: {password}")
        return password
