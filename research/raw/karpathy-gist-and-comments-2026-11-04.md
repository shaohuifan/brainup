# Karpathy LLM Wiki Gist 原文与评论区摘要

- 来源：https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- 抓取日期：2026-11-04（用户提供全文）

## 原文核心（完整保留于 AGENTS.md，此处存证要点）

- 模式定位："idea file"，设计为复制给 LLM Agent 使用
- 核心反 RAG 论点：RAG 每次查询重新拼装，无累积；wiki 是持久、复利的产物，交叉引用、矛盾标记、综合已完成
- 三层：raw sources（不可变）/ wiki（LLM 写人读）/ schema（CLAUDE.md/AGENTS.md，共同演化）
- 三操作：Ingest（单源可触及 10-15 页）/ Query（好答案归档回 wiki）/ Lint（矛盾、过时、孤儿、缺页、缺引用）
- index.md（目录，~100 源/数百页规模可替代向量检索）+ log.md（append-only，`## [日期] 操作 | 标题` 前缀可 grep）
- 思想源头：Vannevar Bush Memex (1945)；"Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase"
- 明确声明：文档刻意抽象，实现细节（目录、schema、页面格式、工具）由使用者与 LLM 共同实例化；一切都是可选模块

## 评论区高价值信息（按项目/主题）

### 社区实现（gist 评论区）

| 项目 | 作者 | 要点 |
|---|---|---|
| Obelyth Cortex v2.0.2 | ShootJackal | MCP server over private Git repo of Markdown；无模型参与引用校验（每条引用核对到 Git commit）；retracted passages 标记 SUPERSEDED；AGPL-3.0；测试 3068；曾发现"伪造文件边界骗取 VERIFIED"漏洞 |
| iwe | gimalay | 澄清：Karpathy gist 是方法论，IWE 提供 Markdown 图操作工具；gimalay gist 展示如何用 IWE 实现该模式（保留三层+三操作，增加确定性 schema/orphan 检查、重命名更新引用） |
| podcast-wiki | HagaiHen | 播客为源；MCP 列 Spotify 已听集数；Whisper 转写。经验：**Extend, don't create**（默认失败是近似重复页）；**Never silently overwrite**（分歧放入"Disagreements & open questions"节，标注来源）；**Rewrite the summary, don't append**；周期性"dream"pass 合并漂移页面。69 概念页/60 集，每几小时无人值守运行 |
| quiz_wiki/llmwiki v0.14.0 | suwonleee | 项目决策 wiki + 测验；实验：决策存续 8 场景×8 次（Wiki only 0/8 → +prompt excerpts 4/8 → +edit-time rule gate 7/8 → both 8/8）；Open Knowledge Format v0.2（typed YAML、sources、相对链接、文件夹索引）；本地 Markdown + SQLite，跨 Claude Code/Codex/OpenCode 共享 |
| MindBase 0.4.6 | frankchu91 | 回应评论区具体问题：broken citation/broken link 在 lint 时代码计算（无模型）；每次回答报告"read 3 pages · 9.1k of 14.2k chars fit · clipped: deep-work.md"（assembler 丢字可见）；near duplicate pairs 研究；自由文本先落盘再调模型（fail open）；查询也入日志（多数实现只记 ingest）。MIT |
| Link 5.0 | gowtham0992 | 本地记忆引擎（非 wiki 编译器，但同域）：review-gated 写入、记忆层无 LLM、规则强制（ask/deny 命令检查）、`lnk stale` 检查记忆引用的文件/脚本/依赖/URL/版本是否仍存在（0 误报 345 引用）、`lnk receipt` 会话回执、supersedes 谱系（旧矛盾值 0.00 先返回，新值 0.94）、NLI 矛盾检测 opt-in（裸用误报太多，30% 主题重叠门控后 0 误报 +1 补充） |
| Kompl | tuirk | 传统 wiki（规则与结构）+ LLM wiki（模型读写）的合成；本地 NLP + 固定规则保结构，模型做读写；来源一次性编译为带编号引用的互链页面；来源分歧时页面双面展示；新来源推翻旧主张时标记 changed；MCP 供 agent 读 |
| llm-repo-wiki | lucaslimafons | 模式应用于代码；每条 claim 引用确切代码行；PR 合并只更新受影响页面；chat 可编辑 wiki；以可审查 diff 交付变更（对比 DeepWiki 类工具的重新生成） |
| MemexOS | liushengyu | 三层之上：无审查不入 wiki（writer 在独立 git worktree 分支工作，程序检查先跑，再由**不同家族模型**逐句对照来源审查）；夜间采集器（YouTube/Bilibili/X/RSS/agent 会话结论）；基于真实使用反馈修正；检索对照预标注问题集检验；`memex search/get` CLI 供任意 agent。作者自述未解决：如何持续积累同时防污染、正确退役过期知识 |
| EXIA SEED | francisdu53 | 无向量搜索，Fuzzy Cognitive Map (Kosko 1986) 铺在页面上；spreading activation 检索；每条 fact 引用确切来源行，确定性 checker 拒绝来源行中不存在的数字/日期/专名；同记忆同问题字节级可复现；LongMemEval oracle 融合 500 题：44.4% vs bge-m3 46.6%（统计不显著=要点：同质量无嵌入模型，中位搜索 11ms vs 315ms，123MB vs 2.6GB RAM）；正确弃答 83% vs 67%；Apache 2.0 |
| crow-hq/llm-wiki-v2 | sassarini-marco | 论文 doi:10.5281/zenodo.22898752；ingest 时 LLM 调用 72% 花在"决定"（哪个文件夹/是否同题/合并否/链接什么）而非写作；小型 typed classifier 接管决策后：正确笔记命中 89% vs 62%（525 文档），ingest 时间减半，token 成本随规模持平；AGPL-3.0，支持 Ollama |
| second-brain-skill | ChavesLiu | Claude Code skill；三层；六命令 /wiki init/ingest/query/lint/wipe/test；自然语言触发；sources/entities/concepts/analyses 四分类；Obsidian + OpenClaw 集成；zh/en 内容语言；MIT |
| nimbalyst-wiki | karlwirth | 反方立场：**wiki 不应是 agent 的记忆，应是写给人（指挥 agent 的人）的**；只记显著的（决策：谁、何时、放弃了什么选项；开放问题及 owner；现状摘要）；测试：失忆后的自己或新 agent 能否凭 wiki 重建现状；MIT |
| Eigma | ya2080 | 对话→结构化可视化 wiki + 间隔复习（spaced review） |

### 关键批评与开放问题（gist 评论区）

- **hyunsoo36（最重要批评）**：ingest 成本难以为继——编译出的 wiki 常缺回答问题所需细节，agent 仍要回读原始来源；wiki 变成额外一层需要导航与验证的结构，叠加 LLM 调用/工具调用/延迟/token；检索节省未见抵消开销。根因怀疑：**ingest 时综合 vs 开放式未来问题的错配**——不知道用户会问什么之前，编译器必须决定保留哪些细节、如何组织；对一问有用的摘要可能恰好略去另一问所需。wiki 对人类可读综合、决策记录、限定领域常见问题有价值；作为通用检索层的价值存疑。呼吁：测量其划算条件（多样化未见问题，计入 ingest/维护/导航/源验证 vs 直接检索）
- securityguy：多类记忆并用（kanban 任务、90 天消息库、后台维护的类 RAG 记忆、文件共享）；观望 OKF 能否被 agent 像 wiki 一样访问
- karlwirth：多 agent 并行时人被淹没；更富的 wiki 反而更糟；见 nimbalyst-wiki 立场
- NDOTO-G vs ShootJackal 交流：doc.html 变更检测 vs markdown wiki 健康检查的实验（wiki 版重复错误事实，doc.html 版察觉异常）
- bg-numarqe / spasm-myelixlabs：代码是关系性知识，markdown 文件夹在"什么调用这个函数"类问题上失效→Synapse MCP 实时代码图（商业推广，注意甄别）
- 评论区大量商业 spam（ALS 药、Stardew 规划器、AI 修图等）——说明热度极高，也提醒调研需甄别

### 时间线线索

- Karpathy 首帖（X status/2039805659525644595）与 gist 后续帖（2040470801506541998）
- SingggggYee 清单引用的更早帖（2026-04-03，"raw data... compiled by an LLM into a .md wiki"），1.7M views
- Gist 创建约 7 个月前（~2026-04）
