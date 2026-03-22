import pytest

from src.search.search_service import SearchService


class TestMergeResults:
    """Tests for the hybrid scoring algorithm (vector + keyword merge)."""

    def test_vector_only(self):
        vector = [(1, 0.9), (2, 0.7), (3, 0.5)]
        keyword = {}
        merged = SearchService._merge_results(vector, keyword, limit=3)

        assert merged[0][0] == 1
        assert merged[1][0] == 2
        assert merged[2][0] == 3

    def test_keyword_only(self):
        vector = []
        keyword = {1: 1.0, 2: 0.5}
        merged = SearchService._merge_results(vector, keyword, limit=2)

        assert merged[0][0] == 1
        assert merged[1][0] == 2

    def test_hybrid_merge_boosts_overlap(self):
        vector = [(1, 0.8), (2, 0.6)]
        keyword = {2: 1.0, 3: 0.5}
        merged = SearchService._merge_results(vector, keyword, limit=3)

        scores = {fid: score for fid, score in merged}
        assert scores[2] > scores[1], "File 2 should rank higher with both vector and keyword hits"

    def test_weights_applied_correctly(self):
        vector = [(1, 1.0)]
        keyword = {1: 1.0}
        merged = SearchService._merge_results(
            vector, keyword, limit=1, vector_weight=0.7, keyword_weight=0.3
        )

        assert abs(merged[0][1] - 1.0) < 1e-6  # 0.7*1.0 + 0.3*1.0 = 1.0

    def test_limit_respected(self):
        vector = [(i, 0.9 - i * 0.1) for i in range(10)]
        keyword = {}
        merged = SearchService._merge_results(vector, keyword, limit=3)
        assert len(merged) == 3

    def test_empty_inputs(self):
        merged = SearchService._merge_results([], {}, limit=5)
        assert merged == []

    def test_custom_weights(self):
        vector = [(1, 0.5)]
        keyword = {1: 0.8}
        merged_default = SearchService._merge_results(vector, keyword, limit=1)
        merged_keyword_heavy = SearchService._merge_results(
            vector, keyword, limit=1, vector_weight=0.3, keyword_weight=0.7
        )
        assert merged_keyword_heavy[0][1] > merged_default[0][1]


class TestKeywordScoring:
    """Tests for keyword-based file scoring using the DB session."""

    def test_keyword_score_hits(self, db_session, sample_files):
        from src.search.vector_store import VectorStore
        from unittest.mock import AsyncMock

        mock_llm = AsyncMock()
        vs = VectorStore.__new__(VectorStore)
        service = SearchService(db_session, vs, mock_llm)

        scores = service._keyword_score_files("investment strategy")
        assert sample_files[0].file_id in scores
        assert scores[sample_files[0].file_id] > 0

    def test_keyword_score_no_hits(self, db_session, sample_files):
        from src.search.vector_store import VectorStore
        from unittest.mock import AsyncMock

        mock_llm = AsyncMock()
        vs = VectorStore.__new__(VectorStore)
        service = SearchService(db_session, vs, mock_llm)

        scores = service._keyword_score_files("zzz_nonexistent_term")
        assert len(scores) == 0

    def test_keyword_excludes_pending(self, db_session, sample_files):
        from src.search.vector_store import VectorStore
        from unittest.mock import AsyncMock

        mock_llm = AsyncMock()
        vs = VectorStore.__new__(VectorStore)
        service = SearchService(db_session, vs, mock_llm)

        scores = service._keyword_score_files("pending")
        pending_file = sample_files[3]
        assert pending_file.file_id not in scores
