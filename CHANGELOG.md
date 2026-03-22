# Changelog

All notable changes to OpenFiles will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.1.0] - 2026-03-20

### Added

- Hybrid search engine combining semantic vector similarity (70%) and keyword matching (30%)
- RAG-powered chat interface with file citations and source references
- Support for 27 file types: PDF, DOCX, DOC, TXT, RTF, Markdown, XLSX, XLS, CSV, PPTX, PPT, JPG, PNG, GIF, WebP, SVG, TIFF, Python, JavaScript, TypeScript, Java, C/C++, HTML, CSS, JSON, YAML
- Real-time file watching with automatic re-indexing on changes
- CLI with commands: `init`, `index`, `reindex`, `search`, `stats`, `serve`
- REST + WebSocket API (FastAPI) with Swagger UI documentation
- React + TypeScript + Tailwind CSS frontend with dark mode
- Internationalization support (English and Chinese)
- Docker Compose setup with Ollama integration
- Multiple LLM provider support: Ollama (local), OpenAI, Yunwu, Claude, Kimi
- Multiple embedding provider support: text-embedding-3-small, Ollama nomic-embed-text, local SentenceTransformers
- SQLite-based storage for metadata, vectors, and chat history
- API key masking in settings endpoint
- Cost tracking and budget controls
- Setup script for quick local installation
