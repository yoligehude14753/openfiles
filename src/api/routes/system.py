import platform
import logging

from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import func

from src.api.app import get_db_session, _llm_service
from src.core.config import settings
from src.core.database import File, Slide, CostTracking

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/stats")
async def stats():
    session = get_db_session()
    try:
        total_files = session.query(func.count(File.file_id)).scalar()
        completed_files = session.query(func.count(File.file_id)).filter(File.status == "completed").scalar()
        total_slides = session.query(func.count(Slide.slide_id)).scalar()
        total_cost = session.query(func.sum(CostTracking.cost_usd)).scalar() or 0.0
        total_tokens = session.query(func.sum(CostTracking.tokens)).scalar() or 0

        return {
            "total_files": total_files,
            "indexed_files": completed_files,
            "total_slides": total_slides,
            "total_tokens": total_tokens,
            "total_cost": round(total_cost, 4),
        }
    finally:
        session.close()


@router.get("/settings")
async def get_settings():
    ollama_available = False
    if _llm_service:
        ollama_available = await _llm_service.check_ollama_available()

    return {
        "llm_provider": settings.llm_provider,
        "embedding_provider": settings.embedding_provider,
        "ollama_host": settings.ollama_host,
        "ollama_model": settings.ollama_model,
        "ollama_available": ollama_available,
        "scan_directories": [str(d) for d in settings.scan_dirs_list],
        "max_file_size_mb": settings.max_file_size_mb,
        "daily_budget_usd": settings.daily_budget_usd,
        "monthly_budget_usd": settings.monthly_budget_usd,
        "platform": platform.system(),
    }


from typing import Optional


class SettingsUpdate(BaseModel):
    llm_provider: Optional[str] = None
    ollama_model: Optional[str] = None
    scan_directories: Optional[str] = None


@router.put("/settings")
async def update_settings(update: SettingsUpdate):
    updated = {}
    if update.llm_provider:
        settings.llm_provider = update.llm_provider
        updated["llm_provider"] = update.llm_provider
    if update.ollama_model:
        settings.ollama_model = update.ollama_model
        updated["ollama_model"] = update.ollama_model
    if update.scan_directories:
        settings.scan_directories = update.scan_directories
        updated["scan_directories"] = update.scan_directories

    return {"status": "updated", "changes": updated}
