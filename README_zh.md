# ChatFiles

> 与你的文件对话。本地运行。隐私优先。

**ChatFiles** 是一个开源的 AI 文件助手，它可以索引你的本地文档，让你用自然语言与它们对话。

## 为什么选择 ChatFiles？

- **与任何文件对话** — PDF、Word、表格、PPT、图片、代码等
- **灵活的 LLM** — 支持任何 OpenAI 兼容 API（云雾、OpenAI、Ollama 等）
- **混合搜索** — 语义向量搜索 + 关键词匹配，检索更精准
- **实时索引** — 监控目录变化，自动索引新增和修改的文件
- **精美界面** — 现代暗色主题聊天界面，带文件引用和来源显示
- **隐私优先** — 文件留在本地。用 Ollama 可以完全离线运行

## 快速开始

### Docker（推荐）

```bash
git clone https://github.com/yoligehude14753/chatfiles.git
cd chatfiles
cp .env.example .env
# 编辑 .env，填入你的 API Key
docker compose up
```

打开 [http://localhost:3000](http://localhost:3000)

### 手动安装

```bash
git clone https://github.com/yoligehude14753/chatfiles.git
cd chatfiles
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
# 使用云雾 API（推荐，支持 GPT-5/Gemini 等模型）
LLM_PROVIDER=yunwu
YUNWU_API_KEY=sk-你的密钥
YUNWU_MODEL=gpt-5.4-nano

# 或使用 Ollama（本地运行，无需 API Key）
LLM_PROVIDER=ollama
EMBEDDING_PROVIDER=ollama
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
