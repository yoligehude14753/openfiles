# PRD：AI 驱动的智能文件检索与幻灯片级抽取工具（Mac）

## 1. 产品概述
- 愿景：深度理解用户本地所有文件（除视频原帧解析外），提供“最懂我”的检索与局部输出体验，包含幻灯片级搜索与导出。
- 目标用户：Mac 知识工作者、创作者、职场用户；常处理文档/表格/演示/图片/代码/音频/压缩包；经常“记得内容但忘记位置”；常需从多份 PPT/Keynote/WPS 中挑几页组新材料。
- 核心价值：语义理解、多模态支持、上下文推理；幻灯片级抽取与跨文件合成；隐私与成本可控。

## 2. 用户场景
- 找到“含预算饼图/备注提到客户投诉的那张幻灯片”，导出为图片或插入新 PPT。
- 从多份方案中拼“竞品对比页合集”并导出 PPTX/PDF。
- 从 PDF 讲义/扫描件中抽“公式页/流程图页”。
- 模板库中搜“封面/目录页/占位符少的页”组合新 deck。
- 会议材料：同一会议的 PPT、录音、纪要串联，按时间/目录聚合。
- 隐私：自动排除 .ssh/钥匙串/浏览器存储/密码库；敏感目录仅元数据或跳过。

## 3. 功能需求

### 3.1 文件扫描与解析
- 扫描：默认 ~/Documents ~/Desktop ~/Downloads；支持包含/排除；跳过系统/缓存/隐藏目录；大小上限。
- 类型覆盖：
  - 文档：PDF/Word(doc, docx)/Pages/MD/TXT/RTF/HTML/Email。
  - 表格：Excel(xls, xlsx)/CSV/Numbers。
  - 演示：PPT/PPTX/WPS(DPS)/Keynote；必要时转 PDF/图片。
  - 图片：JPG/PNG/GIF/WebP/HEIC/SVG/TIFF（Vision）。
  - 代码：常见语言。
  - 压缩包：ZIP/RAR/7z，列清单+抽样摘要。
  - 音频：mp3/wav/flac，元数据+同目录上下文。
  - 视频：mp4/mov/avi/mkv 等不做帧解析；基于文件名/元数据/同目录摘要推断描述与置信度。
- 解析策略：
  - 在线 LLM/Vision 处理文本/图片/PDF/演示页；长文档分块+汇总。
  - Office/WPS/Keynote：优先 python-pptx 读取文本/备注；无法直接读则 LibreOffice/soffice headless 转 PDF，再按页转图片 + Vision/OCR；Keynote 可用 qlmanage 缩略图或 AppleScript 导出 PDF（需权限）。
  - 未知/不可解析：用元数据 + 同目录摘要 + 路径/扩展名推断，生成说明与置信度。

### 3.2 幻灯片级索引与导出
- 每页记录：slide_id、file_id、page_number、title、summary、keywords、notes 摘要、thumbnail_path/uri、layout_hints（含图表/大图/多段文字/备注长度）、confidence、hash（页级）、source_model、cost_tokens、indexed_at。
- 幻灯片级 embedding 精排，文件级 embedding 粗排。
- 导出操作：
  - 选中多页→导出新 PPTX（简化版式）/PDF/PNG/JPEG。
  - 复制图片或文本摘要；可选保留/忽略演讲者备注。
  - 打开原文件并跳页（提示页码或 URI）。
- 兼容性：自动识别 Office/WPS/Keynote；缺依赖提示安装 LibreOffice/授权 Keynote 导出；失败降级 PDF/图片快照+Vision 摘要。

### 3.3 知识库与数据
- 元数据库（SQLite）：
  - files：file_id/path/hash/type/size/ctime/mtime/indexed_at/status/retry/summary/keywords/category/confidence/source_model/cost_tokens/error。
  - slides：slide_id/file_id/page_number/title/summary/keywords/notes/thumbnail_path/layout_hints/confidence/hash/indexed_at/source_model/cost_tokens。
  - context：file_id/dir_summary/sibling_files/json；archives 清单；inference_reason（推断描述）。
  - tasks：ingest 状态、错误、重试计数。
- 向量库：文件级、幻灯片级分表；默认 sqlite-vec，>20 万文件可切换 Qdrant/LanceDB。
- 缓存：文件/页哈希未变跳过；LLM 响应缓存；缩略图缓存。

### 3.4 增量与队列
- FSEvents 监听创建/修改/删除；实时入队；定期全量校验补漏。
- 任务队列：优先级（桌面/文档/下载、最近修改、手动置顶）；失败队列+指数退避；断点续传。
- 并发/限流：集中限流器控制 LLM/嵌入并发与速率。

### 3.5 检索与体验
- 模式：语义搜索（文件/幻灯片）；混合关键词；过滤（时间/类型/大小/目录/置信度/页范围）；中英双语时间解析。
- 展示：文件视图与幻灯片视图切换；缩略图/摘要/置信度/模型来源；“为何返回”解释；QuickLook 预览。
- 操作：打开/显示位置/复制路径；导出选中页；跨文件多页合成新 deck/PDF/图片包。
- 关联：同目录聚合、会议材料关联、模板/封面页快速搜。

### 3.6 成本与性能
- 预算：每日/月度上限，超限降级为元数据模式并提示。
- 大文件：分块/采样；模型选择（轻量 vs 高精）。
- 去重：文件哈希、页级哈希；重复不二次解析。
- 并行：受限并发；后台低优先级不干扰前台。

### 3.7 隐私与安全
- 本地存储；传输 HTTPS。
- 黑名单：.ssh、钥匙串、浏览器存储、密码库、云盘缓存、系统/临时目录。
- 模式：标准（云解析）/隐私（仅元数据+本地嵌入）。
- 权限：Full Disk Access 引导；Keynote/QuickLook/AppleScript 权限提示；API Key 加密（Keychain）。

### 3.8 可靠性与可观测性
- 指标：处理速率、失败率、token/成本、索引大小；健康检查。
- 降级：LLM 不可用→元数据搜索；Vision 失败→OCR/文本回退；导出失败→图片打包。
- 备份与迁移：导出/导入索引（JSON/CSV）；数据库备份与 VACUUM/压缩。

### 3.9 UI/UX（Mac）
- 菜单栏常驻 + 全局快捷键召回。
- 状态面板：索引进度、队列长度、失败任务、预算消耗。
- 搜索面板：文件/幻灯片视图、过滤、解释、预览、导出。
- 设置：目录/黑名单、模型、预算、是否索引备注/隐藏页、导出默认格式。

## 4. 技术方案概要
- 前端：SwiftUI 菜单栏 + QuickLook 预览；本地 HTTP/Unix socket 调用后端。
- 后端：Python FastAPI + asyncio 队列；FSEvents 监听；任务调度与限流；CLI 兼容。
- 解析链：类型检测 → 预处理（Office/WPS/Keynote 转 PDF/图片）→ 分页/分块 → LLM/Vision 摘要 + 备注抽取 → 嵌入 → 存储。
- 幻灯片导出：
  - 读取：python-pptx（文本/备注）；转图：libreoffice --headless --convert-to pdf + pdftoppm/ImageMagick 或 Keynote qlmanage；失败则 Vision 直接解析。
  - 组装：python-pptx 生成新 deck（简化版式），或先合并 PDF（PyPDF2）再可选转回 PPTX；图片批量输出。
- 存储：SQLite + sqlite-vec（默认）；可切 Qdrant/LanceDB。
- LLM/Embedding：Claude/GPT-4o 等解析；OpenAI text-embedding-3 等嵌入；模型可配置。

## 5. 流程
- 索引：扫描→入队→解析（含演示分页/缩略图/备注）→摘要→嵌入→写库（files+slides+context）→缓存/统计。
- 搜索：query→嵌入→文件粗排→幻灯片精排→过滤/解释→展示缩略图→导出/打开。
- 导出：选页→生成 PPTX/PDF/PNG/JPEG → 保存本地/打开文件夹。

## 6. 路线图
- Phase 1 (MVP)：CLI 全量索引；文本/图片/PDF 解析；文件级检索；成本/权限提示。
- Phase 2 (Beta)：FSEvents 增量；幻灯片级索引（PPTX/PDF）+ 缩略图；幻灯片搜索与导出图片/PDF；失败队列；菜单栏 UI 初版。
- Phase 3 (GA)：Keynote/WPS 兼容转换；跨文件多页合成 PPTX；高级过滤/解释；预算面板；备份/恢复；隐私模式；性能/成本调优。
- Phase 4（优化）：模板/封面页搜索、会议聚合、推荐/关联、更多自动化导出场景。

## 7. 成功指标
- 覆盖率：文件索引成功率 >95%；幻灯片缩略图成功率 >90%（可解析格式）。
- 相关性：检索结果用户认可度 >90%；幻灯片级命中率 >85%。
- 性能：P50 搜索 <800ms，P95 <1.5s；初始化 10 万文件 ≤X 小时（上线前给出测算）。
- 成本：≤ $X/每万文件（上线前设定）；超限自动降级。
- 可靠性：任务失败率 <1%，重试成功率 >80%；导出成功率 >95%。

## 8. 风险与缓解
- 解析/兼容性失败：Office/WPS/Keynote → PDF/图片转换链；失败回退 Vision+元数据；提示安装依赖。
- 成本爆发：预算守卫、分块、缓存、哈希去重。
- 隐私担忧：隐私模式、敏感目录黑名单、本地存储。
- 性能瓶颈：限流并发、优先级队列、冷热目录策略、哈希跳过。
