# 使用 Kimi API 配置指南

## Kimi API 简介

Kimi 是由月之暗面（Moonshot AI）开发的大语言模型，支持超长上下文（最高 128k tokens）。本项目已集成 Kimi API 支持。

## 配置步骤

### 1. 获取 API Key

访问 [Moonshot AI 开放平台](https://platform.moonshot.cn/) 注册并获取 API Key。

### 2. 配置环境变量

编辑 `.env` 文件：

```bash
# 设置 Kimi API Key
KIMI_API_KEY=your_kimi_api_key_here

# 设置 LLM 提供商为 kimi
LLM_PROVIDER=kimi

# （可选）如果需要使用嵌入功能，仍需配置 OpenAI API Key
OPENAI_API_KEY=your_openai_key_here
```

### 3. 支持的模型

项目默认使用 `moonshot-v1-32k` 模型，支持：
- **moonshot-v1-8k**: 8k 上下文窗口
- **moonshot-v1-32k**: 32k 上下文窗口（默认）
- **moonshot-v1-128k**: 128k 上下文窗口

### 4. 功能支持

✅ **文本摘要**: 使用 Kimi 进行文档内容分析和摘要
✅ **关键词提取**: 自动提取关键主题和关键词
✅ **图片分析**: 支持 Kimi 的视觉能力分析图片内容
✅ **中文优化**: Kimi 对中文内容理解更好

⚠️ **嵌入向量**: Kimi 不提供嵌入模型，仍需使用 OpenAI 的 text-embedding-3-small

## 使用示例

### 初始化和索引

```bash
# 初始化数据库
python main.py init

# 开始索引（使用 Kimi）
python main.py index
```

### 搜索

```bash
# 搜索文件
python main.py search "预算报告"

# 搜索幻灯片
python main.py search "产品规划" --type slides --limit 20

# 查看统计
python main.py stats
```

## 成本对比

| 模型 | 价格（每百万 tokens） | 适用场景 |
|------|---------------------|---------|
| moonshot-v1-8k | ¥12 (~$1.7) | 短文档 |
| moonshot-v1-32k | ¥24 (~$3.4) | 中长文档（默认） |
| moonshot-v1-128k | ¥60 (~$8.5) | 超长文档 |
| Claude 3.5 Sonnet | $3 | 高质量分析 |
| GPT-4o-mini | $0.15 | 经济实惠 |

## 切换 LLM 提供商

在 `.env` 中修改 `LLM_PROVIDER` 即可切换：

```bash
# 使用 Kimi
LLM_PROVIDER=kimi

# 使用 Claude
LLM_PROVIDER=claude

# 使用 OpenAI
LLM_PROVIDER=openai
```

## 优势

1. **超长上下文**: 最高支持 128k tokens，适合处理长文档
2. **中文优化**: 对中文内容理解更准确
3. **成本适中**: 价格介于 GPT-4 和 GPT-3.5 之间
4. **国内访问**: 无需代理，访问速度快

## 注意事项

1. **嵌入功能**: 搜索功能仍需要 OpenAI API Key（用于生成嵌入向量）
2. **图片分析**: Kimi 支持图片分析，但需要确保图片大小合理
3. **预算控制**: 在 `.env` 中设置 `DAILY_BUDGET_USD` 和 `MONTHLY_BUDGET_USD` 控制成本

## 故障排查

### 问题：API 调用失败

检查：
1. API Key 是否正确配置
2. 网络连接是否正常
3. API 配额是否充足

### 问题：搜索功能不工作

确保：
1. 已配置 `OPENAI_API_KEY`（用于嵌入）
2. 已完成文件索引

### 问题：中文乱码

Kimi 原生支持中文，不应出现乱码。如果出现，检查：
1. 文件编码是否为 UTF-8
2. 终端是否支持中文显示

## 更多信息

- [Kimi API 文档](https://platform.moonshot.cn/docs)
- [定价信息](https://platform.moonshot.cn/pricing)
- [使用限制](https://platform.moonshot.cn/docs/intro#使用限制)
