import pytest
from playwright.sync_api import Page
from pages.shifting_content_page import ShiftingContentPage
from utils.logger import logger

@pytest.mark.regression
@pytest.mark.shifting_content
class TestShiftingContentRegression:
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page, request):
        test_name = request.node.name
        logger.info(f"{'='*60}")
        logger.info(f"Starting: {test_name}")
        logger.info(f"{'='*60}")
        self.page = page
        self.sc = ShiftingContentPage(page)
        yield
        logger.info(f"Completed: {test_name}\n")

    def test_gallery_position_changes_with_pixel_shift(self):
        logger.step("Testing gallery position changes")
        self.sc.load_menu(pixel_shift=0)
        assert self.sc.verify_menu_loaded(timeout_ms=5000), "Menu did not load (pixel_shift=0)"
        no_shift_box = self.sc.get_gallery_box()
        assert no_shift_box is not None, "Gallery should have position coordinates"
        logger.info(f"Gallery position pixel_shift=0: X={no_shift_box['x']}, Y={no_shift_box['y']}")
        
        self.sc.load_menu(pixel_shift=100)
        assert self.sc.verify_menu_loaded(timeout_ms=5000), "Menu did not load (pixel_shift=100)"
        shift_box = self.sc.get_gallery_box()
        assert shift_box is not None, "Gallery should have position coordinates"
        logger.info(f"Gallery position pixel_shift=100: X={shift_box['x']}, Y={shift_box['y']}")
        
        x_diff = abs(shift_box["x"] - no_shift_box["x"])
        logger.info(f"Position difference: X shift={x_diff}px")
        assert no_shift_box["x"] != shift_box["x"], \
            f"Gallery X should change with pixel_shift"
        assert x_diff >= 10, f"X position difference should be at least 10px, got {x_diff}px"
        logger.info("Position changes validated")
    
    def test_random_mode_causes_position_variations(self):
        logger.step("Testing random mode position variations")
        positions = []
        for i in range(5):
            self.sc.load_menu_random(pixel_shift=100)
            assert self.sc.verify_menu_loaded(timeout_ms=5000), f"Menu did not load (random run {i+1})"
            box = self.sc.get_gallery_box()
            assert box is not None, f"Gallery box missing on run {i+1}"
            positions.append(box["x"])
            logger.info(f"Run {i+1}: Gallery X={box['x']}")
        
        unique = len(set(positions))
        logger.info(f"Unique positions observed: {unique}")
        assert unique >= 2, f"Expected at least 2 unique X positions in random mode"
        
        rng = max(positions) - min(positions)
        logger.info(f"Position range: {rng}px")
        assert rng >= 10, f"Expected at least 10px range, got {rng}px"
        logger.info("Random mode variations validated")
