"""
PortalHomePage: Shared entry point for CBAPS and DAWMS applications
User selects which application to access from portal
"""

import logging
from playwright.sync_api import Page, Locator
from dawms.library.playwright_manager import PlaywrightManager

logger = logging.getLogger(__name__)


class PortalHomePage:
    """
    PortalHomePage represents the portal landing page.
    This is the Python equivalent of the Java PortalHomePage.
    """
    
    def __init__(self, page: Page, pwm: PlaywrightManager):
        """
        Initialize PortalHomePage
        
        Args:
            page: Playwright Page object
            pwm: PlaywrightManager instance
        """
        self.page = page
        self.pwm = pwm
        
        # Locators
        self.cbaps_link: Locator = page.locator("a:has-text('CBAPS')")
        self.dawms_link: Locator = page.locator("a:has-text('DAWMS')")
        
        # Stability anchor: wait for portal to load
        pwm.wait_visible("text=Application Portal")
        logger.info("Portal Home Page loaded successfully.")
    
    def navigate_to_portal(self, portal_url: str) -> 'PortalHomePage':
        """
        Navigate to portal homepage
        
        Args:
            portal_url: URL of the portal
            
        Returns:
            self for method chaining
        """
        self.page.goto(portal_url)
        self.pwm.wait_visible("text=Application Portal")
        logger.info(f"Navigated to Portal: {portal_url}")
        return self
    
    def open_dawms(self) -> 'DAWMSDashboardPage':
        """
        Open DAWMS application from portal
        
        Returns:
            DAWMSDashboardPage instance
        """
        from dawms.pages.dawms_dashboard_page import DAWMSDashboardPage
        
        self.pwm.click(self.dawms_link)
        logger.info("Clicked DAWMS link from portal.")
        return DAWMSDashboardPage(self.page, self.pwm)
    
    def get_title(self) -> str:
        """Get portal page title"""
        return self.page.title()
