from pathlib import Path
from typing import Dict, Any
from .text_parser import TextParser
from .pdf_parser import PDFParser
from .image_parser import ImageParser
from .docx_parser import DocxParser
from .pptx_parser import PPTXParser
from .xlsx_parser import XlsxParser
from .csv_parser import CsvParser
from .markdown_parser import MarkdownParser
from .html_parser import HtmlParser


class ParserFactory:
    def __init__(self):
        self.parsers = [
            MarkdownParser(),
            TextParser(),
            PDFParser(),
            ImageParser(),
            DocxParser(),
            PPTXParser(),
            XlsxParser(),
            CsvParser(),
            HtmlParser(),
        ]

    def get_parser(self, file_type: str):
        for parser in self.parsers:
            if parser.can_parse(file_type):
                return parser
        return None

    def parse_file(self, file_path: Path, file_type: str) -> Dict[str, Any]:
        parser = self.get_parser(file_type)
        if parser:
            return parser.parse(file_path)
        return {
            "content": "",
            "error": f"No parser available for file type: {file_type}",
            "success": False,
        }

    def supported_types(self) -> list:
        types = set()
        for parser in self.parsers:
            if hasattr(parser, "SUPPORTED_TYPES"):
                types.update(parser.SUPPORTED_TYPES)
        return sorted(types)
