import os
import hashlib
import platform
from pathlib import Path
from typing import Generator, Tuple, Optional
from datetime import datetime

from src.core.config import settings


class FileScanner:
    SUPPORTED_TYPES = {
        # Documents
        "application/pdf": "pdf",
        "application/msword": "doc",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
        "text/plain": "txt",
        "text/markdown": "md",
        "text/html": "html",
        "application/rtf": "rtf",
        # Spreadsheets
        "application/vnd.ms-excel": "xls",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",
        "text/csv": "csv",
        # Presentations
        "application/vnd.ms-powerpoint": "ppt",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation": "pptx",
        # Images
        "image/jpeg": "jpg",
        "image/png": "png",
        "image/gif": "gif",
        "image/webp": "webp",
        "image/svg+xml": "svg",
        "image/tiff": "tiff",
        # Code
        "text/x-python": "py",
        "text/x-java": "java",
        "text/x-c": "c",
        "text/x-c++": "cpp",
        "application/javascript": "js",
        "application/typescript": "ts",
    }

    EXT_MAP = {
        ".txt": "txt", ".md": "md", ".py": "py", ".js": "js",
        ".ts": "ts", ".java": "java", ".c": "c", ".cpp": "cpp",
        ".html": "html", ".htm": "html", ".css": "css",
        ".json": "json", ".xml": "xml", ".yaml": "yaml", ".yml": "yaml",
        ".pdf": "pdf", ".doc": "doc", ".docx": "docx",
        ".xls": "xls", ".xlsx": "xlsx", ".csv": "csv",
        ".ppt": "ppt", ".pptx": "pptx",
        ".jpg": "jpg", ".jpeg": "jpg", ".png": "png",
        ".gif": "gif", ".webp": "webp", ".svg": "svg", ".tiff": "tiff",
    }

    SYSTEM_SKIP_DIRS = {"__pycache__", "node_modules", ".git", "venv", ".venv", ".tox", ".mypy_cache"}

    def __init__(self):
        self._magic = None
        self.max_size = settings.max_file_size_mb * 1024 * 1024
        self.blacklist_dirs = settings.blacklist_dirs_list
        self.exclude_patterns = settings.exclude_patterns_list

        if platform.system() == "Darwin":
            self.SYSTEM_SKIP_DIRS.update({"Library", "Applications"})
        elif platform.system() == "Windows":
            self.SYSTEM_SKIP_DIRS.update({"AppData", "Windows", "Program Files", "Program Files (x86)"})

    @property
    def magic(self):
        if self._magic is None:
            try:
                import magic
                self._magic = magic.Magic(mime=True)
            except ImportError:
                self._magic = False
        return self._magic if self._magic is not False else None

    def should_skip_path(self, path: Path) -> bool:
        path_str = str(path)

        for blacklist in self.blacklist_dirs:
            if blacklist in path_str:
                return True

        for pattern in self.exclude_patterns:
            if pattern in path.name:
                return True

        if path.name.startswith(".") and path.name not in (".env", ".gitignore"):
            return True

        if any(sd in path.parts for sd in self.SYSTEM_SKIP_DIRS):
            return True

        return False

    def scan_directories(self) -> Generator[Tuple[Path, str, int], None, None]:
        for scan_dir in settings.scan_dirs_list:
            if not scan_dir.exists():
                continue

            for root, dirs, files in os.walk(scan_dir):
                root_path = Path(root)
                dirs[:] = [d for d in dirs if not self.should_skip_path(root_path / d)]

                for file in files:
                    file_path = root_path / file

                    if self.should_skip_path(file_path):
                        continue

                    try:
                        stat = file_path.stat()
                        if stat.st_size > self.max_size or stat.st_size == 0:
                            continue

                        file_type = self.detect_file_type(file_path)
                        if file_type:
                            yield file_path, file_type, stat.st_size

                    except (PermissionError, OSError):
                        continue

    def detect_file_type(self, path: Path) -> Optional[str]:
        ext = path.suffix.lower()
        if ext in self.EXT_MAP:
            return self.EXT_MAP[ext]

        if self.magic:
            try:
                mime_type = self.magic.from_file(str(path))
                if mime_type in self.SUPPORTED_TYPES:
                    return self.SUPPORTED_TYPES[mime_type]
            except Exception:
                pass

        return None

    @staticmethod
    def compute_file_hash(path: Path) -> str:
        sha256 = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        return sha256.hexdigest()

    @staticmethod
    def get_file_metadata(path: Path) -> dict:
        stat = path.stat()
        return {
            "path": str(path),
            "size": stat.st_size,
            "ctime": datetime.fromtimestamp(stat.st_ctime),
            "mtime": datetime.fromtimestamp(stat.st_mtime),
        }
