# OpenFiles

> Open-source AI assistant for your local files.

**OpenFiles** helps you search, understand, and chat with your local documents using natural language — powered by any LLM, fully local with [Ollama](https://ollama.com).

<!-- TODO: Replace with a real demo recording -->
<!-- ![Demo](docs/demo.gif) -->

## Why OpenFiles?

Traditional file search (Spotlight, Everything) only matches filenames and exact keywords. OpenFiles **understands the content** of your files, finds what you mean (not just what you typed), and lets you ask follow-up questions with source citations.

## Highlights

- **Search by meaning** — Type _"find my Q4 budget report"_ and get results based on content, not filenames
- **Chat with citations** — Ask questions about your files and get AI answers that cite specific documents
- **27 file types** — PDFs, Word, Excel, PowerPoint, images, code, markdown, and more
- **Hybrid search** — 70% semantic (vector) + 30% keyword matching for accurate retrieval
- **Real-time indexing** — Watches your directories and auto-indexes new and changed files
- **Any LLM** — Works with any OpenAI-compatible API. Fully local with [Ollama](https://ollama.com) — no API key needed
- **Privacy-first** — Files stay on your machine. SQLite for everything — no Postgres, no Redis, no vector DB

## Quick Start

```bash
git clone https://github.com/yoligehude14753/openfiles.git
cd openfiles
cp .env.example .env
docker compose up
```

Open [http://localhost:3000](http://localhost:3000)

> **Want to set up manually?** See [Manual Setup](#manual-setup) below.

### Prerequisites

- **Python 3.9+**
- **Node.js 18+** (for the web UI)
- One of the following LLM providers:
  - **Ollama** (fully local, no API key) — install from [ollama.com](https://ollama.com)
  - **Any OpenAI-compatible API** (e.g. OpenRouter, Yunwu, etc.)
  - **OpenAI** directly

## Use Cases

- **"I remember the content, but not the filename"** — Describe what you're looking for in plain English. OpenFiles finds matching files by understanding their content.
- **"Summarize what matters across multiple files"** — Ask a question that spans several documents. Get a single answer with citations.
- **"Where does this concept appear in my codebase?"** — Search code, docs, and configs semantically.

## Supported File Types

| Category | Formats |
|----------|---------|
| Documents | PDF, DOCX, DOC, TXT, RTF, Markdown |
| Spreadsheets | XLSX, XLS, CSV |
| Presentations | PPTX, PPT |
| Images | JPG, PNG, GIF, WebP, SVG, TIFF |
| Code | Python, JavaScript, TypeScript, Java, C/C++, HTML, CSS, JSON, YAML |

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│   Frontend   │────▶│   FastAPI     │────▶│  LLM Provider   │
│   React/TS   │◀────│   Backend     │◀────│  (Ollama/OpenAI/ │
└─────────────┘     └──────┬───────┘     │   Yunwu/...)    │
                           │              └─────────────────┘
                    ┌──────┴───────┐
                    │   SQLite     │
                    │  + Vectors   │
                    └──────────────┘
```

- **Frontend**: React + TypeScript + Tailwind CSS
- **Backend**: FastAPI + Python
- **LLM**: Any OpenAI-compatible provider (Ollama, OpenAI, Yunwu, Claude, Kimi)
- **Embeddings**: text-embedding-3-small (default), Ollama, or local SentenceTransformers
- **Storage**: SQLite for metadata + numpy-powered vector similarity search
- **Parsing**: PyPDF2, python-docx, python-pptx, openpyxl, Pillow, BeautifulSoup

## Configuration

Copy `.env.example` to `.env` and customize:

```bash
# Use Ollama (local, no API key)
LLM_PROVIDER=ollama
EMBEDDING_PROVIDER=ollama

# Or use any OpenAI-compatible API
LLM_PROVIDER=yunwu
YUNWU_API_KEY=sk-your-key
YUNWU_BASE_URL=https://yunwu.ai/v1
YUNWU_MODEL=gpt-5.4-nano

# Directories to index
SCAN_DIRECTORIES=~/Documents,~/Desktop,~/Downloads
```

See [.env.example](.env.example) for all options.

## CLI Usage

```bash
python main.py init          # Initialize database
python main.py index         # Index all configured directories
python main.py reindex       # Clear old data and rebuild from scratch
python main.py search "..."  # Search from the terminal
python main.py stats         # Show indexing statistics
python main.py serve         # Start the web server
```

## API

The backend exposes a REST + WebSocket API:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/chat` | POST | Send a chat message |
| `/api/v1/chat/stream` | WS | Stream chat responses |
| `/api/v1/search` | POST | Semantic file search |
| `/api/v1/files` | GET | List indexed files |
| `/api/v1/index` | POST | Trigger indexing |
| `/api/v1/stats` | GET | Get statistics |
| `/api/v1/settings` | GET | Get/update settings |
| `/api/health` | GET | Health check |

Full API docs at [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI).

## Manual Setup

```bash
git clone https://github.com/yoligehude14753/openfiles.git
cd openfiles
./setup.sh
```

Then start the backend and frontend:

```bash
# Terminal 1 - Backend
source venv/bin/activate
python main.py serve

# Terminal 2 - Frontend
cd frontend && npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

## Roadmap

- [x] Chat interface with RAG (Retrieval-Augmented Generation)
- [x] Ollama (local LLM) support
- [x] Hybrid search (vector + keyword)
- [x] File watcher (real-time indexing)
- [x] Multi-format parsers (PDF, DOCX, XLSX, PPTX, images, code)
- [x] Dark mode UI with i18n (English + Chinese)
- [ ] Voice input (OpenAI Realtime API)
- [ ] Desktop app (Tauri) with Spotlight-style UX
- [ ] Slide-level search & export
- [ ] Plugin system for custom parsers
- [ ] Multi-user support

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

```bash
# Development setup
./setup.sh
source venv/bin/activate
python main.py serve  # Backend

cd frontend
npm run dev  # Frontend with hot reload
```

## License

[MIT](LICENSE) — use it however you want.

---

**OpenFiles** is built with Python, React, and a lot of caffeine. If you find it useful, please give it a star!
