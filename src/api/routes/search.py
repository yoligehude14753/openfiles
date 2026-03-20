from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.api.app import get_services

router = APIRouter()


class SearchRequest(BaseModel):
    query: str
    type: str = "files"
    limit: int = 10
    file_type: Optional[str] = None


@router.post("/search")
async def search(req: SearchRequest):
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query is required")

    session, search_service, _ = get_services()
    try:
        if req.type == "slides":
            results = await search_service.search_slides(req.query, limit=req.limit)
        else:
            results = await search_service.search_files(
                req.query, limit=req.limit, file_type=req.file_type
            )
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()
