"""Base Test Class"""
import pytest
from loguru import logger

class BaseTest:
    @pytest.fixture(autouse=True)
    def setup(self, pw, page):
        self.pw = pw
        self.page = page
        logger.info("🚀 Test started")
        yield
        logger.info("✅ Test completed")
    
    def log_step(self, msg: str):
        logger.info(f"📋 {msg}")
    
    def log_pass(self, msg: str):
        logger.success(f"✅ {msg}")
