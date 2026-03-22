import os
import tempfile
import pytest
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.database import Base, File, Slide, Conversation, Message
from src.search.vector_store import VectorStore


@pytest.fixture
def tmp_db_path(tmp_path):
    return str(tmp_path / "test.db")


@pytest.fixture
def db_engine(tmp_db_path):
    engine = create_engine(f"sqlite:///{tmp_db_path}", echo=False)
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture
def db_session(db_engine):
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def vector_store(tmp_db_path):
    store = VectorStore(tmp_db_path)
    yield store
    store.close()


@pytest.fixture
def sample_files(db_session):
    """Insert a set of sample files for search tests."""
    files = [
        File(
            path="/docs/q4-strategy.pdf",
            type="pdf",
            size=1024,
            status="completed",
            summary="Q4 investment strategy report with market analysis and portfolio recommendations",
            keywords="investment, strategy, Q4, portfolio, market",
            category="finance",
            confidence=0.95,
        ),
        File(
            path="/docs/meeting-notes.md",
            type="md",
            size=512,
            status="completed",
            summary="Weekly team meeting notes discussing project milestones and deadlines",
            keywords="meeting, notes, project, milestones, deadlines",
            category="work",
            confidence=0.90,
        ),
        File(
            path="/docs/recipe.txt",
            type="txt",
            size=256,
            status="completed",
            summary="Pasta carbonara recipe with traditional Italian ingredients",
            keywords="pasta, carbonara, recipe, Italian, cooking",
            category="personal",
            confidence=0.88,
        ),
        File(
            path="/docs/pending.pdf",
            type="pdf",
            size=2048,
            status="pending",
            summary=None,
            keywords=None,
            category=None,
            confidence=None,
        ),
    ]
    for f in files:
        db_session.add(f)
    db_session.commit()
    return files


@pytest.fixture
def sample_text_file(tmp_path):
    p = tmp_path / "hello.txt"
    p.write_text("Hello, world!\nThis is a test file.\nLine three.")
    return p


@pytest.fixture
def sample_markdown_file(tmp_path):
    p = tmp_path / "doc.md"
    p.write_text(
        "---\ntitle: Test Doc\nauthor: OpenFiles\n---\n"
        "# Heading One\n\nSome content with a [link](https://example.com).\n\n"
        "## Heading Two\n\nMore content here."
    )
    return p
