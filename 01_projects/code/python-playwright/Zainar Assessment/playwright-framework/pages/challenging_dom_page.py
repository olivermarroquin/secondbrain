from pages.base_page import BasePage
from playwright.sync_api import Page
from typing import List, Dict
from config.config import config
from utils.logger import logger
from utils import TableHelper

class ChallengingDOMPage(BasePage):
    
    BLUE_BUTTON = "a.button"
    RED_BUTTON = "a.button.alert"
    GREEN_BUTTON = "a.button.success"
    CANVAS = "#canvas"
    DATA_TABLE = "table"
    TABLE_HEADERS = "table thead tr th"
    TABLE_ROWS = "table tbody tr"
    TABLE_CELLS = "table tbody tr td"
    EDIT_LINKS = "table tbody tr td a[href*='edit']"
    DELETE_LINKS = "table tbody tr td a[href*='delete']"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def load(self) -> None:
        url = config.get_url("challenging_dom")
        logger.step("Loading Challenging DOM page")
        self.navigate_to(url)
        
    def get_blue_button_text(self) -> str:
        logger.debug("Getting blue button text")
        return self.page.locator(self.BLUE_BUTTON).first.text_content()
    
    def get_red_button_text(self) -> str:
        logger.debug("Getting red button text")
        return self.get_text(self.RED_BUTTON)
    
    def get_green_button_text(self) -> str:
        logger.debug("Getting green button text")
        return self.get_text(self.GREEN_BUTTON)
    
    def get_canvas_width(self) -> str:
        return self.get_attribute(self.CANVAS, "width")
    
    def get_canvas_height(self) -> str:
        return self.get_attribute(self.CANVAS, "height")
    
    def is_table_visible(self) -> bool:
        return self.is_visible(self.DATA_TABLE)
    
    def get_table_headers(self) -> List[str]:
        logger.debug("Extracting table headers")
        headers = []
        header_elements = self.page.locator(self.TABLE_HEADERS).all()
        for header in header_elements:
            headers.append(header.text_content().strip())
        return headers
    
    def get_table_row_count(self) -> int:
        return self.get_element_count(self.TABLE_ROWS)
    
    def get_row_data(self, row_index: int) -> Dict[str, str]:
        headers = self.get_table_headers()
        row_selector = f"table tbody tr:nth-child({row_index + 1}) td"
        cells = self.page.locator(row_selector).all()
        row_data = {}
        for i, cell in enumerate(cells):
            if i < len(headers):
                row_data[headers[i]] = cell.text_content().strip()
        return row_data
    
    def get_all_table_data(self) -> List[Dict[str, str]]:
        logger.step("Extracting all table data")
        return TableHelper.extract_table_data(self.page, self.DATA_TABLE)
    
    def get_edit_links_count(self) -> int:
        return self.get_element_count(self.EDIT_LINKS)
    
    def get_delete_links_count(self) -> int:
        return self.get_element_count(self.DELETE_LINKS)
