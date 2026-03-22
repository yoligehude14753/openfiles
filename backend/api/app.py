import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.core.config import settings
from src.core.database import init_db, get_session
from src.core.llm_service import LLMService
from src.search.vector_store import VectorStore
from src.search.search_service import SearchService
from src.chat.engine import ChatEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_engine = None
_vector_store = None
_llm_service = None


def get_db_session():
    return get_session(_engine)


def get_services():
    session = get_db_session()
    search_service = SearchService(session, _vector_store, _llm_service)
    chat_engine = ChatEngine(search_service, _llm_service, session)
    return session, search_service, chat_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _engine, _vector_store, _llm_service

    db_path = Path(settings.database_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    _engine = init_db(str(db_path))
    _vector_store = VectorStore(str(db_path))
    _llm_service = LLMService()

    ollama_ok = await _llm_service.check_ollama_available()
    if settings.is_ollama_provider and not ollama_ok:
        logger.warning(
            "Ollama not reachable at %s. Install from https://ollama.com "
            "or set LLM_PROVIDER to openai/claude/kimi in .env",
            settings.ollama_host,
        )

    logger.info("OpenFiles backend started on %s:%s", settings.web_host, settings.web_port)
    yield

    if _vector_store:
        _vector_store.close()


app = FastAPI(
    title="OpenFiles",
    description="Open-source AI assistant for your local files.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from src.api.routes import search, chat, files, system  # noqa: E402

app.include_router(search.router, prefix="/api/v1", tags=["search"])
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])
app.include_router(files.router, prefix="/api/v1", tags=["files"])
app.include_router(system.router, prefix="/api/v1", tags=["system"])


@app.get("/api/health")
async def health():
    return {"status": "ok", "version": "0.1.0"}
