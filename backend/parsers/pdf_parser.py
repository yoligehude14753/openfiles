from pathlib import Path
from typing import Dict, Any
import PyPDF2
from .base import BaseParser

class PDFParser(BaseParser):
    SUPPORTED_TYPES = ["pdf"]

    def can_parse(self, file_type: str) -> bool:
        return file_type in self.SUPPORTED_TYPES

    def parse(self, file_path: Path) -> Dict[str, Any]:
        try:
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                num_pages = len(reader.pages)

                # Extract text from all pages
                text_content = []
                for page_num in range(num_pages):
                    page = reader.pages[page_num]
                    text = page.extract_text()
                    text_content.append(text)

                full_text = '\n\n'.join(text_content)

                # Extract metadata
                metadata = reader.metadata if reader.metadata else {}

                return {
                    'content': full_text,
                    'num_pages': num_pages,
                    'metadata': {
                        'title': metadata.get('/Title', ''),
                        'author': metadata.get('/Author', ''),
                        'subject': metadata.get('/Subject', ''),
                        'creator': metadata.get('/Creator', ''),
                    },
                    'pages': [{'page_num': i+1, 'text': text} for i, text in enumerate(text_content)],
                    'success': True
                }
        except Exception as e:
            return {
                'content': '',
                'error': str(e),
                'success': False
            }
