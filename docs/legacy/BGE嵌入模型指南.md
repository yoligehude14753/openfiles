# BGE 本地嵌入模型使用指南

## 什么是 BGE？

BGE (BAAI General Embedding) 是由智源研究院开发的高质量中英文双语嵌入模型，特别适合中文场景。

## 优势

✅ **完全免费** - 无 API 调用费用
✅ **本地运行** - 数据不离开本地，隐私安全
✅ **中文优化** - 在中文任务上表现优异
✅ **无需网络** - 离线也能使用
✅ **高性能** - 在多个中文评测榜单上名列前茅

## 支持的模型

### BGE 系列（推荐）

| 模型 | 维度 | 大小 | 适用场景 |
|------|------|------|---------|
| BAAI/bge-small-zh-v1.5 | 512 | ~100MB | 快速、轻量（推荐） |
| BAAI/bge-base-zh-v1.5 | 768 | ~400MB | 平衡性能和速度 |
| BAAI/bge-large-zh-v1.5 | 1024 | ~1.3GB | 最高质量 |

### 其他开源模型

- **text2vec-chinese**: 中文文本向量化
- **m3e-base**: 多语言嵌入模型
- **paraphrase-multilingual**: 多语言释义模型

## 配置方法

### 1. 安装依赖

```bash
pip install sentence-transformers torch
```

### 2. 配置 .env

```bash
# 使用本地嵌入模型
EMBEDDING_PROVIDER=local

# 选择模型（推荐 bge-small-zh-v1.5）
EMBEDDING_MODEL=BAAI/bge-small-zh-v1.5

# LLM 使用 Kimi
LLM_PROVIDER=kimi
KIMI_API_KEY=your_kimi_key_here
```

### 3. 首次运行

首次运行时，模型会自动从 HuggingFace 下载到本地：

```bash
python main.py index
```

下载位置：`~/.cache/huggingface/hub/`

## 性能对比

### 质量对比

| 模型 | 中文检索 | 英文检索 | 速度 | 成本 |
|------|---------|---------|------|------|
| BGE-small | ⭐⭐⭐⭐ | ⭐⭐⭐ | 快 | 免费 |
| BGE-base | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 中 | 免费 |
| BGE-large | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 慢 | 免费 |
| OpenAI text-embedding-3-small | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 快 | $0.02/1M tokens |

### 速度测试（单次嵌入）

- **BGE-small**: ~10ms
- **BGE-base**: ~30ms
- **BGE-large**: ~100ms
- **OpenAI API**: ~200ms (含网络延迟)

## 完整配置示例

### 方案 1：Kimi + BGE（推荐，完全国产）

```bash
# .env
LLM_PROVIDER=kimi
KIMI_API_KEY=sk-xxx

EMBEDDING_PROVIDER=local
EMBEDDING_MODEL=BAAI/bge-small-zh-v1.5
```

**优势**：
- 完全本地嵌入，无 API 费用
- Kimi 对中文理解好
- 数据隐私安全

### 方案 2：Kimi + OpenAI Embedding

```bash
# .env
LLM_PROVIDER=kimi
KIMI_API_KEY=sk-xxx

EMBEDDING_PROVIDER=openai
OPENAI_API_KEY=sk-xxx
```

**优势**：
- OpenAI 嵌入质量高
- 适合多语言场景

### 方案 3：Claude + BGE

```bash
# .env
LLM_PROVIDER=claude
ANTHROPIC_API_KEY=sk-xxx

EMBEDDING_PROVIDER=local
EMBEDDING_MODEL=BAAI/bge-base-zh-v1.5
```

**优势**：
- Claude 分析质量最高
- 本地嵌入节省成本

## 使用示例

```bash
# 初始化（首次会下载模型）
python main.py init

# 索引文件（使用 BGE 生成嵌入）
python main.py index

# 搜索（使用 BGE 进行语义匹配）
python main.py search "预算报告"
python main.py search "技术文档" --type slides

# 查看统计
python main.py stats
```

## 模型选择建议

### 场景 1：个人使用，文件量 < 1万

**推荐**：`BAAI/bge-small-zh-v1.5`
- 速度快，占用内存少
- 质量足够好
- 适合日常使用

### 场景 2：企业使用，文件量 > 1万

**推荐**：`BAAI/bge-base-zh-v1.5`
- 更高的检索准确率
- 性能和质量平衡
- 适合生产环境

### 场景 3：追求极致质量

**推荐**：`BAAI/bge-large-zh-v1.5`
- 最高质量
- 需要更多计算资源
- 适合高价值文档检索

### 场景 4：多语言混合

**推荐**：`OpenAI text-embedding-3-small`
- 多语言支持最好
- 需要 API 费用
- 适合国际化场景

## 常见问题

### Q1: 首次运行很慢？

A: 首次运行需要下载模型（100MB-1.3GB），之后会缓存到本地。

### Q2: 如何切换模型？

A: 修改 `.env` 中的 `EMBEDDING_MODEL`，重启程序即可。

### Q3: 模型存储在哪里？

A: 默认在 `~/.cache/huggingface/hub/`，可通过环境变量 `HF_HOME` 修改。

### Q4: 内存占用多少？

A:
- bge-small: ~500MB
- bge-base: ~1.5GB
- bge-large: ~4GB

### Q5: 可以使用 GPU 加速吗？

A: 可以！如果安装了 CUDA 版本的 PyTorch，会自动使用 GPU。

```bash
# 安装 GPU 版本
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Q6: BGE 和 OpenAI 嵌入兼容吗？

A: 不兼容。两者维度不同：
- BGE-small: 512 维
- OpenAI: 1536 维

切换模型需要重新索引所有文件。

## 性能优化

### 1. 批量处理

如果需要索引大量文件，可以修改代码使用批量嵌入：

```python
# 批量生成嵌入（更快）
embeddings = model.encode(texts, batch_size=32)
```

### 2. 使用 GPU

```bash
# 检查 GPU 是否可用
python -c "import torch; print(torch.cuda.is_available())"
```

### 3. 量化模型

使用量化版本减少内存占用（略微降低质量）：

```python
model = SentenceTransformer('BAAI/bge-small-zh-v1.5')
model.half()  # 使用 FP16
```

## 评测数据

BGE 在中文检索任务上的表现（MTEB Chinese）：

| 模型 | 平均分 | 检索 | 分类 | 聚类 |
|------|--------|------|------|------|
| BGE-large-zh | 64.8 | 71.4 | 68.9 | 62.1 |
| BGE-base-zh | 62.4 | 69.6 | 67.1 | 60.2 |
| BGE-small-zh | 58.4 | 63.0 | 65.6 | 56.8 |
| text2vec-base | 57.2 | 61.8 | 64.5 | 55.3 |

## 相关链接

- [BGE GitHub](https://github.com/FlagOpen/FlagEmbedding)
- [HuggingFace 模型页](https://huggingface.co/BAAI)
- [MTEB 排行榜](https://huggingface.co/spaces/mteb/leaderboard)
- [Sentence Transformers 文档](https://www.sbert.net/)

## 总结

**推荐配置**：Kimi (LLM) + BGE-small (嵌入)

这个组合：
- ✅ 完全免费（除了 Kimi API）
- ✅ 中文效果优秀
- ✅ 隐私安全
- ✅ 速度快
- ✅ 易于部署

对于大多数中文文档检索场景，这是最佳选择！
