#!/usr/bin/env python3
"""OpenFiles server entry point for PyInstaller sidecar packaging."""
import uvicorn
from src.core.config import settings
from src.core.database import init_db
from pathlib import Path

if __name__ == "__main__":
    db_path = Path(settings.database_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    init_db(str(db_path))

    uvicorn.run(
        "src.api.app:app",
        host=settings.web_host,
        port=settings.web_port,
        log_level="info",
    )
