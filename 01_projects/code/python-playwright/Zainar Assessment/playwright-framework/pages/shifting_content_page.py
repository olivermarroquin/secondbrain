from pages.base_page import BasePage
from playwright.sync_api import Page, expect
from typing import Dict, Optional
from config.config import config
from utils.logger import logger

class ShiftingContentPage(BasePage):
    
    MENU_LINKS = ".example ul li a"
    PORTFOLIO_LINK = ".example a[href='/portfolio/']"
    GALLERY_LINK = ".example a[href='/gallery/']"
    CONTENT_IMAGE = ".example img"
    
    def __init__(self, page: Page):
        super().__init__(page)
        
    def load_menu(self, pixel_shift: int = 100) -> None:
        url = f"{config.BASE_URL}/shifting_content/menu?pixel_shift={pixel_shift}"
        logger.step(f"Loading menu with pixel_shift={pixel_shift}")
        self.navigate_to(url)
    
    def load_menu_random(self, pixel_shift: int = 100) -> None:
        url = f"{config.BASE_URL}/shifting_content/menu?mode=random&pixel_shift={pixel_shift}"
        logger.step(f"Loading menu in random mode with pixel_shift={pixel_shift}")
        self.navigate_to(url)
    
    def reload(self) -> None:
        logger.debug("Reloading page")
        self.page.reload(wait_until="domcontentloaded")
    
    def wait_until_menu_ready(self, timeout_ms: int = 30_000) -> None:
        logger.debug("Waiting for menu to be ready")
        links = self.page.locator(self.MENU_LINKS)
        expect(links).to_have_count(5, timeout=timeout_ms)
        expect(links.first).to_be_visible(timeout=timeout_ms)
    
    def verify_menu_loaded(self, timeout_ms: int = 30_000) -> bool:
        try:
            self.wait_until_menu_ready(timeout_ms=timeout_ms)
            return True
        except Exception:
            return False
    
    def get_gallery_box(self) -> Optional[Dict[str, float]]:
        logger.debug("Getting gallery bounding box")
        return self.page.locator(self.GALLERY_LINK).bounding_box()
    
    def get_image_position(self) -> Dict[str, float]:
        box = self.page.locator(self.CONTENT_IMAGE).bounding_box()
        if box:
            return {"x": box["x"], "y": box["y"]}
        return {"x": 0, "y": 0}
