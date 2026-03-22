from pydantic_settings import BaseSettings
from typing import List, Optional
from pathlib import Path
import platform


class Settings(BaseSettings):
    # API Keys
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    kimi_api_key: str = ""

    # OpenAI-compatible API (works with any compatible endpoint)
    openai_compatible_api_key: str = ""
    openai_compatible_base_url: str = ""
    openai_compatible_model: str = "gpt-4o-mini"
    openai_compatible_embedding_model: str = "text-embedding-3-small"

    # Legacy yunwu fields (mapped to openai-compatible)
    yunwu_api_key: str = ""
    yunwu_base_url: str = "https://yunwu.ai/v1"
    yunwu_model: str = "gpt-5.4-nano"
    yunwu_embedding_model: str = "text-embedding-3-small"

    # Ollama (local LLM)
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"
    ollama_embedding_model: str = "nomic-embed-text"

    # LLM Provider: ollama, openai, claude, kimi, openai-compatible, yunwu
    llm_provider: str = "ollama"

    # Embedding Provider: ollama, openai, local, openai-compatible, yunwu
    embedding_provider: str = "ollama"
    embedding_model: str = "text-embedding-3-small"

    # Database
    database_path: str = "./data/db/files.db"

    # Indexing
    scan_directories: str = "~/Documents,~/Desktop,~/Downloads"
    exclude_patterns: str = ".git,.DS_Store,node_modules,__pycache__,venv,.venv"
    max_file_size_mb: int = 100

    # Cost Controls
    daily_budget_usd: float = 10.0
    monthly_budget_usd: float = 100.0

    # Privacy
    privacy_mode: bool = False
    blacklist_dirs: str = ".ssh,.gnupg"

    # Performance
    max_concurrent_llm: int = 3
    max_concurrent_embedding: int = 5
    chunk_size: int = 4000

    # Web Server
    web_host: str = "0.0.0.0"
    web_port: int = 8000

    # Chat
    chat_max_history: int = 20
    chat_max_context_chunks: int = 5

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def scan_dirs_list(self) -> List[Path]:
        return [Path(d.strip()).expanduser() for d in self.scan_directories.split(",") if d.strip()]

    @property
    def exclude_patterns_list(self) -> List[str]:
        return [p.strip() for p in self.exclude_patterns.split(",") if p.strip()]

    @property
    def blacklist_dirs_list(self) -> List[str]:
        base = [d.strip() for d in self.blacklist_dirs.split(",") if d.strip()]
        if platform.system() == "Darwin":
            base.extend([
                "Library/Keychains",
                "Library/Application Support/Google/Chrome",
            ])
        return base

    @property
    def is_ollama_provider(self) -> bool:
        return self.llm_provider == "ollama"

    @property
    def effective_compatible_api_key(self) -> str:
        return self.openai_compatible_api_key or self.yunwu_api_key

    @property
    def effective_compatible_base_url(self) -> str:
        return self.openai_compatible_base_url or self.yunwu_base_url

    @property
    def effective_compatible_model(self) -> str:
        return self.openai_compatible_model if self.openai_compatible_api_key else self.yunwu_model

    @property
    def effective_compatible_embedding_model(self) -> str:
        return self.openai_compatible_embedding_model if self.openai_compatible_api_key else self.yunwu_embedding_model


settings = Settings()
