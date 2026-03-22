# OpenFiles 发布文案（定稿）

> 发帖前先公开仓库：
> ```bash
> gh repo edit yoligehude14753/openfiles --visibility public --accept-visibility-change-consequences
> ```

---

## Hacker News

**地址**: https://news.ycombinator.com/submit

**Title**:
```
Show HN: OpenFiles – Voice-powered file search that runs locally (Tauri + FastAPI)
```

**URL**: https://github.com/yoligehude14753/openfiles

**Text**:
```
I built OpenFiles because I kept forgetting which file had what. "I know I had a Q4 strategy report somewhere..." — that kind of thing.

It's a macOS menubar app. Cmd+Shift+Space opens a Spotlight-style search window. Type a query, get instant results. Press Cmd+Enter for an AI-powered answer with file citations.

The part I'm most excited about: voice mode. Press Cmd+Shift+V, say "find my investment reports", and the AI searches your files and speaks the answer back. Under the hood it uses OpenAI's Realtime API with function calling — the AI decides when to search your files mid-conversation.

Technical details:
- Tauri v2 desktop app (11MB binary, 37MB RAM)
- Python FastAPI backend bundled as PyInstaller sidecar (28MB)
- SQLite for everything (metadata + 1536-dim vectors + chat history)
- Hybrid search: numpy cosine similarity + keyword matching
- 27 file types: PDF, DOCX, XLSX, PPTX, images, code, markdown
- WebSocket proxy for Realtime API (browser can't set auth headers)
- .dmg installer, 32MB total

Works with any OpenAI-compatible API. Fully local with Ollama.

Would love feedback on the voice UX and retrieval strategy.
```

**发帖时间**: 北京时间周二~周四晚 21:00-23:00

---

## Reddit r/selfhosted

**地址**: https://www.reddit.com/r/selfhosted/submit

**Title**:
```
OpenFiles: macOS menubar app that indexes your files and lets you search them by voice. Self-hosted, Cmd+Shift+Space.
```

**Text**:
```
Just shipped OpenFiles — a macOS menubar app for searching your local files.

How it works:
1. Indexes ~/Documents, ~/Desktop, ~/Downloads (PDF, Word, Excel, code, images — 27 types)
2. Cmd+Shift+Space opens a Spotlight-style floating window
3. Type a query → instant file results with similarity scores
4. Cmd+Enter → AI answers your question citing specific files
5. Cmd+Shift+V → voice mode: say your question, AI speaks the answer

Self-hosting highlights:
- Everything runs locally: Tauri app + Python FastAPI sidecar
- SQLite only — no Postgres, no Redis, no vector DB
- .dmg installer (32MB), double-click to install
- Works with any OpenAI-compatible API, or Ollama for fully offline

The voice mode uses OpenAI Realtime API with function calling. When you ask "where's my budget report?", the AI automatically searches your files mid-conversation and tells you what it found.

GitHub: https://github.com/yoligehude14753/openfiles
```

---

## Reddit r/LocalLLaMA

**地址**: https://www.reddit.com/r/LocalLLaMA/submit

**Title**:
```
OpenFiles: Voice-enabled RAG over your filesystem — Spotlight-style search with Realtime API function calling
```

**Text**:
```
Built a macOS desktop app that indexes your local files and lets you search + chat with them, including by voice.

Architecture:
- Tauri v2 (Rust) — 11MB binary, 37MB RAM, menubar resident
- Python FastAPI sidecar (PyInstaller) — handles indexing + search + chat
- SQLite: metadata + 1536-dim vectors (no ChromaDB/Pinecone)
- Hybrid retrieval: numpy cosine similarity (0.7 weight) + keyword matching (0.3)

Voice mode (the interesting part):
- Uses OpenAI Realtime API via WebSocket
- Registered `search_files` as a function tool
- AI decides when to call it during voice conversation
- Backend has a WebSocket proxy (browser can't set auth headers on WS)
- After function_call returns, response.create with modalities: ["text", "audio"] triggers voice reply

Supports 27 file types. Works with any OpenAI-compatible endpoint. Ollama for local.

Looking for feedback on:
1. Retrieval strategy — is numpy + keyword hybrid enough, or should I add reranking?
2. Voice UX — any ideas for making the voice interaction feel more natural?

GitHub: https://github.com/yoligehude14753/openfiles
```

---

## V2EX

**地址**: https://www.v2ex.com/new （节点: `share` 或 `create`）

**Title**:
```
OpenFiles：macOS 菜单栏应用，Cmd+Shift+Space 搜文件，还能语音对话找文件
```

**Text**:
```
做了一个 macOS 桌面应用，解决"记得内容但找不到文件"这个问题。

核心交互：
- 菜单栏常驻，Cmd+Shift+Space 呼出悬浮搜索框
- 输入关键词，200ms 内返回匹配文件（带相似度百分比）
- Cmd+Enter 让 AI 基于文件内容回答你的问题
- Cmd+Shift+V 进入语音模式：直接说话，AI 自动搜文件并语音回复

实测效果：
搜"春季行情 策略"，0.5 秒内第一个结果就是光大证券的策略报告（49% 匹配）。

技术栈：
- Tauri v2 桌面应用（11MB，37MB 内存）
- Python FastAPI 后端打包成 PyInstaller sidecar（28MB）
- SQLite 存一切（元数据 + 1536 维向量 + 对话历史）
- 混合搜索：numpy 余弦相似度 + 关键词匹配
- 语音：OpenAI Realtime API + function calling（AI 对话中自动搜文件）
- 支持 27 种文件格式
- .dmg 安装包，32MB，双击安装

支持任意 OpenAI 兼容 API，也可以用 Ollama 完全本地运行。

GitHub：https://github.com/yoligehude14753/openfiles

MIT 协议，欢迎 Star 和反馈。特别想听听大家对语音交互体验的看法。
```

---

## Twitter/X

**推文 1（主发布，配 demo.gif）**:
```
I built a voice-powered file search for macOS.

⌘⇧Space → type → instant results
⌘Enter → AI answers with file citations
⌘⇧V → just speak: "find my budget report"

The AI searches your files mid-conversation using function calling.

Tauri + FastAPI + SQLite. No cloud needed.

github.com/yoligehude14753/openfiles
```

**推文 2（技术 thread）**:
```
How voice file search works in OpenFiles:

1. User speaks → mic captures PCM16 → WebSocket to Realtime API
2. AI transcribes + understands intent
3. AI calls search_files() function automatically
4. Backend runs hybrid search (numpy vectors + keyword matching)
5. Results fed back to AI
6. AI speaks the answer with 14 audio chunks

The key insight: register your search as a "tool" in the Realtime API. The AI decides WHEN to search.
```

---

## 知乎

**标题**:
```
我做了一个能用语音搜文件的 macOS 应用（开源）
```

**正文**:
```
## 痛点

"我记得之前看过一份关于春季行情的策略报告，但忘了存在哪了。"

这种情况你有过吗？Spotlight 只能搜文件名，搜不到内容。

## 解决方案

我做了 OpenFiles，一个 macOS 菜单栏应用：

1. 后台自动索引你的 Documents/Desktop/Downloads
2. Cmd+Shift+Space 呼出搜索框，输入"春季行情 策略"
3. 0.5 秒出结果——第一个就是光大证券的策略报告

更酷的是语音模式：按 Cmd+Shift+V，说"帮我找投资策略报告"，AI 会自动搜索你的文件，然后用语音告诉你找到了什么。

## 技术实现

语音模式用的是 OpenAI Realtime API 的 function calling。我把"搜索文件"注册成了一个 tool，AI 在语音对话过程中会自主决定什么时候调用搜索。这意味着你不需要先搜再问——直接对话就行。

全栈：Tauri v2（11MB） + Python FastAPI sidecar（28MB） + SQLite + numpy 向量搜索

搜索用的是混合策略：70% 语义向量匹配 + 30% 关键词匹配，12000 个文件搜索秒级返回。

GitHub：https://github.com/yoligehude14753/openfiles

MIT 协议，完全免费开源。.dmg 双击安装，32MB。
```

---

## 发布节奏

| 时间 | 平台 | 核心角度 |
|------|------|---------|
| Day 1 晚 9 点 | Hacker News | "voice-powered file search with function calling" |
| Day 1 同时 | Reddit r/selfhosted | "menubar app, .dmg, no cloud" |
| Day 1 同时 | Reddit r/LocalLLaMA | "Realtime API + function calling architecture" |
| Day 1 同时 | V2EX | "语音搜文件" |
| Day 2 | Twitter 推文 1 | demo.gif |
| Day 3 | Twitter 推文 2 | 技术 thread |
| Day 5 | 知乎 | 长文讲故事 |
| Week 2 | Product Hunt | 等有 Star 基础 |
