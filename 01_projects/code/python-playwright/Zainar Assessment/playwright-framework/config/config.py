"""
Centralized configuration - Enhanced with YAML environment support
"""
import os
import yaml
from pathlib import Path

class Config:
    def __init__(self):
        self.env = os.getenv('TEST_ENV', 'dev')
        self._load_from_yaml()
    
    def _load_from_yaml(self):
        try:
            config_file = Path(__file__).parent / 'environments.yaml'
            if config_file.exists():
                with open(config_file, 'r') as f:
                    all_configs = yaml.safe_load(f)
                    env_config = all_configs.get(self.env, all_configs.get('dev', {}))
                    self.BASE_URL = env_config.get('base_url', "https://the-internet.herokuapp.com")
                    self.DEFAULT_TIMEOUT = env_config.get('timeout', 30000)
                    self.SHORT_TIMEOUT = env_config.get('short_timeout', 5000)
                    self.LONG_TIMEOUT = env_config.get('long_timeout', 60000)
                    self.VIEWPORT_WIDTH = env_config.get('viewport_width', 1920)
                    self.VIEWPORT_HEIGHT = env_config.get('viewport_height', 1080)
            else:
                self._set_defaults()
        except Exception:
            self._set_defaults()
        
        self.SCREENSHOT_DIR = "reports/screenshots"
    
    def _set_defaults(self):
        self.BASE_URL = "https://the-internet.herokuapp.com"
        self.DEFAULT_TIMEOUT = 30000
        self.SHORT_TIMEOUT = 5000
        self.LONG_TIMEOUT = 60000
        self.VIEWPORT_WIDTH = 1920
        self.VIEWPORT_HEIGHT = 1080
    
    def get_url(self, path: str) -> str:
        return f"{config.BASE_URL}/{path.lstrip('/')}"

config = Config()
