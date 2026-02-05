from dataclasses import dataclass
from typing import Optional

@dataclass
class ReviewerData:
    name: str
    role: str
    specialty: Optional[str] = None
