import sqlite3
import struct
import logging
from typing import List, Tuple, Optional

import numpy as np

logger = logging.getLogger(__name__)


class VectorStore:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._init_vector_tables()

    def _init_vector_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS file_embeddings (
                file_id INTEGER PRIMARY KEY,
                embedding BLOB NOT NULL,
                FOREIGN KEY (file_id) REFERENCES files(file_id) ON DELETE CASCADE
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS slide_embeddings (
                slide_id INTEGER PRIMARY KEY,
                embedding BLOB NOT NULL,
                FOREIGN KEY (slide_id) REFERENCES slides(slide_id) ON DELETE CASCADE
            )
        """)
        self.conn.commit()

    @staticmethod
    def _serialize_vector(vector: List[float]) -> bytes:
        return struct.pack(f"{len(vector)}f", *vector)

    @staticmethod
    def _deserialize_vector(data: bytes) -> np.ndarray:
        n = len(data) // 4
        return np.array(struct.unpack(f"{n}f", data), dtype=np.float32)

    def add_file_embedding(self, file_id: int, embedding: List[float]):
        blob = self._serialize_vector(embedding)
        self.conn.execute(
            "INSERT OR REPLACE INTO file_embeddings (file_id, embedding) VALUES (?, ?)",
            (file_id, blob),
        )
        self.conn.commit()

    def add_slide_embedding(self, slide_id: int, embedding: List[float]):
        blob = self._serialize_vector(embedding)
        self.conn.execute(
            "INSERT OR REPLACE INTO slide_embeddings (slide_id, embedding) VALUES (?, ?)",
            (slide_id, blob),
        )
        self.conn.commit()

    def search_files(self, query_embedding: List[float], limit: int = 10) -> List[Tuple[int, float]]:
        return self._search("file_embeddings", "file_id", query_embedding, limit)

    def search_slides(self, query_embedding: List[float], limit: int = 20) -> List[Tuple[int, float]]:
        return self._search("slide_embeddings", "slide_id", query_embedding, limit)

    def _search(self, table: str, id_col: str, query_embedding: List[float], limit: int) -> List[Tuple[int, float]]:
        cursor = self.conn.execute(f"SELECT {id_col}, embedding FROM {table}")
        rows = cursor.fetchall()
        if not rows:
            return []

        query_vec = np.array(query_embedding, dtype=np.float32)
        query_norm = np.linalg.norm(query_vec)
        if query_norm == 0:
            return []
        query_vec = query_vec / query_norm

        ids = []
        embeddings = []
        for row_id, blob in rows:
            ids.append(row_id)
            embeddings.append(self._deserialize_vector(blob))

        matrix = np.vstack(embeddings)
        norms = np.linalg.norm(matrix, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        matrix = matrix / norms

        similarities = matrix @ query_vec
        top_indices = np.argsort(similarities)[::-1][:limit]

        return [(ids[i], float(similarities[i])) for i in top_indices]

    def get_file_embedding(self, file_id: int) -> Optional[List[float]]:
        row = self.conn.execute(
            "SELECT embedding FROM file_embeddings WHERE file_id = ?", (file_id,)
        ).fetchone()
        if row:
            return self._deserialize_vector(row[0]).tolist()
        return None

    def get_embedding_count(self) -> dict:
        file_count = self.conn.execute("SELECT COUNT(*) FROM file_embeddings").fetchone()[0]
        slide_count = self.conn.execute("SELECT COUNT(*) FROM slide_embeddings").fetchone()[0]
        return {"files": file_count, "slides": slide_count}

    def close(self):
        self.conn.close()
