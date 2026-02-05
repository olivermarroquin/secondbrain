"""Custom assertion helpers for better test validation (for class and page)"""
from typing import Any, List
from playwright.sync_api import Page, expect


class SoftAssert:
    
    def __init__(self):
        self.errors: List[str] = []
    
    def assert_equal(self, actual: Any, expected: Any, message: str = ""):
        if actual != expected:
            error = f"{message}: Expected '{expected}', got '{actual}'"
            self.errors.append(error)
    
    def assert_true(self, condition: bool, message: str = ""):
        if not condition:
            self.errors.append(f"{message}: Condition was False")
    
    def assert_in(self, item: Any, collection: Any, message: str = ""):
        if item not in collection:
            self.errors.append(f"{message}: '{item}' not in '{collection}'")
    
    def assert_all(self):
        if self.errors:
            error_msg = "\n".join([f"  - {e}" for e in self.errors])
            raise AssertionError(f"Multiple assertion failures:\n{error_msg}")


class PageAssertions:
    
    def __init__(self, page: Page):
        self.page = page
    
    def assert_url_contains(self, text: str, timeout: int = 5000):
        expect(self.page).to_have_url(text, timeout=timeout)
    
    def assert_title_is(self, title: str, timeout: int = 5000):
        expect(self.page).to_have_title(title, timeout=timeout)
    
    def assert_element_visible(self, selector: str, timeout: int = 5000):
        expect(self.page.locator(selector)).to_be_visible(timeout=timeout)
    
    def assert_element_has_text(self, selector: str, text: str, timeout: int = 5000):
        expect(self.page.locator(selector)).to_contain_text(text, timeout=timeout)
