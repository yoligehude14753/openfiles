import numpy as np
import pytest

from src.search.vector_store import VectorStore


class TestVectorSerialization:
    def test_roundtrip(self):
        vec = [0.1, 0.2, 0.3, -0.4, 0.5]
        blob = VectorStore._serialize_vector(vec)
        restored = VectorStore._deserialize_vector(blob)
        np.testing.assert_allclose(restored, vec, atol=1e-6)

    def test_high_dimensional(self):
        vec = np.random.randn(1536).tolist()
        blob = VectorStore._serialize_vector(vec)
        restored = VectorStore._deserialize_vector(blob)
        np.testing.assert_allclose(restored, vec, atol=1e-6)


class TestVectorStoreSearch:
    def test_add_and_search_files(self, vector_store):
        v1 = [1.0, 0.0, 0.0]
        v2 = [0.0, 1.0, 0.0]
        v3 = [0.9, 0.1, 0.0]

        vector_store.add_file_embedding(1, v1)
        vector_store.add_file_embedding(2, v2)
        vector_store.add_file_embedding(3, v3)

        results = vector_store.search_files([1.0, 0.0, 0.0], limit=3)

        assert len(results) == 3
        ids = [r[0] for r in results]
        assert ids[0] == 1
        assert ids[1] == 3

    def test_search_empty_store(self, vector_store):
        results = vector_store.search_files([1.0, 0.0, 0.0], limit=5)
        assert results == []

    def test_zero_query_vector(self, vector_store):
        vector_store.add_file_embedding(1, [1.0, 0.0, 0.0])
        results = vector_store.search_files([0.0, 0.0, 0.0], limit=5)
        assert results == []

    def test_limit_respected(self, vector_store):
        for i in range(10):
            vector_store.add_file_embedding(i, np.random.randn(3).tolist())

        results = vector_store.search_files([1.0, 0.0, 0.0], limit=3)
        assert len(results) == 3

    def test_cosine_similarity_correctness(self, vector_store):
        vector_store.add_file_embedding(1, [1.0, 0.0])
        vector_store.add_file_embedding(2, [0.0, 1.0])

        results = vector_store.search_files([1.0, 0.0], limit=2)
        assert results[0][0] == 1
        assert abs(results[0][1] - 1.0) < 1e-5
        assert abs(results[1][1] - 0.0) < 1e-5

    def test_upsert_overwrites(self, vector_store):
        vector_store.add_file_embedding(1, [1.0, 0.0, 0.0])
        vector_store.add_file_embedding(1, [0.0, 1.0, 0.0])

        results = vector_store.search_files([0.0, 1.0, 0.0], limit=1)
        assert results[0][0] == 1
        assert results[0][1] > 0.99


class TestSlideSearch:
    def test_add_and_search_slides(self, vector_store):
        vector_store.add_slide_embedding(10, [1.0, 0.0])
        vector_store.add_slide_embedding(20, [0.0, 1.0])

        results = vector_store.search_slides([0.9, 0.1], limit=2)
        assert results[0][0] == 10

    def test_get_embedding_count(self, vector_store):
        vector_store.add_file_embedding(1, [1.0, 0.0])
        vector_store.add_file_embedding(2, [0.0, 1.0])
        vector_store.add_slide_embedding(10, [1.0, 0.0])

        counts = vector_store.get_embedding_count()
        assert counts["files"] == 2
        assert counts["slides"] == 1
