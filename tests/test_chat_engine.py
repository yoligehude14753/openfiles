import pytest

from src.chat.engine import ChatEngine
from src.chat.memory import format_history_for_rewrite
from src.chat.prompts import SYSTEM_PROMPT, CONTEXT_TEMPLATE, RAG_QUERY_REWRITE


class TestFormatContext:
    def test_empty_sources(self):
        assert ChatEngine._format_context([]) == ""

    def test_single_source(self):
        sources = [
            {
                "file_id": 1,
                "path": "/docs/report.pdf",
                "type": "pdf",
                "summary": "Quarterly earnings report",
                "keywords": "earnings, Q4, revenue",
            }
        ]
        result = ChatEngine._format_context(sources)
        assert "[File 1]" in result
        assert "/docs/report.pdf" in result
        assert "Quarterly earnings report" in result
        assert "earnings, Q4, revenue" in result

    def test_multiple_sources(self):
        sources = [
            {"file_id": 1, "path": "/a.pdf", "type": "pdf", "summary": "A", "keywords": "a"},
            {"file_id": 2, "path": "/b.md", "type": "md", "summary": "B", "keywords": "b"},
            {"file_id": 3, "path": "/c.txt", "type": "txt", "summary": "C", "keywords": "c"},
        ]
        result = ChatEngine._format_context(sources)
        assert "[File 1]" in result
        assert "[File 2]" in result
        assert "[File 3]" in result

    def test_missing_fields_handled(self):
        sources = [{"file_id": 1}]
        result = ChatEngine._format_context(sources)
        assert "[File 1]" in result
        assert "unknown" in result


class TestFormatHistoryForRewrite:
    def test_basic(self):
        history = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"},
        ]
        result = format_history_for_rewrite(history)
        assert "User: Hello" in result
        assert "Assistant: Hi there!" in result

    def test_truncates_long_content(self):
        history = [{"role": "user", "content": "x" * 500}]
        result = format_history_for_rewrite(history)
        assert len(result) < 500

    def test_limits_to_six_messages(self):
        history = [{"role": "user", "content": f"msg {i}"} for i in range(20)]
        result = format_history_for_rewrite(history)
        lines = [l for l in result.strip().split("\n") if l]
        assert len(lines) == 6


class TestPrompts:
    def test_system_prompt_not_empty(self):
        assert len(SYSTEM_PROMPT) > 50

    def test_context_template_has_placeholder(self):
        assert "{context}" in CONTEXT_TEMPLATE

    def test_rag_rewrite_has_placeholders(self):
        assert "{history}" in RAG_QUERY_REWRITE
        assert "{question}" in RAG_QUERY_REWRITE
