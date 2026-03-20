import re
import logging
from typing import List, Dict, Any, Optional

from sqlalchemy.orm import Session
from sqlalchemy import or_

from src.core.database import File, Slide
from src.search.vector_store import VectorStore
from src.core.llm_service import LLMService

logger = logging.getLogger(__name__)


class SearchService:
    def __init__(self, db_session: Session, vector_store: VectorStore, llm_service: LLMService):
        self.db_session = db_session
        self.vector_store = vector_store
        self.llm_service = llm_service

    async def search_files(
        self,
        query: str,
        limit: int = 10,
        file_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        query_embedding = await self.llm_service.get_embedding(query)
        if not query_embedding:
            return self.search_by_keyword(query, file_type=file_type, limit=limit)

        vector_results = self.vector_store.search_files(query_embedding, limit=limit * 2)
        keyword_results = self._keyword_score_files(query)

        merged = self._merge_results(vector_results, keyword_results, limit)

        file_results = []
        for file_id, score in merged:
            file = self.db_session.query(File).filter(File.file_id == file_id).first()
            if not file:
                continue
            if file_type and file.type != file_type:
                continue
            file_results.append({
                "file_id": file.file_id,
                "path": file.path,
                "type": file.type,
                "summary": file.summary,
                "keywords": file.keywords,
                "category": file.category,
                "confidence": file.confidence,
                "similarity": score,
                "size": file.size,
                "mtime": file.mtime.isoformat() if file.mtime else None,
            })

        return file_results[:limit]

    async def search_slides(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        query_embedding = await self.llm_service.get_embedding(query)
        if not query_embedding:
            return []

        results = self.vector_store.search_slides(query_embedding, limit=limit)

        slide_results = []
        for slide_id, similarity in results:
            slide = self.db_session.query(Slide).filter(Slide.slide_id == slide_id).first()
            if slide and slide.file:
                slide_results.append({
                    "slide_id": slide.slide_id,
                    "file_id": slide.file_id,
                    "file_path": slide.file.path,
                    "page_number": slide.page_number,
                    "title": slide.title,
                    "summary": slide.summary,
                    "keywords": slide.keywords,
                    "notes": slide.notes,
                    "thumbnail_path": slide.thumbnail_path,
                    "confidence": slide.confidence,
                    "similarity": similarity,
                })

        return slide_results

    def search_by_keyword(
        self, keyword: str, file_type: Optional[str] = None, limit: int = 20
    ) -> List[Dict[str, Any]]:
        safe_keyword = f"%{keyword}%"
        query = self.db_session.query(File).filter(
            or_(
                File.summary.like(safe_keyword),
                File.keywords.like(safe_keyword),
            )
        )
        if file_type:
            query = query.filter(File.type == file_type)

        query = query.filter(File.status == "completed")
        query = query.order_by(File.mtime.desc()).limit(limit)

        return [
            {
                "file_id": f.file_id,
                "path": f.path,
                "type": f.type,
                "summary": f.summary,
                "keywords": f.keywords,
                "category": f.category,
                "similarity": 0.5,
                "size": f.size,
                "mtime": f.mtime.isoformat() if f.mtime else None,
            }
            for f in query.all()
        ]

    def get_file_content_for_chat(self, file_ids: List[int]) -> List[Dict[str, Any]]:
        """Retrieve file summaries and keywords for RAG context assembly."""
        results = []
        for fid in file_ids:
            f = self.db_session.query(File).filter(File.file_id == fid).first()
            if f and f.summary:
                results.append({
                    "file_id": f.file_id,
                    "path": f.path,
                    "type": f.type,
                    "summary": f.summary,
                    "keywords": f.keywords,
                })
        return results

    def _keyword_score_files(self, query: str) -> Dict[int, float]:
        terms = re.split(r"\s+", query.lower().strip())
        if not terms:
            return {}

        files = (
            self.db_session.query(File)
            .filter(File.status == "completed")
            .all()
        )

        scores: Dict[int, float] = {}
        for f in files:
            text = f"{f.summary or ''} {f.keywords or ''}".lower()
            hits = sum(1 for t in terms if t in text)
            if hits > 0:
                scores[f.file_id] = hits / len(terms)
        return scores

    @staticmethod
    def _merge_results(
        vector_results: List[tuple],
        keyword_scores: Dict[int, float],
        limit: int,
        vector_weight: float = 0.7,
        keyword_weight: float = 0.3,
    ) -> List[tuple]:
        combined: Dict[int, float] = {}

        for file_id, sim in vector_results:
            combined[file_id] = combined.get(file_id, 0) + sim * vector_weight

        for file_id, score in keyword_scores.items():
            combined[file_id] = combined.get(file_id, 0) + score * keyword_weight

        ranked = sorted(combined.items(), key=lambda x: x[1], reverse=True)
        return ranked[:limit]
