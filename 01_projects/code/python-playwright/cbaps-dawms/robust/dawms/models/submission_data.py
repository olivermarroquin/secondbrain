from dataclasses import dataclass
from typing import Optional

@dataclass
class SubmissionData:
    submission_type: str
    application_number: str
    sponsor_name: Optional[str] = None
    drug_name: Optional[str] = None
