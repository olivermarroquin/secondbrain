import requests
from loguru import logger
from shared.config import DAWMS_API

class APIHelper:
    @staticmethod
    def get(endpoint: str):
        url = f"{DAWMS_API}{endpoint}"
        logger.info(f"📡 GET: {url}")
        return requests.get(url)
    
    @staticmethod
    def post(endpoint: str, data: dict):
        url = f"{DAWMS_API}{endpoint}"
        logger.info(f"📡 POST: {url}")
        return requests.post(url, json=data)
