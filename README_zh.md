<p align="center">
  <h1 align="center">OpenFiles</h1>
  <p align="center">
    <strong>开源 AI 本地文件助手</strong><br>
    按语义搜索，带引用问答，用 Ollama 完全本地运行。
  </p>
  <p align="center">
    <a href="https://github.com/yoligehude14753/openfiles/stargazers"><img src="https://img.shields.io/github/stars/yoligehude14753/openfiles?style=social" alt="Stars"></a>
    <a href="https://github.com/yoligehude14753/openfiles/blob/main/LICENSE"><img src="https://img.shields.io/github/license/yoligehude14753/openfiles" alt="License"></a>
    <a href="https://github.com/yoligehude14753/openfiles/actions"><img src="https://img.shields.io/github/actions/workflow/status/yoligehude14753/openfiles/ci.yml?branch=main" alt="CI"></a>
    <img src="https://img.shields.io/badge/python-3.9+-blue" alt="Python">
  </p>
  <p align="center">
    <a href="https://github.com/yoligehude14753/openfiles/releases/latest"><strong>下载 .dmg</strong></a> &middot;
    <a href="#快速开始">快速开始</a> &middot;
    <a href="#核心功能">核心功能</a> &middot;
    <a href="#工作原理">工作原理</a> &middot;
    <a href="README.md">English</a>
  </p>
</p>

<p align="center">
  <img src="docs/assets/demo.gif" alt="OpenFiles 演示 — 按语义搜索文件，带引用的 AI 问答" width="720">
</p>

> **Spotlight 搜文件名，OpenFiles 搜内容。**
>
> 输入「找我的 Q4 预算报告」—— OpenFiles 通过理解文件内容找到正确的 PDF，然后回答你的追问，并标注引用来源。

## 快速开始

### 方式一：macOS 桌面应用（推荐）

1. 安装 [Ollama](https://ollama.com) 并拉取模型：

```bash
ollama pull qwen3-vl:8b
ollama pull EntropyYue/jina-embeddings-v2-base-zh
```

2. 下载安装 [OpenFiles.dmg](https://github.com/yoligehude14753/openfiles/releases/latest)

3. 从应用中打开 OpenFiles，按 `Cmd+Shift+Space` 开始搜索

完成。文件自动索引，一切本地运行，无需 API Key。

### 方式二：Docker

```bash
git clone https://github.com/yoligehude14753/openfiles.git
cd openfiles
cp .env.example .env
docker compose up
```

打开 [http://localhost:3000](http://localhost:3000)，开始搜索。

## 核心功能

| | |
|---|---|
| **语义搜索** | 描述你要找的东西，OpenFiles 按内容匹配文件，不只是匹配文件名。 |
| **带引用的问答** | 对文件提问，AI 回答时标注具体来源文件。 |
| **27 种文件格式** | PDF、Word、Excel、PPT、图片、代码、Markdown 等。 |
| **混合检索** | 70% 语义向量 + 30% 关键词匹配，更精准。 |
| **实时索引** | 文件监控自动索引新增和修改的文件。 |
| **任意 LLM** | Ollama（本地）、OpenAI、Claude，或任何 OpenAI 兼容 API。 |
| **隐私优先** | 文件留在本地。仅用 SQLite —— 不需要 Postgres、Redis、向量数据库。 |

## 工作原理

```
  "找我的 Q4 预算报告"
            │
            ▼
   ┌─────────────────┐
   │   混合搜索        │  70% 语义 + 30% 关键词
   │  (numpy + SQL)   │
   └────────┬────────┘
            │
   ┌────────▼────────┐
   │   RAG 引擎       │  检索相关片段
   │  + LLM (Ollama)  │  生成带引用的回答
   └────────┬────────┘
            │
            ▼
   "在 Q4-Strategy.pdf (第3页) 中找到：
    营收同比增长 23%..."
```

**技术栈：** Python/FastAPI 后端，React/TypeScript 前端，SQLite + numpy 向量，Ollama。

## 使用场景

**"记得内容，忘了文件名"**
> 用自然语言描述你要找的东西。OpenFiles 通过理解文件内容来匹配结果。

**"把多个文件的要点总结一下"**
> 提一个跨多文档的问题，得到一个带引用的综合回答。

**"这个概念在代码里哪里出现过？"**
> 对代码、文档、配置文件做语义搜索 —— 不只是 grep。

## 支持的文件类型

| 类别 | 格式 |
|------|------|
| 文档 | PDF, DOCX, DOC, TXT, RTF, Markdown |
| 表格 | XLSX, XLS, CSV |
| 演示文稿 | PPTX, PPT |
| 图片 | JPG, PNG, GIF, WebP, SVG, TIFF |
| 代码 | Python, JavaScript, TypeScript, Java, C/C++, HTML, CSS, JSON, YAML |

## 配置

```bash
# 默认：Ollama（本地运行，无需 API Key）
LLM_PROVIDER=ollama
EMBEDDING_PROVIDER=ollama

# 或使用任意 OpenAI 兼容 API
LLM_PROVIDER=openai-compatible
OPENAI_COMPATIBLE_API_KEY=sk-你的密钥
OPENAI_COMPATIBLE_BASE_URL=https://api.example.com/v1

# 要索引的目录
SCAN_DIRECTORIES=~/Documents,~/Desktop,~/Downloads
```

完整选项见 [.env.example](.env.example)。

## CLI 命令

```bash
python main.py init          # 初始化数据库
python main.py index         # 索引配置的目录
python main.py search "..."  # 终端搜索
python main.py serve         # 启动 Web 服务
```

## API

REST + WebSocket API，带 [Swagger UI](http://localhost:8000/docs)：

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/v1/search` | POST | 语义文件搜索 |
| `/api/v1/chat` | POST | 发送聊天消息 |
| `/api/v1/chat/stream` | WS | 流式聊天响应 |
| `/api/v1/files` | GET | 列出已索引文件 |
| `/api/v1/index` | POST | 触发索引 |
| `/api/v1/stats` | GET | 查看统计 |

## 手动安装

```bash
git clone https://github.com/yoligehude14753/openfiles.git && cd openfiles
./setup.sh

# 终端 1 — 后端
source venv/bin/activate && python main.py serve

# 终端 2 — 前端
cd frontend && npm run dev
```

**前置条件：** Python 3.9+，Node.js 18+，[Ollama](https://ollama.com)（推荐）

## 路线图

- [x] RAG 问答 + 文件引用
- [x] 混合搜索（向量 + 关键词）
- [x] 实时文件监控
- [x] 27 种文件格式解析
- [x] Ollama / OpenAI / Claude 支持
- [x] 暗色模式 + 国际化（中/英）
- [ ] 语音输入（OpenAI Realtime API）
- [ ] 桌面应用（Tauri）Spotlight 式交互
- [ ] 插件系统：自定义解析器
- [ ] 多用户支持

## 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可证

[MIT](LICENSE)

---

<p align="center">
  如果 OpenFiles 对你有帮助，请给一个 <a href="https://github.com/yoligehude14753/openfiles">Star</a>。
</p>
