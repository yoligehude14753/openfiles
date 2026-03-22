# OpenFiles Launch Plan

## Positioning

**One-liner**: "Open-source AI file assistant — search, understand, and chat with your local files. Runs locally with Ollama."

**Technical angle** (Hacker News): "Show HN: OpenFiles — local RAG over your filesystem with Ollama, FastAPI, and React"

**Self-hosting angle** (r/selfhosted): "OpenFiles: self-hosted AI file search. No cloud, no API keys, just Ollama + Docker."

**Privacy angle**: "Your files never leave your machine. OpenFiles indexes locally and uses Ollama for zero-cloud AI search."

---

## Hacker News Post

**Title**: Show HN: OpenFiles – Search and chat with your local files using Ollama (open source)

**Body**:

Hi HN, I built OpenFiles — an open-source AI file assistant that indexes your local documents and lets you search and chat with them.

Key features:
- Uses Ollama by default (no API keys needed, nothing sent to the cloud)
- Indexes PDFs, Word docs, spreadsheets, presentations, images, code
- Hybrid search: vector embeddings + keyword matching
- FastAPI backend with streaming WebSocket responses
- React frontend with dark mode
- Docker Compose one-command setup

Stack: Python/FastAPI, React/TypeScript/Tailwind, SQLite + numpy vectors, Ollama

The main difference from similar tools: OpenFiles is designed as a general-purpose local file assistant, not just for a specific document type. It watches your directories and auto-indexes changes.

GitHub: [link]
Demo: [screenshot/gif]

---

## Reddit r/selfhosted Post

**Title**: OpenFiles - Self-hosted AI file assistant. Index your docs, chat with them. No cloud needed.

**Body**:

Just released OpenFiles, an open-source alternative to cloud-based document AI tools.

- Docker Compose setup (backend + frontend + Ollama)
- Indexes: PDF, DOCX, XLSX, PPTX, images, code, markdown
- Chat interface with file citations
- Completely local — uses Ollama, no API keys required
- Also supports OpenAI/Claude if you prefer

`docker compose up` and you're running.

GitHub: [link]

---

## Reddit r/LocalLLaMA Post

**Title**: OpenFiles: RAG-powered file search using Ollama locally

**Body**:

Built a local RAG system that indexes your filesystem and lets you chat with your files using Ollama.

Uses nomic-embed-text for embeddings and llama3.2 for chat. Hybrid retrieval (vector + keyword). Supports PDFs, spreadsheets, presentations, code files, and images (with llava).

FastAPI backend, React frontend, Docker setup included.

GitHub: [link]

---

## Product Hunt

**Tagline**: Search, understand, and chat with your local files.

**Description**: OpenFiles is an open-source AI file assistant that indexes your local documents (PDFs, Word, Excel, PowerPoint, images, code) and lets you ask questions about them in a beautiful chat interface. Powered by Ollama for 100% local operation — no API keys, no cloud, no data leaks.

**Topics**: Open Source, Artificial Intelligence, Developer Tools, Privacy, Productivity

---

## Social Media (Twitter/X)

**Launch tweet**:

Introducing OpenFiles — search, understand, and chat with your files, 100% locally.

Open-source AI file assistant:
- Indexes PDFs, docs, spreadsheets, code, images
- Runs with Ollama (no API keys)
- Hybrid search: vector + keyword
- Beautiful dark mode UI

docker compose up and you're running.

github.com/...

---

## Demo Scenarios

1. **Quick search**: "Find my Q4 budget report" -> shows matching PDF with summary
2. **Summarization**: "Summarize the main points from my project proposal" -> RAG-powered summary with citations
3. **Cross-file Q&A**: "Which spreadsheets contain revenue data?" -> finds multiple matching XLSX files
4. **Code search**: "Where is the authentication logic?" -> finds relevant Python/JS files

## Key Screenshots Needed

1. Welcome screen (clean, inviting)
2. Chat conversation with file citations
3. File browser with type filters
4. Settings panel showing Ollama connected
5. Terminal showing `docker compose up` starting successfully
