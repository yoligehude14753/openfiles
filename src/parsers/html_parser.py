from pathlib import Path
from typing import Dict, Any
from .base import BaseParser


class HtmlParser(BaseParser):
    SUPPORTED_TYPES = ["html"]

    def can_parse(self, file_type: str) -> bool:
        return file_type in self.SUPPORTED_TYPES

    def parse(self, file_path: Path) -> Dict[str, Any]:
        try:
            from bs4 import BeautifulSoup

            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                raw = f.read()

            soup = BeautifulSoup(raw, "html.parser")

            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()

            title = ""
            if soup.title and soup.title.string:
                title = soup.title.string.strip()

            text = soup.get_text(separator="\n", strip=True)
            lines = [line for line in text.split("\n") if line.strip()]
            content = "\n".join(lines)

            meta_desc = ""
            meta_tag = soup.find("meta", attrs={"name": "description"})
            if meta_tag and meta_tag.get("content"):
                meta_desc = meta_tag["content"]

            return {
                "content": content,
                "title": title,
                "meta_description": meta_desc,
                "char_count": len(content),
                "success": True,
            }
        except ImportError:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return {"content": f.read(), "success": True}
        except Exception as e:
            return {"content": "", "error": str(e), "success": False}
