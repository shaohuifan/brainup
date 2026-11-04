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

- **调研阶段已完成**，产出在 `research/`（按 LLM Wiki 模式组织）：`wiki/synthesis.md` 是总结论入口，`wiki/landscape.md` 是生态全景，`raw/` 存四份原始资料（主清单/gist 评论区/三份深挖笔记）。
- **设计已确认**（`design/design-proposal-v0.1.md`）：读书/学习场景；CLI + MCP 工具先行（引擎/壳分离）；技术栈 Python 3.12+ / uv；模型 BYOK 全兼容（OpenAI-compat + Anthropic，小模型路由+大模型综合）；Apache-2.0；双语命名（具体名待定）。
- 仓库尚未 `git init`。核心架构约束：Vault 三层单向流（raw 不可变 → .kb 可重建 → wiki append-only）、封闭动作词表写路径、lint=决策队列、渐进结构化（50/100/300 阈值）、OKF v0.2 兼容。
- 本文件需随项目推进持续更新：仓库脚手架落地后补充命令速查（build / test / lint），代码成型后补充架构与目录说明。

## 既定工作流（用户约定，勿跳过）

1. **调研** ✅：系统性调研市面上开源个人知识库项目与相关论文的最新进展；为收集资料可自行编写爬虫。
   - 已知调研起点：Karpathy gist 评论区与 "Awesome LLM Wiki" 清单聚合了大量实现，如 iwe、second-brain-skill、Obelyth Cortex、mindbase、EXIA SEED、MemexOS、Kompl、Link、llm-repo-wiki、podcast-wiki、nimbalyst-wiki 等；注意同时收集对模式本身的批评与量化评估（如 ingest 编译成本 vs 检索收益的权衡）。
2. **设计** ← 当前阶段：与用户讨论确定项目设计；技术栈、架构、目录结构等重大决策必须经用户确认后再落地，勿擅自定稿。设计讨论题清单见 `research/wiki/synthesis.md` 第六节。
3. **实现与发布**：按确认的设计开发，最终开源发布到 GitHub。

## 沟通约定

- 使用中文与用户沟通。
