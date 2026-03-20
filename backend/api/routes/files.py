import asyncio
import logging
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy import func

from src.api.app import get_services, get_db_session, _vector_store, _llm_service
from src.core.config import settings
from src.core.database import File, Slide, init_db, get_session
from src.core.indexing_service import IndexingService

logger = logging.getLogger(__name__)

router = APIRouter()

_indexing_in_progress = False


class IndexRequest(BaseModel):
    directories: Optional[list] = None


@router.get("/files")
async def list_files(
    file_type: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
):
    session = get_db_session()
    try:
        query = session.query(File)
        if file_type:
            query = query.filter(File.type == file_type)
        if status:
            query = query.filter(File.status == status)

        total = query.count()
        files = query.order_by(File.mtime.desc()).offset(offset).limit(limit).all()

        return {
            "total": total,
            "files": [
                {
                    "file_id": f.file_id,
                    "path": f.path,
                    "type": f.type,
                    "size": f.size,
                    "summary": f.summary,
                    "keywords": f.keywords,
                    "category": f.category,
                    "status": f.status,
                    "mtime": f.mtime.isoformat() if f.mtime else None,
                    "indexed_at": f.indexed_at.isoformat() if f.indexed_at else None,
                }
                for f in files
            ],
        }
    finally:
        session.close()


@router.get("/files/types")
async def file_type_stats():
    session = get_db_session()
    try:
        stats = (
            session.query(File.type, func.count(File.file_id))
            .filter(File.status == "completed")
            .group_by(File.type)
            .all()
        )
        return {t: c for t, c in stats}
    finally:
        session.close()


@router.post("/index")
async def start_indexing(background_tasks: BackgroundTasks):
    global _indexing_in_progress
    if _indexing_in_progress:
        raise HTTPException(status_code=409, detail="Indexing already in progress")

    _indexing_in_progress = True
    background_tasks.add_task(_run_indexing)
    return {"status": "started", "message": "Indexing started in background"}


async def _run_indexing():
    global _indexing_in_progress
    try:
        db_path = Path(settings.database_path)
        engine = init_db(str(db_path))
        session = get_session(engine)
        from src.search.vector_store import VectorStore
        vector_store = VectorStore(str(db_path))
        from src.core.llm_service import LLMService
        llm_service = LLMService()
        indexing_service = IndexingService(session, vector_store, llm_service)
        await indexing_service.index_all()
        vector_store.close()
    except Exception as e:
        logger.error("Indexing failed: %s", e)
    finally:
        _indexing_in_progress = False


@router.get("/index/status")
async def indexing_status():
    session = get_db_session()
    try:
        total = session.query(func.count(File.file_id)).scalar()
        completed = session.query(func.count(File.file_id)).filter(File.status == "completed").scalar()
        failed = session.query(func.count(File.file_id)).filter(File.status == "failed").scalar()
        pending = session.query(func.count(File.file_id)).filter(File.status == "pending").scalar()

        return {
            "in_progress": _indexing_in_progress,
            "total": total,
            "completed": completed,
            "failed": failed,
            "pending": pending,
        }
    finally:
        session.close()
