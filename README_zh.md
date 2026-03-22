# OpenFiles

> 开源 AI 本地文件助手。

**OpenFiles** 可以索引你的本地文档，让你用自然语言搜索和对话。支持任何 LLM，用 [Ollama](https://ollama.com) 完全本地运行。

## 为什么选择 OpenFiles？

传统文件搜索（Spotlight、Everything）只能匹配文件名和精确关键词。OpenFiles **理解文件内容**，找到你想要的（而不只是你输入的），还能带引用地回答后续问题。

- **语义搜索** — 输入"找我的 Q4 预算报告"，根据内容匹配，而不是文件名
- **带引用的问答** — 对文件提问，AI 回答时标注来源文件
- **灵活的 LLM** — 支持任何 OpenAI 兼容 API（Ollama、OpenAI、OpenRouter 等）
- **混合搜索** — 语义向量搜索 + 关键词匹配，检索更精准
- **实时索引** — 监控目录变化，自动索引新增和修改的文件
- **隐私优先** — 文件留在本地。用 Ollama 可以完全离线运行

## 快速开始

```bash
git clone https://github.com/yoligehude14753/openfiles.git
cd openfiles
cp .env.example .env
docker compose up
```

打开 [http://localhost:3000](http://localhost:3000)

### 手动安装

```bash
git clone https://github.com/yoligehude14753/openfiles.git
cd openfiles
./setup.sh
```

启动服务：

```bash
# 终端 1 - 后端
source venv/bin/activate
python main.py serve

# 终端 2 - 前端
cd frontend && npm run dev
```

## 配置

复制 `.env.example` 到 `.env` 并修改：

```bash
# 使用 Ollama（推荐，本地运行，无需 API Key）
LLM_PROVIDER=ollama
EMBEDDING_PROVIDER=ollama

# 或使用任意 OpenAI 兼容 API
LLM_PROVIDER=openai-compatible
OPENAI_COMPATIBLE_API_KEY=sk-你的密钥
OPENAI_COMPATIBLE_BASE_URL=https://api.example.com/v1
OPENAI_COMPATIBLE_MODEL=gpt-4o-mini
```

## CLI 命令

```bash
python main.py init          # 初始化数据库
python main.py index         # 索引所有配置的目录
python main.py reindex       # 清除旧数据，从头重建索引
python main.py search "..."  # 终端搜索
python main.py stats         # 查看统计信息
python main.py serve         # 启动 Web 服务
```

## 支持的文件类型

| 类别 | 格式 |
|------|------|
| 文档 | PDF, DOCX, DOC, TXT, RTF, Markdown |
| 表格 | XLSX, XLS, CSV |
| 演示文稿 | PPTX, PPT |
| 图片 | JPG, PNG, GIF, WebP, SVG, TIFF |
| 代码 | Python, JavaScript, TypeScript, Java, C/C++, HTML, CSS, JSON, YAML |

## 许可证

[MIT](LICENSE) — 随意使用。

---

如果你觉得有用，请给个 Star！
