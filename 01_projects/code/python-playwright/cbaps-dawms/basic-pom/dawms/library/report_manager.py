"""
ReportManager: HTML report generation for DAWMS automation
Uses pytest-html for reporting (Python equivalent of ExtentReports)
"""

import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class ReportManager:
    """
    ReportManager handles HTML report generation.
    This is the Python equivalent of the Java ExtentReportManager.
    """
    
    def __init__(self):
        self.report_path = None
        self.setup_report()
    
    def setup_report(self):
        """Setup HTML report"""
        try:
            # Create report directory
            Path("target/report").mkdir(parents=True, exist_ok=True)
            
            # Generate timestamped report name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.report_path = f"target/report/dawms-automation-report-{timestamp}.html"
            
            logger.info(f"Report will be generated at: {self.report_path}")
            
        except Exception as e:
            logger.error(f"Failed to setup report: {e}")
            raise
    
    def finalize_report(self):
        """Finalize and flush report"""
        try:
            logger.info("Report finalized.")
            logger.info(f"Log file location: target/logs/automation.log")
            logger.info(f"Screenshot location: target/screenshot/")
            logger.info(f"Video location: target/videos/")
            logger.info(f"HTML report location: {self.report_path}")
        except Exception as e:
            logger.error(f"Failed to finalize report: {e}")
    
    @staticmethod
    def get_report_metadata():
        """Get report metadata for pytest-html"""
        return {
            "Application": "DAWMS",
            "Environment": "QA/Test",
            "Automation Developer": "QA Team"
        }


# Note: To use pytest-html, run tests with:
# pytest --html=target/report/dawms-report.html --self-contained-html
