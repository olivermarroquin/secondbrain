from dataclasses import dataclass
from typing import Optional

@dataclass
class RequisitionData:
    title: str
    fund_type: str
    description: Optional[str] = None
    priority: Optional[str] = None
