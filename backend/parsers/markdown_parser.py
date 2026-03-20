from pathlib import Path
from typing import Dict, Any
from .base import BaseParser


class MarkdownParser(BaseParser):
    SUPPORTED_TYPES = ["md"]

    def can_parse(self, file_type: str) -> bool:
        return file_type in self.SUPPORTED_TYPES

    def parse(self, file_path: Path) -> Dict[str, Any]:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                raw = f.read()

            frontmatter = {}
            content = raw

            if raw.startswith("---"):
                parts = raw.split("---", 2)
                if len(parts) >= 3:
                    fm_text = parts[1].strip()
                    content = parts[2].strip()
                    for line in fm_text.split("\n"):
                        if ":" in line:
                            key, _, val = line.partition(":")
                            frontmatter[key.strip()] = val.strip()

            headings = []
            links = []
            for line in content.split("\n"):
                stripped = line.strip()
                if stripped.startswith("#"):
                    level = len(stripped) - len(stripped.lstrip("#"))
                    heading_text = stripped.lstrip("#").strip()
                    if heading_text:
                        headings.append({"level": level, "text": heading_text})

                import re
                for match in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", line):
                    links.append({"text": match.group(1), "url": match.group(2)})

            return {
                "content": content,
                "frontmatter": frontmatter,
                "headings": headings,
                "links": links,
                "char_count": len(content),
                "success": True,
            }
        except Exception as e:
            return {"content": "", "error": str(e), "success": False}
