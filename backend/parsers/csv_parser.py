import csv
import io
from pathlib import Path
from typing import Dict, Any
from .base import BaseParser


class CsvParser(BaseParser):
    SUPPORTED_TYPES = ["csv"]

    def can_parse(self, file_type: str) -> bool:
        return file_type in self.SUPPORTED_TYPES

    def parse(self, file_path: Path) -> Dict[str, Any]:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                sample = f.read(8192)
                f.seek(0)

                try:
                    dialect = csv.Sniffer().sniff(sample)
                except csv.Error:
                    dialect = csv.excel

                reader = csv.reader(f, dialect)
                rows = []
                for i, row in enumerate(reader):
                    if i >= 500:
                        break
                    rows.append(row)

            if not rows:
                return {"content": "", "success": True}

            header = " | ".join(rows[0])
            lines = [f"Columns: {header}"]
            for row in rows[1:50]:
                lines.append(" | ".join(row))

            content = "\n".join(lines)
            return {
                "content": content,
                "num_rows": len(rows),
                "num_columns": len(rows[0]) if rows else 0,
                "success": True,
            }
        except Exception as e:
            return {"content": "", "error": str(e), "success": False}
