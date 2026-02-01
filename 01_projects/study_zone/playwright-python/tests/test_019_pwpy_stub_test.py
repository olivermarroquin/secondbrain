from playwright.sync_api import sync_playwright

def test_todo():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        # TODO
        browser.close()
