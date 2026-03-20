from pathlib import Path
from typing import Dict, Any
from .base import BaseParser

class TextParser(BaseParser):
    SUPPORTED_TYPES = ['txt', 'py', 'js', 'ts', 'java', 'c', 'cpp', 'css', 'json', 'xml', 'yaml', 'yml']

    def can_parse(self, file_type: str) -> bool:
        return file_type in self.SUPPORTED_TYPES

    def parse(self, file_path: Path) -> Dict[str, Any]:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            return {
                'content': content,
                'char_count': len(content),
                'line_count': content.count('\n') + 1,
                'success': True
            }
        except Exception as e:
            return {
                'content': '',
                'error': str(e),
                'success': False
            }
