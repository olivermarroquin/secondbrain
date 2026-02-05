import pytest
from playwright.sync_api import Page
from pages.challenging_dom_page import ChallengingDOMPage
from utils.logger import logger

@pytest.mark.regression
@pytest.mark.challenging_dom
class TestChallengingDOMRegression:
    
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

    def test_get_all_table_data(self):
        logger.step("Extracting table data")
        all_data = self.dom_page.get_all_table_data()
        assert len(all_data) == 10, f"Expected 10 rows of data, got {len(all_data)}"
        for i, row in enumerate(all_data):
            assert len(row) == 7, f"Row {i} should have 7 columns, has {len(row)}"
        logger.info(f"Extracted {len(all_data)} rows with 7 columns each")
    
    def test_edit_links_are_present(self):
        logger.step("Checking edit links")
        edit_count = self.dom_page.get_edit_links_count()
        row_count = self.dom_page.get_table_row_count()
        assert edit_count == row_count, \
            f"Each row should have an edit link. Expected {row_count}, found {edit_count}"
        logger.info(f"Found {edit_count} edit links")
    
    def test_delete_links_are_present(self):
        logger.step("Checking delete links")
        delete_count = self.dom_page.get_delete_links_count()
        row_count = self.dom_page.get_table_row_count()
        assert delete_count == row_count, \
            f"Each row should have a delete link. Expected {row_count}, found {delete_count}"
        logger.info(f"Found {delete_count} delete links")
