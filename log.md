# 项目日志（append-only）

> 约定：条目前缀 `## [YYYY-MM-DD] 操作 | 标题`，便于 grep。研究阶段日志见 [research/log.md](research/log.md)。

## [2026-11-04] scaffold | 仓库脚手架落地，命名定稿
- 命名定稿：`brainup`（repo/PyPI，PyPI 可用性已验证）+「升级大脑」（中文产品名，双语字面同构：brain=大脑、up=升级）
- 脚手架：Python 3.12+/uv、typer CLI（7 命令面：version/status/init/ingest/query/lint/review/metrics，v0.1 仅前两个可用）、pytest+ruff、GitHub Actions CI（ubuntu+windows × 3.12/3.13）、Apache-2.0
- 设计依据 `design/design-proposal-v0.1.md`（全部决策已用户确认）；调研依据 `research/wiki/synthesis.md`（30+ 一手来源）
- 修复：Windows 中文控制台乱码（PEP 686 之前 stdio 跟随系统代码页）→ 入口强制 UTF-8 reconfigure；ruff 全绿、4 测试通过
- 首次提交 `81f48e3`（21 文件）；AGENTS.md 补充命令速查
- 命名讨论记录：用户提议 7 个候选（LoveLearn/GoodGoodStudy/HappyLearn/LearnDeeper/FixYourBrain/UpdateYourBrain/DiveYourBrain），逐一评价后采纳 UpdateYourBrain 的机制意象；用户将「涨知识」修正为「升级大脑」（双语同构更优）；GoodGoodStudy 与 wikiloom 在 PyPI 已被占用（后者为同赛道竞品）

## [2026-11-04] publish | GitHub 发布完成
- 仓库上线：https://github.com/shaohuifan/brainup（main 分支，6 commits）
- 主题标签：llm-wiki / knowledge-base / mcp / cli / personal-knowledge-management / obsidian / karpathy / okf / chinese / reading
- 过程记录：gh CLI 经 winget 安装（首次下载超时重试成功）；设备码流程三次失败（一次过期、一次网络轮询超时、一次用户未完成）后第四次成功，补齐 workflow scope；首次 push 因 OAuth token 缺 workflow scope 被拒（CI 文件需要）；repo description 曾被 PowerShell 5.1 无 BOM 读取写坏，经 gh api + UTF-8 JSON 修正
- 教训：本机 PowerShell 5.1 执行含中文的 .ps1 脚本会因编码假设产生 mojibake——含中文的脚本应走 JSON 文件 + gh api，或写 BOM
- 用户反馈：repo description 去掉「中文优先」表述
- CI 修复：Actions runner 无全局 git 身份导致测试失败（Vault.init 首次 commit 需要）→ ci.yml 增加 identity 配置；修复后四矩阵全绿（41783750189，1m16s）

## [2026-11-04] build | 核心引擎构建完成（184d9d5）
- 9 个引擎模块 + 35 项测试全绿 + ruff 全绿 + 端到端验证通过（init→ingest→MCP 提交→人审→lint→检索→伪造引用拦截）
- P0 写路径信任全部落地并测试锁定：封闭词表（extra=forbid）、逐字引用核验、人审队列、原子应用、失败零写入
- 过程中修复的真实 bug：frontmatter 切分、CJK 分词（unicode61 单 token 问题→逐字分词+bigram OR）、mcp 2.x API 更名、lint 复活已裁决项、BOM 污染、MCP stdio 编码
- 已知边界（诚实记录）：PDF/EPUB 为直提取（复杂版式 v0.2）；LLM 路径为打桩测试（无真实 key 验证）
- 下一步：v0.2 路线（FSRS 复习卡、播客/视频源、领域模板扩展）见 design/design-proposal-v0.1.md 第六节
