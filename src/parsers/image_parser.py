from pathlib import Path
from typing import Dict, Any
from PIL import Image
from .base import BaseParser

class ImageParser(BaseParser):
    SUPPORTED_TYPES = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'tiff', 'svg']

    def can_parse(self, file_type: str) -> bool:
        return file_type in self.SUPPORTED_TYPES

    def parse(self, file_path: Path) -> Dict[str, Any]:
        try:
            # For SVG, just read as text
            if file_path.suffix.lower() == '.svg':
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return {
                    'content': content,
                    'format': 'svg',
                    'success': True,
                    'needs_vision': False
                }

            # For raster images, extract metadata
            with Image.open(file_path) as img:
                return {
                    'format': img.format,
                    'mode': img.mode,
                    'size': img.size,
                    'width': img.width,
                    'height': img.height,
                    'file_path': str(file_path),
                    'success': True,
                    'needs_vision': True  # Will need LLM vision to understand content
                }
        except Exception as e:
            return {
                'error': str(e),
                'success': False
            }
