from playwright.sync_api import Page, Locator
from typing import Dict, List
import time

class SafeActions:
    @staticmethod
    def safe_click(locator: Locator, timeout: int = 30000, retries: int = 3):
        for attempt in range(retries):
            try:
                locator.wait_for(state="visible", timeout=timeout)
                locator.click(timeout=timeout)
                return
            except Exception as e:
                if attempt == retries - 1:
                    raise e
                time.sleep(0.5)
    
    @staticmethod
    def safe_get_text(locator: Locator, timeout: int = 30000) -> str:
        locator.wait_for(state="visible", timeout=timeout)
        text = locator.text_content()
        return text.strip() if text else ""
    

class TableHelper:
    @staticmethod
    def extract_table_data(page: Page, table_selector: str, 
                          header_selector: str = "thead tr th",
                          row_selector: str = "tbody tr") -> List[Dict[str, str]]:
        headers = []
        header_elements = page.locator(f"{table_selector} {header_selector}").all()
        for header in header_elements:
            headers.append(header.text_content().strip())

        all_data = []
        rows = page.locator(f"{table_selector} {row_selector}").all()
        
        for row in rows:
            cells = row.locator("td").all()
            row_data = {}
            for i, cell in enumerate(cells):
                if i < len(headers):
                    row_data[headers[i]] = cell.text_content().strip()
            all_data.append(row_data)
        
        return all_data
