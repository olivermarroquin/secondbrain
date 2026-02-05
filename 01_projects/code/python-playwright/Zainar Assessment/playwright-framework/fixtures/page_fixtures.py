"""Reusable page object fixtures"""
import pytest
from pages.challenging_dom_page import ChallengingDOMPage
from pages.dynamic_loading_page import DynamicLoadingPage
from pages.shifting_content_page import ShiftingContentPage

@pytest.fixture
def challenging_dom_page(page):
    dom_page = ChallengingDOMPage(page)
    dom_page.load()
    return dom_page

@pytest.fixture
def dynamic_loading_page(page):
    dl_page = DynamicLoadingPage(page)
    dl_page.load()
    return dl_page

@pytest.fixture
def shifting_content_page(page):
    return ShiftingContentPage(page)
