#!/bin/bash
set -e

echo "🚀 Building Complete Python-Selenium Framework with 60+ methods..."

# Create all __init__ files
for dir in shared cbaps cbaps/pages cbaps/models cbaps/tests cbaps/api dawms dawms/pages dawms/models dawms/tests dawms/api; do
    touch $dir/__init__.py
done

# ========== ROOT FILES ==========
cat > requirements.txt << 'EOF'
selenium==4.15.2
webdriver-manager==4.0.1
pytest==7.4.3
pytest-xdist==3.5.0
pytest-html==4.1.1
requests==2.31.0
faker==21.0.0
loguru==0.7.2
EOF

cat > pytest.ini << 'EOF'
[pytest]
testpaths = cbaps/tests dawms/tests
addopts = -v --html=reports/report.html -n auto
markers =
    cbaps: CBAPS tests
    dawms: DAWMS tests
    smoke: Smoke tests
    api: API tests
log_cli = true
log_cli_level = INFO
EOF

cat > conftest.py << 'EOF'
import pytest
from shared.selenium_manager import SeleniumManager

@pytest.fixture(scope="function")
def selenium_mgr():
    m = SeleniumManager()
    m.init_selenium()
    yield m
    m.close_selenium()

@pytest.fixture(scope="function")
def driver(selenium_mgr):
    return selenium_mgr.driver
EOF

cat > shared/base_test.py << 'EOF'
import pytest
from loguru import logger

class BaseTest:
    @pytest.fixture(autouse=True)
    def setup(self, selenium_mgr, driver):
        self.selenium = selenium_mgr
        self.driver = driver
        logger.info("🚀 Test started")
        yield
        logger.info("✅ Test completed")
    
    def log_step(self, msg: str):
        logger.info(f"📋 {msg}")
    
    def log_pass(self, msg: str):
        logger.success(f"✅ {msg}")
EOF

cat > shared/config.py << 'EOF'
CBAPS_URL = "https://cbaps.example.com"
DAWMS_URL = "https://dawms.example.com"
CBAPS_API = "https://api.cbaps.example.com"
DAWMS_API = "https://api.dawms.example.com"
EOF

# ========== CBAPS MODELS ==========
cat > cbaps/models/requisition_data.py << 'EOF'
from dataclasses import dataclass
from typing import Optional

@dataclass
class RequisitionData:
    title: str
    fund_type: str
    description: Optional[str] = None
    priority: Optional[str] = None
EOF

cat > cbaps/models/funding_line_data.py << 'EOF'
from dataclasses import dataclass

@dataclass
class FundingLineData:
    amount: str
    fiscal_year: str
EOF

# ========== DAWMS MODELS ==========
cat > dawms/models/submission_data.py << 'EOF'
from dataclasses import dataclass
from typing import Optional

@dataclass
class SubmissionData:
    submission_type: str
    application_number: str
    sponsor_name: Optional[str] = None
    drug_name: Optional[str] = None
EOF

cat > dawms/models/reviewer_data.py << 'EOF'
from dataclasses import dataclass
from typing import Optional

@dataclass
class ReviewerData:
    name: str
    role: str
    specialty: Optional[str] = None
EOF

echo "✅ Models and config created"
