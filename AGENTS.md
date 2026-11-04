# AGENTS.md

## 项目使命

基于 Andrej Karpathy 的 LLM Wiki 模式构建开源个人知识库项目：帮助用户在 AI 时代借助 AI 系统地学习新知识、沉淀新知识，构建和维护自己的知识库。

**LLM Wiki 模式要点**（原文 https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f ，设计讨论的领域词汇以此为准）：

- 核心理念：区别于 RAG（每次查询从原始文档重新检索拼装），LLM 增量构建并维护一个持久的、互相链接的 markdown wiki。知识编译一次、持续保鲜；人负责筛选来源、提问、把关，LLM 负责总结、交叉引用、一致性维护等全部簿记工作。
- 三层架构：raw sources（不可变原始资料，人写 LLM 读）→ wiki（LLM 生成维护的知识库，LLM 写人读）→ schema（AGENTS.md 类约定文档，人与 LLM 共同演化）。
- 三类操作：Ingest（摄入新来源，单个来源可触及 10-15 个页面）/ Query（回答基于 wiki，好的答案归档回 wiki，让探索也复利）/ Lint（健康检查：矛盾、过时主张、孤儿页、缺失引用）。
- 两个特殊文件：index.md（内容目录，LLM 查询入口，中等规模下可替代向量检索）、log.md（append-only 时间线，条目前缀 `## [YYYY-MM-DD] 操作 | 标题` 便于 grep）。
- 思想源头：Vannevar Bush 的 Memex（1945）。

## 当前状态（2026-11-04）

- **项目名**：`brainup`（repo/PyPI）+「升级大脑」（中文产品名）。学习爱好者的 LLM Wiki 复利知识库引擎（多源：论文/书籍/博客/播客/视频/代码），CLI + MCP 工具先行（引擎/壳分离，v0.3 GUI 包壳）。
- **阶段**：v0.1 骨架已提交（`81f48e3`）。设计已定稿：`design/design-proposal-v0.1.md`；调研产出入库 `research/`（`research/wiki/synthesis.md` 为结论入口）。
- **核心架构约束**（勿违反，有调研证据支撑）：Vault 三层单向流（raw 不可变 → .kb 可重建 → wiki append-only）、封闭动作词表写路径（raw 层从动作枚举上不可达）、lint=决策队列、渐进结构化（50/100/300 阈值）、OKF v0.2 兼容、答案写回带防火墙。

## 命令速查

```bash
uv sync --dev          # 安装依赖（含 dev 组）
uv run brainup --help  # CLI（v0.1 仅 version/status 可用，其余为占位）
uv run pytest          # 测试
uv run ruff check .    # lint
uv build               # 构建
```

- 本地解释器为 CPython 3.14（requires-python >=3.12）；CI 矩阵 3.12/3.13 × ubuntu/windows。
- Windows 中文控制台：CLI 已强制 UTF-8 stdio；旧版 conhost 需 `chcp 65001`。
- 提交信息用文件方式传入（`git commit -F <file>`），避免 shell 多行结构问题。

## 既定工作流（用户约定，勿跳过）

1. **调研** ✅：系统性调研市面上开源个人知识库项目与相关论文的最新进展；为收集资料可自行编写爬虫。
   - 已知调研起点：Karpathy gist 评论区与 "Awesome LLM Wiki" 清单聚合了大量实现，如 iwe、second-brain-skill、Obelyth Cortex、mindbase、EXIA SEED、MemexOS、Kompl、Link、llm-repo-wiki、podcast-wiki、nimbalyst-wiki 等；注意同时收集对模式本身的批评与量化评估（如 ingest 编译成本 vs 检索收益的权衡）。
2. **设计** ← 当前阶段：与用户讨论确定项目设计；技术栈、架构、目录结构等重大决策必须经用户确认后再落地，勿擅自定稿。设计讨论题清单见 `research/wiki/synthesis.md` 第六节。
3. **实现与发布**：按确认的设计开发，最终开源发布到 GitHub。

## 沟通约定

- 使用中文与用户沟通。
