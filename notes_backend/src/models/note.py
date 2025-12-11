from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Note:
    """Represents a note entity."""
    id: Optional[int]
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
