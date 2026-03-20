from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any

class BaseParser(ABC):
    @abstractmethod
    def parse(self, file_path: Path) -> Dict[str, Any]:
        """Parse file and return extracted content."""
        pass

    @abstractmethod
    def can_parse(self, file_type: str) -> bool:
        """Check if parser can handle this file type."""
        pass
