# 项目日志（append-only）

> 约定：条目前缀 `## [YYYY-MM-DD] 操作 | 标题`，便于 grep。研究阶段日志见 [research/log.md](research/log.md)。

## [2026-11-04] scaffold | 仓库脚手架落地，命名定稿
- 命名定稿：`brainup`（repo/PyPI，PyPI 可用性已验证）+「升级大脑」（中文产品名，双语字面同构：brain=大脑、up=升级）
- 脚手架：Python 3.12+/uv、typer CLI（7 命令面：version/status/init/ingest/query/lint/review/metrics，v0.1 仅前两个可用）、pytest+ruff、GitHub Actions CI（ubuntu+windows × 3.12/3.13）、Apache-2.0
- 设计依据 `design/design-proposal-v0.1.md`（全部决策已用户确认）；调研依据 `research/wiki/synthesis.md`（30+ 一手来源）
