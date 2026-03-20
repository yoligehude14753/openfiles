import logging
from typing import List, Dict, Any, Tuple, AsyncGenerator

from sqlalchemy.orm import Session

from src.core.llm_service import LLMService
from src.core.config import settings
from src.search.search_service import SearchService
from src.chat.prompts import SYSTEM_PROMPT, CONTEXT_TEMPLATE, RAG_QUERY_REWRITE
from src.chat.memory import get_conversation_history, format_history_for_rewrite

logger = logging.getLogger(__name__)


class ChatEngine:
    def __init__(self, search_service: SearchService, llm_service: LLMService, session: Session):
        self.search = search_service
        self.llm = llm_service
        self.session = session

    async def generate_response(self, user_message: str, conversation_id: int) -> Tuple[str, List[dict]]:
        history = get_conversation_history(self.session, conversation_id)
        search_query = await self._rewrite_query(user_message, history)
        sources = await self._retrieve_context(search_query)
        context_text = self._format_context(sources)

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
        ]

        if context_text:
            messages.append({
                "role": "system",
                "content": CONTEXT_TEMPLATE.format(context=context_text),
            })

        for msg in history[-10:]:
            messages.append(msg)

        messages.append({"role": "user", "content": user_message})

        try:
            response = await self.llm.chat_completion(messages, stream=False)
            source_refs = [
                {"file_id": s["file_id"], "path": s["path"], "type": s["type"]}
                for s in sources
            ]
            return response, source_refs
        except Exception as e:
            logger.error("Chat generation failed: %s", e)
            return f"Sorry, I encountered an error: {e}", []

    async def generate_response_stream(
        self, user_message: str, conversation_id: int
    ) -> AsyncGenerator[Tuple[str, Any], None]:
        history = get_conversation_history(self.session, conversation_id)
        search_query = await self._rewrite_query(user_message, history)
        sources = await self._retrieve_context(search_query)
        context_text = self._format_context(sources)

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
        ]

        if context_text:
            messages.append({
                "role": "system",
                "content": CONTEXT_TEMPLATE.format(context=context_text),
            })

        for msg in history[-10:]:
            messages.append(msg)

        messages.append({"role": "user", "content": user_message})

        source_refs = [
            {"file_id": s["file_id"], "path": s["path"], "type": s["type"]}
            for s in sources
        ]
        if source_refs:
            yield ("sources", source_refs)

        try:
            stream = await self.llm.chat_completion(messages, stream=True)
            async for chunk in stream:
                yield ("text", chunk)
        except Exception as e:
            logger.error("Stream generation failed: %s", e)
            yield ("text", f"Sorry, I encountered an error: {e}")

    async def _rewrite_query(self, question: str, history: List[Dict[str, str]]) -> str:
        if not history or len(history) <= 1:
            return question

        try:
            history_text = format_history_for_rewrite(history)
            prompt = RAG_QUERY_REWRITE.format(history=history_text, question=question)
            messages = [{"role": "user", "content": prompt}]
            rewritten = await self.llm.chat_completion(messages, stream=False, temperature=0.1)
            return rewritten.strip() if rewritten else question
        except Exception:
            return question

    async def _retrieve_context(self, query: str) -> List[Dict[str, Any]]:
        try:
            results = await self.search.search_files(
                query, limit=settings.chat_max_context_chunks
            )
            return results
        except Exception as e:
            logger.error("Context retrieval failed: %s", e)
            return []

    @staticmethod
    def _format_context(sources: List[Dict[str, Any]]) -> str:
        if not sources:
            return ""

        parts = []
        for i, source in enumerate(sources, 1):
            path = source.get("path", "unknown")
            summary = source.get("summary", "")
            keywords = source.get("keywords", "")
            file_type = source.get("type", "")

            parts.append(
                f"[File {i}] {path} ({file_type})\n"
                f"Summary: {summary}\n"
                f"Keywords: {keywords}"
            )

        return "\n\n".join(parts)
