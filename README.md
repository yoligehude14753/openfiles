# ChatFiles

> Chat with your files. Locally. Privately.

**ChatFiles** is an open-source AI file assistant that indexes your local documents and lets you chat with them using natural language.

![Demo](docs/demo.gif)

## Why ChatFiles?

- **Chat with any file** — PDFs, Word docs, spreadsheets, presentations, images, code, and more
- **Flexible LLM** — Works with any OpenAI-compatible API (Yunwu, OpenAI, Ollama, etc.)
- **Hybrid search** — Combines semantic (vector) search with keyword matching for accurate retrieval
- **Real-time indexing** — Watches your directories and auto-indexes new and changed files
- **Beautiful UI** — Modern dark-mode chat interface with file citations and source references
- **Privacy-first** — Your files stay on your machine. Use a local LLM (Ollama) for fully offline operation

## Quick Start

### Option 1: Docker (recommended)

```bash
git clone https://github.com/yoligehude14753/chatfiles.git
cd chatfiles
cp .env.example .env
# Edit .env — add your API key
docker compose up
```

Open [http://localhost:3000](http://localhost:3000)

### Option 2: Manual Setup

```bash
git clone https://github.com/yoligehude14753/chatfiles.git
cd chatfiles
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

### Prerequisites

- **Python 3.9+**
- **Node.js 18+** (for the web UI)
- One of the following LLM providers:
  - **Any OpenAI-compatible API** (e.g. [Yunwu](https://yunwu.ai), OpenRouter, etc.)
  - **OpenAI** directly
  - **Ollama** (fully local, no API key) — install from [ollama.com](https://ollama.com)

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
│   React/TS   │◀────│   Backend     │◀────│  (Yunwu/OpenAI/ │
└─────────────┘     └──────┬───────┘     │   Ollama/...)   │
                           │              └─────────────────┘
                    ┌──────┴───────┐
                    │   SQLite     │
                    │  + Vectors   │
                    └──────────────┘
```

- **Frontend**: React + TypeScript + Tailwind CSS
- **Backend**: FastAPI with OpenAI Responses API support
- **LLM**: Any OpenAI-compatible provider (Yunwu, OpenAI, Ollama, Claude, Kimi)
- **Embeddings**: text-embedding-3-small (default), Ollama, or local SentenceTransformers
- **Storage**: SQLite for metadata + numpy-powered vector similarity search
- **Parsing**: PyPDF2, python-docx, python-pptx, openpyxl, Pillow, BeautifulSoup

## Configuration

Copy `.env.example` to `.env` and customize:

```bash
# Use any OpenAI-compatible API
LLM_PROVIDER=yunwu
YUNWU_API_KEY=sk-your-key
YUNWU_BASE_URL=https://yunwu.ai/v1
YUNWU_MODEL=gpt-5.4-nano

# Or use Ollama (local, no API key)
LLM_PROVIDER=ollama
EMBEDDING_PROVIDER=ollama

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

## Roadmap

- [x] Chat interface with RAG (Retrieval-Augmented Generation)
- [x] OpenAI Responses API support (GPT-5.4-nano, GPT-5, etc.)
- [x] Ollama (local LLM) support
- [x] Hybrid search (vector + keyword)
- [x] File watcher (real-time indexing)
- [x] Multi-format parsers (PDF, DOCX, XLSX, PPTX, images, code)
- [x] Dark mode UI with i18n (English + Chinese)
- [ ] Slide-level search & export
- [ ] Plugin system for custom parsers
- [ ] Desktop app (Tauri)
- [ ] Voice input
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

**ChatFiles** is built with Python, React, and a lot of caffeine. If you find it useful, please give it a star!
