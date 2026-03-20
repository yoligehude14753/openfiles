import asyncio
import logging
from pathlib import Path
from typing import Callable, Optional

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent, FileModifiedEvent, FileDeletedEvent

from src.core.config import settings
from src.core.scanner import FileScanner

logger = logging.getLogger(__name__)


class _IndexHandler(FileSystemEventHandler):
    def __init__(self, scanner: FileScanner, on_change: Callable):
        self.scanner = scanner
        self.on_change = on_change
        self._debounce: dict = {}

    def _should_process(self, path_str: str) -> bool:
        path = Path(path_str)
        if self.scanner.should_skip_path(path):
            return False
        file_type = self.scanner.detect_file_type(path)
        return file_type is not None

    def on_created(self, event):
        if event.is_directory or not self._should_process(event.src_path):
            return
        logger.info("File created: %s", event.src_path)
        self.on_change("created", event.src_path)

    def on_modified(self, event):
        if event.is_directory or not self._should_process(event.src_path):
            return
        logger.info("File modified: %s", event.src_path)
        self.on_change("modified", event.src_path)

    def on_deleted(self, event):
        if event.is_directory:
            return
        logger.info("File deleted: %s", event.src_path)
        self.on_change("deleted", event.src_path)


class FileWatcher:
    def __init__(self, on_change: Callable):
        self.scanner = FileScanner()
        self.observer = Observer()
        self.on_change = on_change
        self._running = False

    def start(self):
        handler = _IndexHandler(self.scanner, self.on_change)

        for scan_dir in settings.scan_dirs_list:
            if scan_dir.exists():
                self.observer.schedule(handler, str(scan_dir), recursive=True)
                logger.info("Watching directory: %s", scan_dir)
            else:
                logger.warning("Directory does not exist, skipping watch: %s", scan_dir)

        self.observer.start()
        self._running = True
        logger.info("File watcher started")

    def stop(self):
        if self._running:
            self.observer.stop()
            self.observer.join()
            self._running = False
            logger.info("File watcher stopped")

    @property
    def is_running(self) -> bool:
        return self._running
