# OpenFiles Launch Plan

## Core Positioning

**What it is:** Open-source AI file assistant — search by meaning, chat with citations, 100% local.

**Why it matters:** Everyone has files they can't find. Spotlight/Everything only match filenames. OpenFiles understands what's *inside* your files.

**Key differentiator:** General-purpose local file assistant with hybrid search (semantic + keyword), not just "chat with one PDF".

## Angles by Platform

| Platform | Angle | Hook |
|----------|-------|------|
| Hacker News | Technical simplicity | "SQLite + numpy vectors, no ChromaDB/Pinecone" |
| r/selfhosted | Zero dependencies | "docker compose up, no cloud, no API keys" |
| r/LocalLLaMA | Ollama-native RAG | "llama3.2 + nomic-embed-text, hybrid retrieval" |
| V2EX | Pain point | "记得内容忘了文件名" |
| Twitter/X | Visual demo | GIF showing search -> chat -> citation |
| Product Hunt | Product story | "Your files, searchable by meaning" |

## What's Shipped (safe to claim)

- Web UI with semantic search and RAG chat
- 27 file type parsers
- Hybrid search (70% vector + 30% keyword)
- Real-time file watcher
- Ollama / OpenAI / Claude support
- Docker Compose one-command setup
- CLI tools
- Dark mode + i18n (EN/中文)

## What's In Development (mention as roadmap only)

- Voice input (OpenAI Realtime API)
- Desktop app (Tauri) with Spotlight-style UX
- Plugin system for custom parsers

## Pre-launch Checklist

- [ ] Record demo.gif (10-15s: query -> results -> chat -> citation)
- [ ] Place demo.gif in `docs/assets/demo.gif`
- [ ] Verify `docker compose up` works clean on a fresh clone
- [ ] Take 3 screenshots: search results, chat with citations, settings page
- [ ] Test GitHub URL works: https://github.com/yoligehude14753/openfiles

## Launch Timing

Best times (in US Pacific / Beijing):
- **Hacker News**: Tuesday-Thursday, 6-8am PT / 21:00-23:00 Beijing
- **Reddit**: Same day, post within 1 hour of HN
- **Twitter**: Next day, with demo.gif
- **Product Hunt**: Week 2, after initial star momentum
