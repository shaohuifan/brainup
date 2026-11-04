# 调研资料索引（research/）

> 本目录按 LLM Wiki 模式组织：`raw/` 为不可变原始资料（人写 LLM 读），`wiki/` 为综合分析（LLM 写人读）。
> 用法：先读本索引定位，再深入具体文件。

## wiki/（综合分析）

| 页面 | 内容 | 状态 |
|---|---|---|
| [wiki/landscape.md](wiki/landscape.md) | 生态全景图：时间线、规模、生态位分类、标准化进程、大厂动态、社区技术趋同、格局判断 | ✅ 初版 |
| [wiki/synthesis.md](wiki/synthesis.md) | 调研总结论：证据调和（wiki 胜负边界）、定位空隙、设计约束 P0-P7、风险清单、设计阶段讨论题 | ✅ 完成 |

## raw/（原始资料）

| 文件 | 来源 | 内容 |
|---|---|---|
| [raw/awesome-llm-wiki-readme-2026-11-04.md](raw/awesome-llm-wiki-readme-2026-11-04.md) | github.com/gavischneider/awesome-llm-wiki | 生态主清单全文抓取（~200 条目：文章/工具/论文/评测） |
| [raw/karpathy-gist-and-comments-2026-11-04.md](raw/karpathy-gist-and-comments-2026-11-04.md) | gist 评论区（用户提供） | 原文要点 + 14 个社区实现摘要 + 关键批评（hyunsoo36 ingest 成本质疑等） |
| raw/deep-dive-standards-vendors.md | 子代理抓取 | OKF 规范、LangChain OpenWiki/WikiBench、腾讯 WeKnora、MS/Vercel/Pinecone、YANP |
| raw/deep-dive-papers.md | 子代理抓取 | 14 篇 arXiv/zenodo 论文摘要与启示（含负面结果） |
| raw/deep-dive-failure-modes.md | 子代理抓取 | 真实规模运行的失败模式与对策（10 个一手运维报告/横评） |

## 操作历史

见 [log.md](log.md)。
