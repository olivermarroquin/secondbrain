import pytest
from playwright.sync_api import Page
from pages.dynamic_loading_page import DynamicLoadingPage
from utils.logger import logger

@pytest.mark.smoke
@pytest.mark.dynamic_loading
class TestDynamicLoadingSmoke:
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page, request):
        test_name = request.node.name
        logger.info(f"{'='*60}")
        logger.info(f"Starting: {test_name}")
        logger.info(f"{'='*60}")
        self.dl_page = DynamicLoadingPage(page)
        self.dl_page.load()
        yield
        logger.info(f"Completed: {test_name}\n")

    def test_hidden_element_becomes_visible_after_loading(self):
        logger.step("Testing dynamic loading")
        self.dl_page.click_start_button()
        self.dl_page.wait_for_finish_message(timeout=10000)
        assert self.dl_page.is_finish_message_visible(), \
            "Finish message should be visible after loading completes"
        finish_text = self.dl_page.get_finish_message_text()
        assert finish_text == "Hello World!", \
            f"Expected finish message to be 'Hello World!', got '{finish_text}'"
        assert not self.dl_page.is_loading_indicator_visible(), \
            "Loading indicator should not be visible after loading completes"
        logger.info("Dynamic loading completed successfully")
