# ChatFiles 发布文案（各平台定稿）

> 发帖前：先把仓库改为 public
> ```bash
> gh repo edit yoligehude14753/chatfiles --visibility public --accept-visibility-change-consequences
> ```

---

## 1. Hacker News（Show HN）

**发帖地址**: https://news.ycombinator.com/submit

**标题**:
```
Show HN: ChatFiles – Open-source RAG file assistant (FastAPI + React, any LLM)
```

**正文（URL 栏填 GitHub 链接，text 栏填以下内容）**:

```
I built ChatFiles, an open-source AI file assistant that indexes your local documents and lets you chat with them.

It works like a personal ChatGPT that actually knows what's in your files — PDFs, Word docs, spreadsheets, presentations, images, code, markdown, and more (27 file types).

How it works:
1. Point it at your directories (Documents, Desktop, etc.)
2. It parses and indexes everything with vector embeddings
3. Ask questions in natural language → get answers with file citations

Key technical decisions:
- Hybrid search: numpy-based vector similarity + keyword BM25 scoring
- OpenAI Responses API for chat (works with any OpenAI-compatible endpoint)
- SQLite for everything (metadata + vectors), no external DB needed
- FastAPI backend with streaming WebSocket
- React + TypeScript + Tailwind frontend
- File watcher (watchdog) for real-time re-indexing

Supports any OpenAI-compatible LLM provider (Yunwu, OpenRouter, OpenAI, Ollama for local).

Stack: Python 3.9+, FastAPI, React/TS, SQLite, numpy, Docker Compose

GitHub: https://github.com/yoligehude14753/chatfiles
```

**最佳发帖时间**: 美国东部时间周二~周四上午 9-11 点（北京时间 21:00-23:00）

---

## 2. Reddit r/selfhosted

**发帖地址**: https://www.reddit.com/r/selfhosted/submit

**标题**:
```
ChatFiles: self-hosted AI file assistant. Index your docs, chat with them. Docker one-command setup.
```

**正文**:

```
Just released ChatFiles — an open-source alternative to cloud-based document AI tools.

What it does:
- Indexes your local files: PDF, DOCX, XLSX, PPTX, images, code, markdown (27 types)
- Chat interface with RAG (retrieval-augmented generation)
- Answers your questions with file citations — shows which files the answer came from
- Hybrid search: semantic vectors + keyword matching

Self-hosting highlights:
- `docker compose up` and you're running
- SQLite-based, no external database needed
- Works with any OpenAI-compatible API, or use Ollama for fully local/offline operation
- All data stays on your machine
- React frontend with dark mode

Tech stack: Python/FastAPI, React/TypeScript/Tailwind, SQLite + numpy vectors

GitHub: https://github.com/yoligehude14753/chatfiles

Happy to answer any questions!
```

---

## 3. Reddit r/LocalLLaMA

**发帖地址**: https://www.reddit.com/r/LocalLLaMA/submit

**标题**:
```
ChatFiles: open-source RAG over your filesystem — works with Ollama, OpenAI, or any compatible API
```

**正文**:

```
I built a local RAG system that indexes your filesystem and lets you chat with your files.

LLM setup:
- Works with any OpenAI-compatible endpoint (tested with GPT-5.4-nano, Gemini 2.5 Flash)
- Ollama support for fully local operation (llama3.2 + nomic-embed-text)
- Embeddings via text-embedding-3-small or Ollama
- Hybrid retrieval: numpy vector similarity + keyword BM25

What it indexes:
- PDF, DOCX, XLSX, PPTX, images, code files, markdown, CSV, HTML (27 types total)
- Uses LLM to summarize each file, then embeds the summary for semantic search
- File watcher auto-indexes new/changed files

The chat engine:
1. Rewrites your question based on conversation history
2. Retrieves top-k relevant files via hybrid search
3. Assembles context from file summaries
4. Streams response with source citations

FastAPI backend, React frontend, Docker Compose setup included.

GitHub: https://github.com/yoligehude14753/chatfiles

Feedback welcome — especially on retrieval strategy and embedding model choices.
```

---

## 4. Twitter/X 发布推文

**推文 1（主发布，配 demo.gif）**:

```
Introducing ChatFiles 🔍

Open-source AI file assistant:
→ Index PDFs, docs, spreadsheets, code, images (27 types)
→ Chat with your files using RAG
→ Hybrid search: vector + keyword
→ Any LLM: OpenAI, Ollama, Gemini...
→ Beautiful dark mode UI

docker compose up → done.

github.com/yoligehude14753/chatfiles
```

**推文 2（第二天，技术细节）**:

```
How ChatFiles search works:

1. Files → parse → LLM summarize → embed (1536-dim)
2. Query → embed → numpy cosine similarity
3. + keyword BM25 scoring
4. Merge with 0.7/0.3 weights
5. Top-k results → LLM generates answer with citations

All in SQLite. No Pinecone, no Chroma, no Weaviate.

Just numpy + SQLite.
```

**推文 3（第三天，配 screenshot_chat.png）**:

```
ChatFiles RAG in action:

"帮我总结投资策略报告"
→ Finds matching PDFs automatically
→ Summarizes key findings from each report
→ Cites specific files

All running locally with your own files.
```

---

## 5. V2EX

**发帖地址**: https://www.v2ex.com/new （节点选 `share` 或 `create`）

**标题**:
```
ChatFiles：开源本地 AI 文件助手，索引你电脑里的一切，用自然语言对话
```

**正文**:

```
做了一个开源项目 ChatFiles，核心功能是索引你本地的文件，然后通过聊天的方式问答。

功能：
- 支持 27 种文件格式：PDF、Word、Excel、PPT、图片、代码、Markdown 等
- RAG 对话：问问题时自动检索相关文件，基于文件内容生成回答，带来源引用
- 混合搜索：向量语义搜索 + 关键词匹配
- 实时监控：文件变化自动重新索引

技术栈：
- 后端：Python + FastAPI + SQLite（元数据+向量全部存 SQLite，没用额外数据库）
- 前端：React + TypeScript + Tailwind CSS，暗色主题
- LLM：支持任何 OpenAI 兼容 API（云雾、OpenAI、Ollama 等）
- 向量计算：numpy 批量余弦相似度，12000 个文件搜索秒级返回
- 部署：docker compose up 一键启动

实测效果：
- 索引了 ~/Documents + ~/Desktop + ~/Downloads 下 12000+ 个文件
- 问"帮我总结投资策略报告"，秒级返回光大证券、东吴证券等多份报告的结构化总结
- 前后端分离，支持中英双语切换

GitHub：https://github.com/yoligehude14753/chatfiles

MIT 协议，欢迎 Star 和 PR。

有什么建议或者想要的功能欢迎留言。
```

---

## 6. 知乎文章

**标题**:
```
我开源了一个本地 AI 文件助手：索引 PDF、Word、Excel、代码，直接对话
```

**正文**:

```
## 为什么做这个

电脑里文件越来越多，经常记得内容但找不到在哪个文件里。现有的搜索要么只能搜文件名，要么需要把文件上传到云端。

我想要的是：不上传任何文件，在本地就能用自然语言搜索和问答。

所以做了 ChatFiles。

## 它能做什么

把你电脑上的文件（PDF、Word、Excel、PPT、图片、代码、Markdown 等 27 种格式）全部索引，然后你可以用聊天的方式提问，比如：

- "帮我找关于投资策略的报告"
- "总结一下最近的会议纪要"
- "哪些表格里有预算数据"

它会自动检索相关文件，基于文件内容生成回答，并告诉你答案来自哪个文件。

## 技术实现

- **搜索**：混合搜索 = 向量语义搜索（numpy 余弦相似度） + 关键词 BM25 匹配
- **对话**：RAG（检索增强生成）— 先搜文件，再让 LLM 基于搜索结果回答
- **后端**：Python + FastAPI，支持 WebSocket 流式输出
- **前端**：React + TypeScript + Tailwind CSS，暗色主题，中英双语
- **存储**：SQLite 一个文件搞定（元数据+向量+对话历史）
- **LLM**：支持任何 OpenAI 兼容 API，也可以用 Ollama 完全本地运行

实测 12000+ 个文件，搜索秒级返回。

## 快速开始

```bash
git clone https://github.com/yoligehude14753/chatfiles
cd chatfiles
cp .env.example .env  # 填入你的 API Key
docker compose up
```

打开 http://localhost:3000 就能用了。

GitHub：https://github.com/yoligehude14753/chatfiles

MIT 协议，完全免费开源。欢迎 Star。
```

---

## 发布节奏建议

| 时间 | 平台 | 备注 |
|------|------|------|
| Day 1 晚 9 点 | Hacker News | 对应美东上午，流量最大 |
| Day 1 同时 | Reddit r/selfhosted + r/LocalLLaMA | 同一天铺开 |
| Day 1 同时 | V2EX | 中文社区 |
| Day 2 | Twitter/X 推文 1 | 配 demo.gif |
| Day 3 | Twitter/X 推文 2 | 技术细节 |
| Day 4 | 知乎文章 | 长文，讲故事 |
| Day 5 | Twitter/X 推文 3 | 配截图 |
| Week 2 | Product Hunt | 等积累一些 Star 后 |
