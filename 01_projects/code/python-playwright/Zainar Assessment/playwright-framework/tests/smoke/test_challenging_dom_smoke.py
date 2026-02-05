import pytest
from playwright.sync_api import Page
from pages.challenging_dom_page import ChallengingDOMPage
from utils.logger import logger

@pytest.mark.smoke
@pytest.mark.challenging_dom
class TestChallengingDOMSmoke:
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page, request):
        test_name = request.node.name
        logger.info(f"{'='*60}")
        logger.info(f"Starting: {test_name}")
        logger.info(f"{'='*60}")
        self.dom_page = ChallengingDOMPage(page)
        self.dom_page.load()
        yield
        logger.info(f"Completed: {test_name}\n")

    def test_all_three_buttons_are_visible(self):
        logger.step("Checking button visibility")
        blue_text = self.dom_page.get_blue_button_text()
        red_text = self.dom_page.get_red_button_text()
        green_text = self.dom_page.get_green_button_text()
        assert blue_text, "Blue button should be visible"
        assert red_text, "Red button should be visible"
        assert green_text, "Green button should be visible"
        logger.info("All buttons are visible")
    
    def test_canvas_has_correct_dimensions(self):
        logger.step("Checking canvas dimensions")
        width = self.dom_page.get_canvas_width()
        height = self.dom_page.get_canvas_height()
        assert width is not None, "Canvas should have a width attribute"
        assert height is not None, "Canvas should have a height attribute"
        assert int(width) > 0, "Canvas width should be greater than 0"
        assert int(height) > 0, "Canvas height should be greater than 0"
        logger.info(f"Canvas dimensions: {width}x{height}")
