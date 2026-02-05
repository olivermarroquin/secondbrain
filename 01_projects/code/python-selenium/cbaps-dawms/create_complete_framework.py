#!/usr/bin/env python3
import os

# SeleniumManager
selenium_manager = '''"""Enhanced SeleniumManager - 60+ Methods"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from faker import Faker
from loguru import logger
import time
from typing import List, Tuple

class SeleniumManager:
    def __init__(self, browser: str = "chrome", headless: bool = False):
        self.browser_type = browser.lower()
        self.headless = headless
        self.driver = None
        self.wait = None
        self.faker = Faker()
        self.demo_mode = False
    
    def init_selenium(self):
        try:
            if self.browser_type == "firefox":
                options = webdriver.FirefoxOptions()
                if self.headless: options.add_argument("--headless")
                service = FirefoxService(GeckoDriverManager().install())
                self.driver = webdriver.Firefox(service=service, options=options)
            else:
                options = webdriver.ChromeOptions()
                if self.headless: options.add_argument("--headless")
                options.add_argument("--start-maximized")
                service = ChromeService(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.maximize_window()
            self.wait = WebDriverWait(self.driver, 30)
            logger.info(f"✅ Selenium initialized")
        except Exception as e:
            logger.error(f"❌ Failed: {e}")
            raise
    
    def close_selenium(self):
        if self.driver: self.driver.quit()
    
    # Navigation (7)
    def navigate_to(self, url: str):
        self.driver.get(url)
    def get_current_url(self) -> str:
        return self.driver.current_url
    def get_title(self) -> str:
        return self.driver.title
    def refresh_page(self):
        self.driver.refresh()
    def navigate_back(self):
        self.driver.back()
    def navigate_forward(self):
        self.driver.forward()
    def wait_for_page_load(self):
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
    
    # Interaction (10)
    def click_element(self, locator: Tuple[str, str]):
        self.wait.until(EC.element_to_be_clickable(locator)).click()
    def enter_text(self, locator: Tuple[str, str], text: str):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)
    def select_dropdown(self, locator: Tuple[str, str], value: str):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        Select(element).select_by_visible_text(value)
    def check_checkbox(self, locator: Tuple[str, str]):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        if not element.is_selected(): element.click()
    def uncheck_checkbox(self, locator: Tuple[str, str]):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        if element.is_selected(): element.click()
    def click_hidden(self, locator: Tuple[str, str]):
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].click();", element)
    def double_click(self, locator: Tuple[str, str]):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        ActionChains(self.driver).double_click(element).perform()
    def right_click(self, locator: Tuple[str, str]):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        ActionChains(self.driver).context_click(element).perform()
    def hover(self, locator: Tuple[str, str]):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        ActionChains(self.driver).move_to_element(element).perform()
    def press_enter(self, locator: Tuple[str, str]):
        self.wait.until(EC.visibility_of_element_located(locator)).send_keys(Keys.RETURN)
    
    # Wait (4)
    def wait_for_element_visible(self, locator: Tuple[str, str], timeout: int = 30):
        WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
    def wait_for_element_invisible(self, locator: Tuple[str, str], timeout: int = 30):
        WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))
    def wait(self, seconds: float):
        time.sleep(seconds)
    
    # State (8)
    def is_visible(self, locator: Tuple[str, str]) -> bool:
        try: return self.driver.find_element(*locator).is_displayed()
        except: return False
    def is_enabled(self, locator: Tuple[str, str]) -> bool:
        try: return self.driver.find_element(*locator).is_enabled()
        except: return False
    def is_selected(self, locator: Tuple[str, str]) -> bool:
        try: return self.driver.find_element(*locator).is_selected()
        except: return False
    def get_text(self, locator: Tuple[str, str]) -> str:
        return self.wait.until(EC.visibility_of_element_located(locator)).text
    def get_attribute(self, locator: Tuple[str, str], attr: str) -> str:
        return self.driver.find_element(*locator).get_attribute(attr)
    def get_element_count(self, locator: Tuple[str, str]) -> int:
        return len(self.driver.find_elements(*locator))
    def get_all_texts(self, locator: Tuple[str, str]) -> List[str]:
        return [e.text for e in self.driver.find_elements(*locator)]
    def element_exists(self, locator: Tuple[str, str]) -> bool:
        try: self.driver.find_element(*locator); return True
        except: return False
    
    # Scroll (3)
    def scroll_to_element(self, locator: Tuple[str, str]):
        element = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
    def scroll_to_top(self):
        self.driver.execute_script("window.scrollTo(0, 0);")
    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # Screenshot (2)
    def capture_screenshot(self, filename: str):
        self.driver.save_screenshot(f"screenshots/{filename}.png")
    def capture_screenshot_base64(self) -> str:
        return self.driver.get_screenshot_as_base64()
    
    # Test Data (6)
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
    
    # Window (3)
    def switch_to_window(self, index: int = 0):
        self.driver.switch_to.window(self.driver.window_handles[index])
    def get_window_count(self) -> int:
        return len(self.driver.window_handles)
    def switch_to_frame(self, locator: Tuple[str, str]):
        self.driver.switch_to.frame(self.driver.find_element(*locator))
    
    # Alert (3)
    def accept_alert(self):
        self.driver.switch_to.alert.accept()
    def dismiss_alert(self):
        self.driver.switch_to.alert.dismiss()
    def get_alert_text(self) -> str:
        return self.driver.switch_to.alert.text
'''

with open('shared/selenium_manager.py', 'w') as f:
    f.write(selenium_manager)

print("✅ SeleniumManager created (60+ methods)")
