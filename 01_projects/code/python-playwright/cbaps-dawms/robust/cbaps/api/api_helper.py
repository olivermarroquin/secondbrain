"""CBAPS API Helper using requests"""
import requests
from loguru import logger
from shared.config import CBAPS_API

class APIHelper:
    @staticmethod
    def get(endpoint: str):
        url = f"{CBAPS_API}{endpoint}"
        logger.info(f"📡 GET: {url}")
        return requests.get(url)
    
    @staticmethod
    def post(endpoint: str, data: dict):
        url = f"{CBAPS_API}{endpoint}"
        logger.info(f"📡 POST: {url}")
        return requests.post(url, json=data)
    
    @staticmethod
    def validate_status(response, expected: int):
        assert response.status_code == expected
        logger.info(f"✅ Status: {expected}")
