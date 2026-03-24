# OpenFiles 发布文案（可直接复制发帖）

GitHub: https://github.com/yoligehude14753/openfiles

---

## Hacker News

**地址**: https://news.ycombinator.com/submit

**Title**:
```
Show HN: OpenFiles – local RAG file assistant with hybrid search (Ollama + FastAPI)
```

**URL**: `https://github.com/yoligehude14753/openfiles`

**Text**:
```
I built OpenFiles because I kept forgetting which file had what.

"I know I wrote about Q4 strategy somewhere..." — Spotlight can't help because it only searches filenames.

OpenFiles indexes your local files and lets you search by meaning:

- Type "find my Q4 budget report" → it finds the right PDF by understanding the content
- Ask a follow-up question → get an AI answer with citations to specific files
- All runs locally with Ollama — no API keys, nothing leaves your machine

Technical stack:
- FastAPI backend, React/TypeScript frontend
- SQLite for everything: metadata, 1536-dim vectors, chat history
- Hybrid search: numpy cosine similarity (70%) + keyword matching (30%)
- 27 file parsers: PDF, DOCX, XLSX, PPTX, images, code, markdown
- Real-time file watcher — auto-indexes new and changed files
- Docker Compose: `docker compose up` and you're running

No ChromaDB, no Pinecone, no Postgres, no Redis. Just SQLite + numpy.

I specifically designed it as a general-purpose file assistant, not just "chat with one PDF". It watches your directories and keeps the index fresh.

Also supports OpenAI/Claude if you want cloud models, but Ollama is the default.

Would love feedback on the retrieval strategy and UX.
```

**发帖时间**: 北京时间周二~周四晚 21:00-23:00（美西早上 6-8 点）

---

## Reddit r/selfhosted

**地址**: https://www.reddit.com/r/selfhosted/submit

**Title**:
```
OpenFiles: self-hosted AI file search. docker compose up, no cloud, no API keys.
```

**Text**:
```
Just open-sourced OpenFiles — an AI file assistant that runs entirely on your machine.

What it does:
1. Indexes your local files (PDF, Word, Excel, code, images — 27 types)
2. Search by meaning, not just filename ("find my Q4 budget report")
3. Chat with your files — AI answers with citations to specific documents
4. Real-time: watches your directories, auto-indexes new/changed files

Self-hosting highlights:
- Default LLM: Ollama (llama3.2 + nomic-embed-text) — no API keys needed
- Storage: SQLite only — no Postgres, no Redis, no vector DB
- Setup: `docker compose up` (backend + frontend + Ollama, all included)
- Also supports OpenAI/Claude if you prefer cloud models

The hybrid search (70% semantic vectors + 30% keyword matching) is surprisingly accurate for a SQLite + numpy setup.

GitHub: https://github.com/yoligehude14753/openfiles

MIT license. Feedback welcome.
```

---

## Reddit r/LocalLLaMA

**地址**: https://www.reddit.com/r/LocalLLaMA/submit

**Title**:
```
OpenFiles: local RAG over your filesystem with Ollama — hybrid search, no vector DB needed
```

**Text**:
```
Built an open-source file assistant that indexes your local documents and lets you search + chat with them using Ollama.

Architecture:
- llama3.2 for chat, nomic-embed-text for embeddings (configurable)
- SQLite stores everything: file metadata + 1536-dim vectors + chat history
- Hybrid retrieval: numpy cosine similarity (0.7 weight) + keyword matching (0.3)
- No ChromaDB, no Pinecone, no FAISS — just numpy on raw vectors in SQLite
- FastAPI backend with streaming WebSocket chat
- React frontend with dark mode

The retrieval pipeline:
1. User query → embed with nomic-embed-text
2. numpy cosine similarity against stored file embeddings → top-K candidates
3. Keyword score against file summaries/keywords → merge with vector results
4. RAG: feed top results as context to llama3.2 → generate answer with citations

Supports 27 file types. File watcher auto-indexes changes. Docker Compose setup included.

Looking for feedback on:
1. Is numpy + keyword hybrid enough, or should I add reranking (e.g., bge-reranker)?
2. Currently embedding entire file summaries — would chunking improve recall?

GitHub: https://github.com/yoligehude14753/openfiles
```

---

## V2EX

**地址**: https://www.v2ex.com/new （节点: `share` 或 `create`）

**Title**:
```
OpenFiles：开源 AI 文件助手，用自然语言搜文件内容，Ollama 本地运行
```

**Text**:
```
做了一个开源工具，解决"记得内容但找不到文件"的问题。

核心功能：
- 索引本地文件（PDF、Word、Excel、代码、图片等 27 种格式）
- 输入自然语言搜索，按内容匹配而不是文件名
- 对文件提问，AI 带引用回答（"在 report.pdf 第3页中..."）
- 实时监控目录变化，自动索引新文件

技术栈：
- 后端：Python FastAPI
- 前端：React + TypeScript + Tailwind
- 存储：SQLite 存一切（元数据 + 1536 维向量 + 对话历史）
- 搜索：混合检索，70% 语义向量（numpy 余弦相似度）+ 30% 关键词匹配
- LLM：默认用 Ollama（llama3.2 + nomic-embed-text），无需 API Key
- 也支持 OpenAI / Claude 等云端模型

一条命令启动：
docker compose up

没有用 ChromaDB、Pinecone 这些，纯 SQLite + numpy 就够了。

GitHub：https://github.com/yoligehude14753/openfiles

MIT 协议，欢迎 Star 和反馈。
```

---

## Twitter/X

**推文 1（主发布，配 demo.gif）**:
```
I open-sourced OpenFiles — an AI file assistant that actually understands your files.

Search by meaning, not filenames.
Chat with your files, get answers with citations.
Runs 100% locally with Ollama.

SQLite + numpy vectors. No cloud, no vector DB.

docker compose up

github.com/yoligehude14753/openfiles
```

**推文 2（技术 thread）**:
```
How OpenFiles searches 10K+ files in under a second with just SQLite + numpy:

1. Index: parse file → LLM summarizes → embed summary → store 1536-dim vector in SQLite
2. Search: embed query → numpy cosine similarity against all vectors
3. Hybrid: merge vector scores (70%) with keyword scores (30%)
4. RAG: top results as context → LLM generates answer with citations

No vector database. No Postgres. No Redis. Just SQLite + numpy.

That's the whole stack.
```

**推文 3（痛点共鸣）**:
```
"I know I had a report about Q4 strategy somewhere..."

Spotlight: 0 results (because you searched content, not the filename)

OpenFiles: finds it instantly by understanding what's inside your files.

Open-source, runs locally, no API keys needed.

github.com/yoligehude14753/openfiles
```

---

## 知乎

**标题**:
```
我做了一个开源 AI 文件助手：按内容搜文件，不只是搜文件名
```

**正文**:
```
## 痛点

"我记得之前看过一份关于 Q4 策略的报告，但忘了存在哪了。"

这种情况你有过吗？

macOS 的 Spotlight 和 Windows 的 Everything 都只能搜文件名。如果你记得的是文件内容而不是文件名，它们帮不了你。

## 我做了什么

OpenFiles 是一个开源的 AI 文件助手。它索引你的本地文件，让你用自然语言搜索文件内容。

比如输入"找我的 Q4 预算报告"，它不是去匹配文件名里有没有"Q4"这几个字，而是理解你要找的东西，然后在所有已索引文件的内容中做语义匹配。

找到之后还能继续问："这份报告的核心结论是什么？"——AI 会带引用地回答你。

## 技术实现

搜索用的是混合检索：70% 语义向量匹配 + 30% 关键词匹配。

向量部分：用 Ollama 的 nomic-embed-text 生成 1536 维 embedding，存在 SQLite 里，搜索时用 numpy 做余弦相似度计算。

没有用 ChromaDB、Pinecone 这些向量数据库。纯 SQLite + numpy 在万级文件规模下表现够用，而且部署简单得多。

LLM 部分：默认用 Ollama 的 llama3.2，完全本地运行，不需要任何 API Key，文件数据不出本机。也支持 OpenAI、Claude 等云端模型。

全栈：Python FastAPI 后端 + React TypeScript 前端 + SQLite 存储。

支持 27 种文件格式：PDF、Word、Excel、PPT、图片、各种代码文件。

一条命令启动：docker compose up

## 开源

GitHub：https://github.com/yoligehude14753/openfiles

MIT 协议，完全免费。欢迎 Star，也欢迎反馈和贡献。
```

---

## Product Hunt

**Tagline**: `Search your files by meaning, not filenames. Open-source, runs locally.`

**Description**:
```
OpenFiles is an open-source AI file assistant that indexes your local documents and lets you search them by meaning — not just filenames.

Type "find my Q4 budget report" and OpenFiles finds the right PDF by understanding its content. Then ask follow-up questions and get AI answers citing specific files.

Key features:
- Hybrid search: 70% semantic + 30% keyword matching
- 27 file types: PDFs, Word, Excel, PowerPoint, images, code
- Runs locally with Ollama — no API keys, no cloud
- Real-time indexing: file watcher auto-indexes changes
- Docker Compose: one command to run

Built with FastAPI, React, SQLite, and numpy. No external vector database needed.
```

**Topics**: `Open Source`, `Artificial Intelligence`, `Developer Tools`, `Privacy`, `Productivity`

---

## 发布节奏

| 时间 | 平台 | 操作 |
|------|------|------|
| Day 1 晚 9 点 | Hacker News | 发帖（需要 demo.gif 就绪） |
| Day 1 同时 | Reddit r/selfhosted | 发帖 |
| Day 1 同时 | Reddit r/LocalLLaMA | 发帖 |
| Day 1 + 30min | V2EX | 发帖 |
| Day 2 | Twitter 推文 1 | 配 demo.gif |
| Day 3 | Twitter 推文 2 | 技术 thread |
| Day 3 | Twitter 推文 3 | 痛点共鸣 |
| Day 5 | 知乎 | 长文 |
| Week 2 | Product Hunt | 等有 Star 基础再上 |

## 发帖前检查

- [ ] demo.gif 已录制并放到 `docs/assets/demo.gif`
- [ ] `docker compose up` 在新 clone 上测试通过
- [ ] 3 张截图已准备：搜索结果、聊天引用、设置页
- [ ] GitHub 链接可访问：https://github.com/yoligehude14753/openfiles
- [ ] README 的 demo.gif 正常显示
