# 深挖笔记：标准化规范与大厂/商业公司动态

- 调研日期：2026-11-04
- 调研人：deep-dive-standards-vendors 子代理
- 方法：webfetch 直接抓取 12 个一手来源（规范全文 ×2、公告博客 ×3、GitHub 仓库 ×5、产品博客 ×2），逐条提取可验证事实与数字
- 上游任务：补充 wiki/landscape.md 中"标准化进程"与"大厂动作"两个维度的证据深度

---

## 1. Google Open Knowledge Format（OKF）—— 最重要的标准化事件

### 1.1 基本盘（可验证事实）

| 项 | 事实 |
| --- | --- |
| 仓库 | github.com/GoogleCloudPlatform/knowledge-catalog（okf/ 子目录） |
| 规范文件 | okf/SPEC.md，v0.2，1006 行 / 786 loc / 36.9 KB |
| v0.1 发布 | 2026-06-13，博客《Introducing the Open Knowledge Format》，作者 Sam McVeety（Tech Lead, Data Analytics）、Amir Hormati（Tech Lead, BigQuery） |
| v0.2 发布 | 2026-07-25，博客《Open Knowledge format v0.2 tackles agentic trust》，同两位作者 |
| 官方定位 | v0.1 公告原文："formalizes the [LLM-wiki] pattern into a portable, interoperable format"，并直接链接 Karpathy gist |
| 商业承接 | Google Cloud Knowledge Catalog（前身 Dataplex）已支持 ingest OKF 并 round-trip（v0.2 博客宣布） |

来源：
- https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
- https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing/
- https://cloud.google.com/blog/products/data-analytics/okf-v0-2-adds-trust-signals

### 1.2 v0.1 核心设计（2026-06-13 公告）

- **形态**："a directory of markdown files with YAML frontmatter"。宣传语极端克制："If you can `cat` a file, you can read OKF; if you can `git clone` a repo, you can ship it."
- **v0.1 字段集**：`type`、`title`、`description`、`resource`、`tags`、`timestamp`（仅此六个）。
- **三原则**：
  1. Minimally opinionated —— 对每个 concept 只要求一个 `type` 字段；
  2. Producer/consumer independence —— 格式即契约，两端工具可独立替换；
  3. Format, not platform —— 不绑定任何云/数据库/模型厂商，永远不需要专有账号或 SDK。
- **首发参考实现**：① enrichment agent（遍历 BigQuery 数据集为每张表/视图起草 OKF 概念文档，再用第二个 LLM pass 抓取权威文档补充引用/schema/join path）；② 静态 HTML 可视化器（单文件、无后端、无安装、数据不出页面）；③ 三个样例 bundle：GA4 e-commerce、Stack Overflow、Bitcoin 公共数据集。
- **动机陈述**（对个人知识库项目有直接参考价值）：组织内知识碎片化在 metadata catalog API、wiki、代码注释、"少数资深工程师的脑袋"里；每个 agent builder 都在从零解决同一个 context-assembly 问题。

### 1.3 v0.2 规范全文要点（SPEC.md 逐节提取）

**目录结构约定（§3）**：

```
path/to/bundle/
  index.md                      # 可选。目录列表，progressive disclosure
  log.md                        # 可选。按时间倒序的更新历史
  <concept>.md                  # bundle 根下的概念文档
  <subdirectory>/...
```

- 保留文件名仅两个：`index.md`（§8）与 `log.md`（§9），任何层级都不得用作 concept 文档。
- 分发方式：git 仓库（推荐）、tarball/zip、大仓库内的子目录。
- `log.md` 格式：`# Directory Update Log` + 按 `## YYYY-MM-DD`（ISO 8601，必须）分组的条目，最新在前；条目是散文，前导粗体词（`**Update**` / `**Creation**` / `**Deprecation**`）是惯例非要求。

**Frontmatter schema（§4.1）**：

- 唯一必填：`type`（短字符串，不中心化注册，producer 自选描述性值，consumer 必须优雅容忍未知 type）。只带 `type` 的概念即完全合规（§11）。
- 推荐：`title`、`description`（一句话，供 index 生成器/搜索摘要）、`resource`（底层资产的规范 URI）、`tags`。
- 扩展：producer 可加任意键；consumer 必须保留未知键、不得拒收。
- body 约定标题：`# Schema`、`# Examples`、`# Computation`。

**Provenance：`sources`（§5.1）**：

- 每个 entry：`resource`（entry 内必填；可为具体 URL / bundle 相对路径 / `references/` 内路径，或 scope descriptor 如 "all queries in BigQuery project X"）、`id`（稳定键，用于 per-claim 归属）、`title`，以及三个可选 **credibility signals**：
  - `author`（actor 约定的身份）
  - `usage_count`（在 `usage_window` 内被行使次数——dashboard 查看、查询执行、页面阅读；定位是 liveness/趋势信号而非精确分数）
  - `last_modified`（来源自身最后变更时间）
  - `usage_window` 写在 `sources` 旁，`{ from, to }` 时间范围，单 entry 可覆盖。
- **关键设计决策：记录信号，不记录可信度分数**。原文理由：分数是主观的、跨 consumer 不可移植、写下即过时。可信度由消费方从信号推断。
- **Per-claim 归属**：markdown footnote 的 label = `sources[].id`（如 `[^ga4-schema]`），consumer 通过匹配 entry 解析归属，不解析 footnote 散文。原文明确解释为何用稳定 `id` 而非位置索引（`sources[0]`）：agents 会不断重写文档，列表一旦重排，位置索引会静默错归，稳定 id 则能存活。

**Trust：`generated` 与 `verified`（§5.2-5.3）**：

- `generated: { by, at }`：当前内容如何产生、最后有意义变更何时。刻意与 `verified` 分离——写的人不必是确认的人。
- `verified: [{ by, at }, ...]`：独立确认事件列表（人工签核 + 夜间流程可并存）；单映射视为单元素列表（consumer MUST 兼容）。
- **Trust tier（consumer 从 `verified` 推导，advisory 而非访问控制）**：
  - 无 `verified` 键 ⇒ unverified
  - 仅非 `human:` actor ⇒ machine-confirmed
  - 含 `human:<id>` actor ⇒ human-reviewed
- Actor 约定（§7）：agent/工具用 `<producer>/<version>`（如 `reference_agent/gemini-2.5-pro`），人用 `human:<id>`，自动化进程用 `process:<id>`。信任分类靠 `human:` 前缀。

**Lifecycle（§5.4-5.5）**：

- `status: draft | stable | deprecated`（缺省 = stable）
- `stale_after`：**绝对时间点**而非相对 TTL，明确理由：staleness 退化为一次纯日期比较，无需引用读取时刻——"exactly the kind of determinism a non-LLM consumer wants"。

**Attested Computation（§10，v0.2 新概念类型）**：

- 解决的问题："provenance 回答 claim 从哪来；attestation 回答这个数字是否按规定的方式产出"（agent 是否即兴写了自己的 SQL）。
- 一个 computation 是独立 concept（`type: Attested Computation`），需要该值的 Metric/Table 用普通 markdown link 引用它。三个动机：`runtime` 定义 `parameters` 语义；一个 computation 多处复用；信任状态按 computation 独立（revenue 新鲜而 profit 过期可并存）。
- 合约字段：`runtime`（必填，如 bigquery/postgres/dbt/python/Looker）、`parameters`（typed named holes，`{name, type, required}`）、`computation`（指向文件的路径，缺省用 body `# Computation` fence）、`executor`（`resource` + `receipt` 声明）、`attester`（`resource` 指向确定性无 LLM 代码）。
- 运行机制（§10.5，informative）：agent 只能给声明过的 `parameters` 填值，**不得编写或修改 computation**；executor 运行绑定后的 computation 并返回 receipt（如 BigQuery `job_id` + `executed_sql` + result）；attester 在消费方运行，检查 receipt——"实际跑的查询 == 声明的 computation + 声称的参数"（比较在展开/编译后的工件上进行，改写查询、换 computation 文件、篡改依赖都会 fail）；失败时拒绝展示该值。
- **verification ≠ attestation**（§10.6）：`verified` 确认定义仍符合策略（doc 级、慢、存于 bundle）；attestation 确认单次运行正确（per-call、runtime、永不存入 bundle）。过期的定义仍可 attest 通过；刚 verified 的定义每次运行仍需 attestation。
- receipt/verdict 是 runtime 工件，**不存入 bundle**；OKF 只记录 computation 与检查方式，自己不执行任何东西。

**交叉链接与路径（§6）**：

- 概念间用标准 markdown link；推荐 bundle 绝对路径（`/` 开头，文档在子目录内移动时稳定）；相对路径亦支持。
- 链接表达"存在关系"，具体种类（parent/child、references、joins-with）由周边散文传达；图视图通常把所有链接当无类型有向边。
- **broken link 不算 malformed**——"it may simply represent not-yet-written knowledge"（未写出的知识）。
- `references/` 子目录约定：镜像外部材料/运行指令/代码为 bundle 内一等公民（executor/attester 常指向它）。

**Conformance（§11）**：三条硬性要求——非保留 .md 文件有可解析 YAML frontmatter；frontmatter 有非空 `type`；保留文件遵循 §8/§9。同时 consumer **不得**因以下原因拒绝 bundle：缺可选字段、未知 type、未知附加键、断链、缺 index.md。

**Versioning（§12）**：`<major>.<minor>`；minor 向后兼容新增，major 可破坏。`okf_version: "0.2"` 声明在 bundle 根 `index.md` 的 frontmatter（这是 index.md 唯一允许 frontmatter 的地方）。

**v0.1 → v0.2 变化（§13）**：两个刻意 breaking rename（`timestamp` → `generated.at`；body `# Citations` 列表 → frontmatter `sources`，v0.2 consumer 可回退读 v0.1 形式）；其余全部 additive。**Deferred**：receipt/verdict wire format、attester ABI/可移植性/沙箱、attestation 缓存、语义层模板（Looker/dbt，比较从 SQL 等价转向 model-and-binding 等价）。

**v0.2 博客补充的生态信号**：发布后社区已提交 extension proposals——typed relationship edges、agent-routing hint fields、optional erasure conformance profile、`.okfignore` 约定；另有新样例 bundle 与"OKF 生态工具目录（Google 之外）"。v0.2 同步更新：reference_agent 生成时即产出 provenance/trust 字段；可视化器显示 trust tier/status/staleness；Knowledge Catalog round-trip demo。

### 1.4 OKF 与 Karpathy LLM Wiki 模式的逐项对应

| Karpathy 模式要素 | OKF v0.2 对应 | 备注 |
| --- | --- | --- |
| raw sources（不可变，人写 LLM 读） | 无直接对应物；`sources[].resource` 指向 bundle 外部材料；`references/` 约定可镜像 | OKF 是"已编译知识"的交换格式，原始层留给 producer |
| wiki（LLM 生成维护，LLM 写人读） | bundle（concept documents 目录树） | 基本同构 |
| index.md（内容目录，查询入口） | `index.md`（§8，任意层级，progressive disclosure） | 几乎逐字对应；OKF 允许 consumer 现场合成 |
| log.md（append-only 时间线，`## [YYYY-MM-DD] 操作 | 标题`） | `log.md`（§9，`## YYYY-MM-DD` 分组 + 粗体动词惯例） | 格式细节不同（Karpathy 前缀更结构化便于 grep），语义相同 |
| schema 层（AGENTS.md 类约定，人与 LLM 共同演化） | SPEC.md 本身 + `openwiki/INSTRUCTIONS.md` 类 per-bundle 约定 | OKF 把"共识"提升为跨厂商规范 |
| Ingest 操作 | producer / reference agent / enrichment agent | OKF 只定格式不定 runtime |
| Query 操作 | consumer（agent、UI、搜索索引、确定性代码） | 同上 |
| Lint 操作 | conformance（§11）+ trust/lifecycle 字段使矛盾/过时可机检 | OKF 无专门 lint 章节，但字段设计为 lintable |
| Memex 思想源头 | 未提及 | Google 叙事接的是企业数据目录谱系（Dataplex） |

**判断**：OKF 是 Karpathy 模式的"子集+企业化扩展"——三层架构中的 wiki 层被完整标准化并加上 trust/provenance/attestation 四族字段；raw 层与人机分工被抽象为 producer/consumer 独立性。个人知识库项目若产出 OKF 兼容 bundle，即可免费接入 Google Catalog、OpenWiki 等消费端。

---

## 2. LangChain OpenWiki 系 —— 标准化最积极的采纳方

### 2.1 GitHub 仓库现状（github.com/langchain-ai/openwiki）

| 项 | 数值（2026-11-04 抓取） |
| --- | --- |
| Stars / Forks / Commits | 17.7k / 1.3k / 511 |
| License | MIT |
| 技术栈 | TypeScript，Node.js ≥ 22.22.0，基于 deepagentsjs（Deep Agents） |
| 定位（About） | "OpenWiki is a CLI that writes and maintains agent documentation for your codebase" |

**双模式**：

| 模式 | 文档化对象 | 写入位置 | 启动命令 |
| --- | --- | --- | --- |
| Code（默认） | 当前仓库 | 仓库内 `openwiki/` | `openwiki --init` |
| Personal | 已连接的外部来源 | `~/.openwiki/wiki` | `openwiki personal --init` |

**OKF 采纳（关键事实）**：README 明确声明"OpenWiki emits Google Open Knowledge Format (OKF) v0.2 bundles **in both modes**"——即 LangChain 已把 OKF v0.2 作为输出格式，覆盖代码库与个人双场景。

**Grounded Claims 架构**：
- 每个 repository page 的事实以 **Claim** 追踪，Claim 指向版本化 source evidence，如 `repo://src/server.ts#L40-L82`；
- Claim sidecar 存于 `openwiki/.claims/`，与 Markdown 一起版本化（"evidence travels with the wiki"）；
- 证据行变更 → hash 变化 → OpenWiki 无需模型调用即可标记受影响 claims（省 token、staleness 检测确定性化）；只有受影响 claims 送模型确认/修订/撤销（对应博客 "self-correcting memory in OpenWiki"）；
- 注意限制：Claims 目前仅覆盖仓库代码 wiki；connector 来源的事实（含 LangSmith 观察）不建 claim。
- Claims 与 OKF 的关系（README 图示标题原文）："OpenWiki Claims reconcile code evidence into OKF page-level trust metadata"。

**生成架构（可恢复性设计）**：有序 page job 队列；`openwiki/.run.json` checkpoint 活跃运行与进度；一个 page 只有在 Markdown、Claims、verification、`openwiki/.page-manifest.json` 条目全部落盘后才算完成——中断后已完成工作得以保留。原生 CLI 支持并行 page worker（`OPENWIKI_PAGE_CONCURRENCY`，1–8，默认 1）。

**检索工具**：`openwiki_search`（紧凑排序结果）+ `openwiki_read`（完整 section）——本地、只读、**model-free**（不启动生成、不自行调模型）。定位是"具体问题时的可选上下文，不是每个任务的例行步骤"；无索引时 fallback 到 `openwiki/quickstart.md`。

**编码代理集成（10 家）**：Codex、Claude Code、OpenCode、Cursor、IBM Bob/Bob Shell、Kiro、Oh My Pi、Antigravity、GitHub Copilot CLI、Pi。利用宿主已认证的模型会话，无单独 provider 配置。

**模型提供商（15 家）**：默认 OpenAI `gpt-5.6-terra`；含 Anthropic、Gemini（AI Studio/Vertex）、Bedrock、Copilot、OpenRouter、OpenAI-compatible（LiteLLM/Ollama/LM Studio）等。凭据存 `~/.openwiki/.env`。

**Connector（9 个）**：Personal 模式内置 Custom MCP、本地 git 仓库、Notion、Gmail、X/Twitter、Web Search、Hacker News、Slack（需 OAuth+HTTPS callback）；LangSmith connector 特殊——feed Code 模式（拉运行时 trace 补充代码文档）。

**其他工程细节**：`openwiki link` 建 named workspace 跨仓库搜索（MCP 下 `openwiki_list_workspaces`/`openwiki_list_wikis`）；`openwiki visualize` 交互图 + 实时 Markdown reader，可导出静态单文件；`openwiki/INSTRUCTIONS.md` 用户自写、运行中永不重写（对应 Karpathy 的 schema 层人机分工）；根 `AGENTS.md` 维护（只重写 `<!-- OPENWIKI:START/END -->` 块）；`.openwikiignore`（glob + `!` 否定，是读取边界：被忽略路径不被读/扫/复现）；Mermaid 图按需嵌入并随 update 同步；CI 模板覆盖 GitHub Actions（含 auto-merge 变体）/GitLab CI/Bitbucket Pipelines；遥测匿名聚合、`OPENWIKI_TELEMETRY_DISABLED=1` 或 `DO_NOT_TRACK=1` 关闭。

### 2.2 Wiki Memory 概念文章（Harrison Chase，2026-06-30）

来源：https://www.langchain.com/blog/wiki-memory

- 核心定义："wiki memory = 用 agent 把 raw source data 转成 compact, persistent, agent-readable 知识层"。
- 与 RAG 的本质区别（原文）："RAG usually retrieves raw chunks at query time. A wiki precomputes and maintains a higher-level synthesis, so the agent does not have to rediscover the structure every time."
- **谱系梳理（LangChain 官方叙事）**：DeepWiki by Cognition（"probably the first example"）→ Karpathy LLM Wiki（更一般形式：不限代码、任意 source files、LLM 增量构建持久 markdown wiki 坐在用户与 raw sources 之间）→ Factory AutoWiki（DeepWiki 同类）。与之相邻的 memory 系统：LangMem、Letta、Mem0、Zep——攻击更广的 agent-memory 问题，而 wiki memory 的显著特点是"uses the simplest possible substrate: files"。
- 四个开放问题的"正在浮现的共同答案"：raw data = anything an agent can read or access；格式 = files；压缩 = agent；维护 = agent。
- 边界（重要，防过度宣称）："Wikis are not all of memory. They are best for durable domain knowledge, not necessarily short-term conversation state, user preferences, or high-frequency event logs."
- 值得注意：文中举的用例是研究公司"clone researchers' brains"（从实验、笔记、行动近似复制离职风险知识）——与个人知识库场景高度同构。

### 2.3 Evidence-Grounded Agent Memory 实证（Eugene Liu，2026-10-28）

来源：https://www.langchain.com/blog/building-agent-memory-openwiki-graphs

**实验设计**（方法论可复用）：
- 语料：合成保险文档库 **111 篇长文档**（选保险因为 policy/endorsement 频繁 reference/amend/override 彼此）。
- 评分基础：**972 条事实的 ledger**，控制每条事实出现位置、文档互引、版本间变化；LLM 生成周边散文 + 自动检查事实在场。
- 语料刻意污染：过时版本、矛盾、间接引用链、措辞差异、超长文档。
- 对照：同一 retrieval agent 两种条件——Search（原文档关键词搜索）vs Wiki（同一 agent + OpenWiki 编译的带源链接 wiki）；模型/指令/文档/问题全部不变。
- 题目：80 道简单查找 + 50 道跨文档连接题；每题问 3 次测 run-to-run 变化。
- 指标：accuracy（0–1，grader 对照 972-fact ledger checklist）、citation consistency（三次运行引用证据集合的平均 pairwise Jaccard）、cost + latency。

**核心数字**：

| 指标 | Search | Wiki | Wiki + Evidence Graph |
| --- | --- | --- | --- |
| 连接题 accuracy | 0.10 | 0.52（≈5x） | 再 +27%（约 0.66） |
| 连接题 citation overlap | — | 0.25 | 翻倍（约 0.5） |
| 每正确答案成本（连接题） | ~$0.55 | ~$0.19 | 再 -58%（约 $0.08） |
| 简单查找 accuracy | 0.84 | 0.83 | — |
| 简单查找 citation overlap | 0.72 | 0.74 | — |
| 简单查找每正确答案成本 | $0.020 | $0.021 | — |
| 简单查找延迟 | 9s | 12s | — |
| 连接题中位答题时间 | — | — | -40% |

**编译成本（ingest vs 检索的权衡数字，直接回答调研提纲关注点）**：
- 111 文档全量编译为约原文 **1/10** 大小的 wiki：**$4.15**；
- 后续增量添加 17 篇文档：约 **$0.09/篇**；
- 明确声明：以下分析**不含**编译与更新成本，只报检索与答题成本。

**Evidence Graph 架构**：
- 两步构建：① 确定性过程把每篇文档切分为 paragraph 并赋唯一 ID（paragraph 成为信息原子，claim 连到精确段落而非整篇文档）；② typed edges 连接段落/claims/wiki 页——claims `cite` 段落、新文档 `supersede` 旧文档、section `refers_to` 其他文档。边列表还包括 `amends`、`attaches_to` 及其逆向。
- **构建无需额外模型调用**（复用 wiki 已有的文本引用与文档引用确定性提取），构建耗时 **<1 秒**，解决库内全部显式交叉引用。
- 定位（与 GraphRAG 的区别，原文）："The graph's job is evidence navigation, not modeling everything the organization knows... unlike an extraction-heavy knowledge graph pipeline, this layer reuses existing references and citations rather than extracting and reconciling entities with a model."
- 两个导航工具：`locate`（匹配问题词到标题/heading/wiki 页/claim 陈述，找起点）、`expand`（打开一个节点列出 typed edges；单路径自动跟随，分支处交 agent 选择）。模式上类比 Microsoft GraphRAG 的 locate-gather。

**结论（原文要点）**：
- "The strongest case for a compiled wiki is repeated cross-source reasoning."
- 简单查找不值得：search alone 同样准确且更快，尤其企业规模下 ingestion + 维护成本可能超过检索节省。
- "With enough reuse, savings from avoiding repeated context reconstruction can offset the cost of building and maintaining memory." —— 复用频次是 wiki 值不值的关键变量。
- 后续方向：按需动态编译（只为跨源问题所需上下文编译，而非整个仓库）；claims + typed edges 作为 semantic/episodic/procedural memory 的接地基础。

### 2.4 WikiBench 评测基准（Nick Hollon）

来源：https://www.langchain.com/blog/evaluating-openwiki-with-wikibench

**框架**：
- 构建于 Harbor（评估长任务 agent 的框架，三组件：environment / agent / verifier）。
- environment = pinned commit 的仓库；agent = 跑 OpenWiki 初始化产出 wiki；verifier = **"reader agent"** 用 wiki（有时配源码）回答关于仓库的问题——以"wiki 实际帮助了什么"来评判 wiki 质量。
- 问题两类，自动生成：**coverage** 问题（共享模板："I need to make a change to how [area] works. Where does that live..."）与 **retrieval** 问题（围绕具体行为单独撰写）。
- 评分：每题配 JSON rubric（应包含的事实清单）；两级 LLM judge——一个查事实是否在答案中，另一个查该事实是否 grounded 于 agent 实际读过的页面（"正确且 grounded 才给分"）；总分 = 命中事实比例（例：期望 5 得 3 = 0.6），wiki 分 = 所有答案均分。

**结果（可引用数字）**：
- Harness 对比（同一模型 Luna）：Bare DeepAgents < OpenWiki 0.2.5 < OpenWiki 0.3.0。0.3.0 的提升主要来自 coverage 题（归因于 system prompt + 专用 planning subagent）；retrieval 题提升小（因为没怎么改 page authoring）。
- 模型对比（OpenWiki 0.3.0）：**DeepSeek Flash 与 GLM 5.2 表现最好**，但 DeepSeek Flash 约为 GLM 5.2 成本的 **1/6**；成本区间 $9.18（GLM 5.2）vs $0.44（Luna）；时间 11 分钟（Terra）到 50 分钟（GLM 5.2）。
- 行为差异：DeepSeek/GLM 读取约 **3 倍**文件，但只多写 **1.2–1.5 倍**页面——额外工作花在理解仓库而非产出更多输出。
- **wiki 是否有用（三设置对比）**：reader agent 仅 wiki / 仅源码 / 两者兼有 → **wiki + source 平均分最高且成本低于仅 source**；仅 wiki 明显最差。结论原文："The wiki acts as an index... it works best as a guide rather than a replacement for the source."（wiki 是索引/指南，不是源码替代品——与 evidence graph 博客"简单查找不值得"互相印证。）

### 2.5 OpenWiki Brains 发布（Brace Sproul，2026-07-10）

来源：https://www.langchain.com/blog/introducing-openwiki-brains-general-purpose-wiki-memory-for-agents

- OpenWiki 0.1.0 引入 Personal Brain：连接 Gmail、Notion、git 仓库、Twitter/X、Hacker News、Web search（Slack 当时 coming soon），转为本地 wiki 供 agent 用作记忆。
- **proactive vs reactive memory 的区分（定位声明的核心）**：Claude/ChatGPT/LangSmith Fleet 内置记忆是 reactive——记住你明确告诉它的；OpenWiki Brain 是 proactive——主动从你工作的地方拉取匹配"你让它关心什么"的信息写入 wiki。
- Connector 二分法：确定性（Gmail/X/HN/git 有 feed 可拉）vs agentic（Notion/web search 无"相关物"的简单 feed，ingestion 时给 agent 工具带目标搜索）。
- 保持更新：本地运行使"staying current"实际可行——定时任务按选定节奏从 connector 拉新信息刷新磁盘 wiki，无需 server。
- 设定聚焦：setup 时询问 brain 应关注什么（默认通用个人助理 prompt，可定制为"活跃项目、AI 研究主题、客户上下文、保存的链接"）——该 prompt 决定 ingest 时保留什么。
- **格式态度的时间线（值得注意）**：此文（7 月）说 "Markdown first... formats like Google's Open Knowledge Format are all interesting directions"；而当前 README 已实现 OKF v0.2 输出——即 7 月到 11 月之间完成了从观望到采纳。
- 后续路线：更多 connector（LangSmith traces、Claude/Codex 本地会话）；更好检索（full-text、MCP、semantic、agentic search）；更好格式。

### 2.6 OpenWiki 产品定位小结

- 双定位并存：Code Brain（代码库文档，对标 DeepWiki/AutoWiki）+ Personal Brain（通用个人记忆，对标个人知识库场景）。
- LangChain 是目前 **OKF 最大的第三方采纳方**（17.7k stars 的 CLI 双模式输出 OKF v0.2），且其评测体系（111-doc 实验 + WikiBench）为"wiki vs 检索"提供了目前最透明的公开数字。
- 与个人知识库项目的重叠警告：OpenWiki Personal Brain 已覆盖 Gmail/Notion/X/HN/web search 的本地 wiki 编译，是直接竞品；但其 claims 机制目前只对 repo evidence 生效（connector 事实不建 claim），个人模式的 trust/provenance 深度弱于 code 模式——这是可差异化的技术缺口。

---

## 3. 腾讯 WeKnora

来源：https://github.com/Tencent/WeKnora

### 3.1 基本盘

| 项 | 数值（2026-11-04 抓取） |
| --- | --- |
| Stars / Forks / Commits | 36.4k / 5.0k / 3,928 |
| License / 语言 | MIT / Go（后端）+ 前端 |
| 定位（About 原文） | "Open-source LLM knowledge platform: turn raw documents into a queryable RAG, an autonomous reasoning agent, and a self-maintaining Wiki" |
| 当前版本 | v0.9.0（2026-10-29 发布） |
| 官网/文档 | weknora.weixin.qq.com（文档中文，约 360 个 API 端点、约 150 个环境变量） |

### 3.2 架构与三模式

- **三种模式共享同一知识库**（README 原图说明）："Use RAG to look things up, the agent for multi-step tasks, and the wiki to organize knowledge. All three work on the same knowledge bases." 这是与 OpenWiki（wiki 为中心）根本不同的产品哲学——RAG 仍是并列一等公民。
- **Wiki Mode 细节**："With Wiki enabled, WeKnora extracts people, products and concepts from knowledge-base documents into pages with source citations, organized by directory. The knowledge graph shows how pages relate; pages can be edited directly and every change can be rolled back."（Features 表补充：revision diff and rollback；v0.8.3 加 wiki graph 的 group layouts/theme captions。）
- **多工作区 RBAC**：四角色、per-resource ownership、per-workspace audit log；scoped API keys + principal 模型；OIDC、AES-256-GCM 凭据加密、SSRF 安全出站（whitelist-only 模式）。
- **MCP**：v0.8.2（2026-09-24）起内置 MCP Server——per-workspace `/mcp/<endpoint_id>` 端点、Streamable HTTP、每端点独立 token/知识库范围/速率限制/工具组；此前 Python `mcp-server/` 已废弃。另有 agent-first CLI（`weknora mcp serve`，命令默认输出稳定 JSON envelope）。
- **Agent 能力**（v0.8.0–v0.9.0 演进）：ReAct agent；ClawHub/SkillHub/Git/ZIP 安装 skills；session-persistent Docker/E2B/Cube 沙箱（含交互终端与图形桌面）；BrowserSkill 扩展驱动用户自己的 Chrome/Edge（登录/验证码交还人工）；跨会话长期记忆（profile/preference/fact/task/interest，用户确认后自动提取 + `search_memory`）；v0.9.0 加多 agent 协作、Automations（一次性/循环任务）、执行权限三档（read-only / confirm-before-change / automatic-write）。
- **检索栈**：关键词 + 向量混合搜索、rerank、parent-child chunking、GraphRAG（Neo4j profile）；端到端评估含 recall 与 BLEU/ROUGE。
- **规模数字**：29 家内置 LLM 供应商；向量库 8 种（pgvector+ParadeDB / ES / OpenSearch / Milvus / Weaviate / Qdrant / Doris / 腾讯 VectorDB）；数据源 11 种（飞书 wiki/Drive、Confluence、GitLab、腾讯 IMA、Notion、语雀、钉钉文档、Seafile、RSS）；IM 渠道 10 种（企微、飞书、QQBot、Slack、Telegram、钉钉、Mattermost、微信、云之家）；Web 搜索 14 家；文档格式 13+（anydoc 进程内解析 Office）。
- **部署**：Docker Compose / K8s Helm / Lite 单二进制（SQLite+内存队列）/ 桌面应用（macOS 沙箱）；离线与私有云安装；UI 五语言。

### 3.3 与个人知识库场景的匹配度判断

**匹配点**：
- 中文生态最强：飞书/语雀/钉钉/企微/腾讯 IMA 全覆盖，文档站点中文，对中文用户的开箱体验没有对手；
- "文档进、wiki 出 + 可编辑 + diff + 回滚"符合 Karpathy 模式的人机分工（LLM 写、人可改）；
- Lite 单二进制与桌面应用降低了个人自部署门槛；
- MCP Server + CLI + Chrome 扩展 + 微信小程序构成多端消费面。

**错配点（对"普通用户个人知识库"）**：
- 企业平台基因：多工作区 RBAC、审计日志、任务队列治理、Langfuse 追踪——360 个 API 端点/150 个环境变量的运维复杂度远超个人场景需要；
- **Wiki 不是中心而是三模式之一**：RAG（分块+向量+rerank）是主检索路径，wiki 是"文档组织视图"——与 Karpathy"知识编译一次、检索复利"的论点路线不同，更接近"RAG 平台长出了 wiki 功能"；
- 未提 OKF 采纳（README 无相关字样）；wiki 页面存于平台数据库而非用户可直接 git 管理的 markdown bundle——"知识可携带性/所有权"弱于 OKF 阵营；
- 组件规模（5 个 docker 服务起步）对非技术用户仍重。

**中文生态地位**：36.4k stars 使其成为中文世界该赛道事实上的头部开源项目（作为对照，OpenWiki 17.7k、Dify 级别的关注度）；其 v0.9.0 的"平台内 assistant 可代你建 agent/排任务/管知识"方向显示它在向 agentic 平台演进，而非向"轻量个人 wiki"演进——为轻量个人项目留出了空间。

---

## 4. 其他大厂信号（快速定位确认）

### 4.1 Microsoft llmwiki —— 最贴近 Karpathy 原教旨的实现

来源：https://github.com/microsoft/llmwiki

| 项 | 数值 |
| --- | --- |
| Stars / Forks / Commits | 104 / 17 / 250 |
| License | MIT（Copyright Microsoft） |
| 形态 | VS Code 扩展 + npm 包（`llmwiki` + `@llmwiki/core` monorepo） |
| 依赖 | Node ≥ 20、VS Code ≥ 1.101、**GitHub Copilot 订阅**（用 VS Code Language Model API 做 ingestion enrichment） |
| 默认模型 | `claude-opus-4.6`（Copilot 家族，可交互选择） |

- 定位原文："A personal knowledge base where the LLM does all the maintenance... Instead of retrieving from raw documents at query time (like RAG), the LLM incrementally builds and maintains a persistent wiki"——README 直接复述 Karpathy 的 RAG 对比。
- **三层架构逐字对应 Karpathy**：Raw Sources（Human 所有，不可变，LLM 读不写）/ Wiki（LLM 完全所有）/ Schema（`AGENTS.md`，Human+LLM 共同演化）。`llmwiki.init` 脚手架 `.wiki/` 目录（raw、wiki、index、log、AGENTS.md）。
- 功能面：侧边栏四视图（**Entities / Concepts / Raw Sources / Backlinks**）；12 个命令（init/ingest/query/status/openPage/search/searchRaw/refresh/fix/removeSource/scanRaw/selectModel）；`@wiki` chat participant（`/status` `/save`（答案存回 wiki 页，即 Karpathy 的 Query 复利）/lint /fix）；批量 ingest 四种入口（palette/右键/工具栏/拖入 `raw/` 自动 file-watcher ingest），>20 文件触发确认；lint 含孤儿页清理。
- **MCP Server**（`@llmwiki/core` 的 `llmwiki-mcp` stdio launcher）：7 个读工具（wiki_status/query/lint/list_pages/list_sources/read_page/read_index）+ 7 个写工具（write_page/create_entity/create_concept/update_page/add_crosslinks/update_index/ingest_with_context）+ 3 个 prompts（ingest-and-integrate、lint-and-fix、research-topic）+ resources（`resource://wiki/index|pages|sources` 及模板）——外部 agent（Claude Desktop/Cursor/Copilot）可编程读写维护 wiki。
- 判断：这是**微软对 Karpathy 模式的直接背书实现**（连 AGENTS.md schema 层都照搬），但分发形态绑死 VS Code + Copilot 订阅，star 数小（104）说明尚是实验性项目而非战略产品；其"扩展内嵌 + MCP 外露"的双消费面设计值得借鉴。

### 4.2 Vercel openwiki（vercel-labs）

来源：https://github.com/vercel-labs/openwiki

| 项 | 数值 |
| --- | --- |
| Stars / Commits | 146 / **1**（单 commit，实验性质） |
| 形态 | Next.js app + eve agent；线上 openwiki.sh；一键 Deploy to Vercel |
| 存储 | Neon Postgres + Vercel Blob |
| 模型默认 | `openai/gpt-5.5`（索引/生成，"用你负担得起的 strongest model"）+ `openai/gpt-5.4-mini`（轻量 app agent） |

- 定位："Generate a living, source-grounded wiki for any GitHub repository"——托管版 DeepWiki 类（仓库文档），**刻意拒绝私有仓库**（公共部署上）。
- 生成流水线 8 阶段：fetch 仓库元数据 → 读高信号文件（README/package 元数据/docs/配置/入口）→ 发现第一方官方文档索引 → eve 规划 docs 式 outline → 规范化 outline → 逐页生成（带 source path 与结构化引用）→ **确定性质量检查**（深度、引用、source-path 有效性、导航形状）→ 原子发布 revision（新 wiki 就绪前旧版保持可见）。
- 自适应页面预算：docs 重的框架可达 **50+** source-backed 页；页面数留给真实读者主题而非逐文件清单。
- 保新鲜：每日 eve schedule（对比 published commit SHA 与 generator 版本；featured 仓库优先；手动触发 API）；未来 GitHub App webhook。
- 判断：与个人知识库无直接竞争（面向公共仓库文档的托管演示）；其贡献在于把"确定性质检 + 原子发布 + 失败不覆盖上一版好 wiki"这些工程实践做成了可抄的样例。

### 4.3 Pinecone Nexus —— 商业公司对"编译知识"论点的验证

来源：https://www.pinecone.io/blog/introducing-nexus-knowledge-engine/（Jeff Zhu & Siva Ragavan，2026-05-04；文首更新注记：**Nexus 已 GA**，另有 GA 公告）

- 品类宣言："Most agent failures are data failures, not model failures"；提出 **Knowledge Engine** 新品类（vs 手工 per-domain 建 context 层）。
- 四原语（逐层组合）：**Artifact**（typed、governed、为具体任务构造的信息块）→ **Context**（为角色/团队/工作流策划的 artifact 集）→ **Knowledge**（全公司 contexts 总和）→ **Knowledge Engine**（构建并服务上述全部的系统）。
- **Context Compiler**：核心是自主 coding agent，配三样东西——每 domain 的 eval set（代表性任务+已知正确答案）、预审 skills 库（文档处理/实体抽取/分块）、按 eval 信号打分的反馈环。每轮迭代修改 `curate()`（artifact 构造）与 `query()`（知识检索）两个函数并跑 eval。早期 design partner 数据：新 domain 的 Context 交付**数天而非数月**。
- **KnowQL**（声明式知识查询）：四成分——Intent（问题/响应形状/作用域 Contexts，可跨 Context 组合）、Filter（确定性谓词 + 访问控制策略，agent 只见调用方被允许见的）、Provenance（**字段级引用 by construction，事后不重建**）、Control（深度/延迟预算，成本以 outcomes 声明而非 tokens）。
- **KRAFTBench 数字**（其自建基准，方法论对个人项目可参考）：
  - 语料：493 份 S&P 500 公司 2022 年 10-K（每份约 500KB，共约 245MB）；150 道难题（9 行业 × 10 金融主题；三种难度形状：multi-fact / multi-company / multi-step）；每题约束 120 秒 + 1M tokens；统一 composer 与裁判均为 claude-sonnet-4-6。

  | 机制 | Completion | 平均延迟 | 平均准确率 | 平均 tokens | 平均 steps |
  | --- | --- | --- | --- | --- | --- |
  | Pinecone Nexus | 100%（150/150） | 22.7s | 0.680 | 6,733 | 1.69 |
  | Agentic RAG | 98.7%（148/150） | 37.9s | 0.413 | 49,103 | 7.77 |
  | Coding agent | 62.7%（94/150） | 84.1s | 0.585 | 528,301 | 14.77 |

  - token 成本约 **7x** 优于 RAG、**80x** 优于 coding agent。
  - 失败模式（trace 级）：RAG 把问题分解为 18 个事实但"金额与 chunk 不同处"导致漏检（数据存在却标为缺失）；coding agent grep 出数百个匹配耗尽 1M token；Nexus 用预编译公司级 fact-sheet artifact 单遍组合答案。
- 生态管道：Box（源 + ACL）→ Unstructured（解析 + 权限元数据）→ Nexus（artifact 层 + KnowQL 查询面）。
- 判断：**商业世界独立复现了 Karpathy 的核心论点**（编译一次 vs 查询时重组），且给出了目前最完整的端到端量化对比；但方向是企业级闭源托管（Box/权限/治理），与个人知识库无产品竞争，其 KnowQL 的"声明式查询 + by-construction 溯源"与 OKF 的"frontmatter trust + attested computation"是同一问题的两种解法，值得跟踪二者是否合流。

### 4.4 YANP（Yet Another Notes Project）规范 v0.2 Draft

来源：https://spinchange.com/yanp/（2026-03，个人项目 by spinchange / github.com/spinchange）

- 定位："a plain-text, tool-agnostic format for personal knowledge vaults"——**个人笔记 vault 规范**，与 OKF（agent 知识交换）是不同生态位的最小规范尝试。
- 核心规则：`.md` UTF-8、LF（读容 CRLF 写归一）、lowercase kebab-case 文件名且 vault 内大小写不敏感唯一；YAML frontmatter 可选、全字段可选、未知字段必须保留。
- **"Frontmatter is written once"原则**（与 OKF 的显著分歧）：字段在写作时设置、不覆写（更正除外），"temporal evolution belongs in appendices, not in frontmatter rewrites"。
- 字段集：`tags`/`author`（claude、gemini、codex 或人名）/`hostname`/`date`/`status`（draft·active·archived）/`title`/`aliases`/`priority`/`due`/`scheduled`/`project`。
- **双标签体系**：frontmatter tags 是机器写的、inline `#tags` 是人写的，工具合并两者，`author` 字段预测哪种风格——把 Karpathy 的"人写 raw、LLM 写 wiki"分工延伸到了元数据层。
- Wikilink 解析：`[[Note Title]]` 按 title → aliases → filename stem 三级（大小写不敏感）；路径前缀消歧；**rename 必须自动重写全部入链**；delete 前必须警告入链数；发布时 wikilink → 相对链接转换且**源文件永不修改**。
- 文件夹约定：`daily/`（YYYY-MM-DD.md）、`weekly/`、`monthly/`、`assets/`、`templates/`；保留 `inbox.md` 为默认捕获目标。
- 合规工具：YANP app（单文件浏览器编辑器）、jot（Python 参考实现）、minimal-notes（PowerShell 7）、Obsidian/Zettlr（原生 wikilink）、Quartz（SSG 直接支持）。
- 判断：单人维护的 Draft 规范、无大厂背书，但它是"**个人 vault 互操作**"这条 OKF 不覆盖的缝隙里最完整的文本规范（周期笔记、任务字段、wikilink 语义、重命名/删除的 UX 契约）；对本项目的价值是 frontmatter 最小集 + 人机字段分工 + vault 操作行为规范的参考，而非采用对象。

---

## 5. 横向对比与对本项目的启示

### 5.1 OKF 采纳现状（标准化收敛的直接证据）

| 主体 | 角色 | OKF 关系 |
| --- | --- | --- |
| Google Cloud | 规范作者 + Knowledge Catalog 消费端 | v0.1（2026-06-13）→ v0.2（2026-07-25）；Catalog ingest + round-trip |
| LangChain OpenWiki | 17.7k star CLI，最大第三方 | 双模式输出 OKF v0.2 bundle；Claims 证据对账到 OKF trust 元数据 |
| Microsoft llmwiki | VS Code 扩展 | 未提 OKF；自有 .wiki/ 结构（raw/wiki/index/log/AGENTS.md），与 OKF 形态高度兼容但未声明 |
| 腾讯 WeKnora | 36.4k star 平台 | 未提 OKF；wiki 存平台数据库，非可携带 markdown bundle |
| Vercel openwiki | 托管仓库 wiki | 未提 OKF |
| YANP | 个人 vault 规范 | 平行规范，无交集 |
| Pinecone Nexus | 商业 Knowledge Engine | 未提 OKF；走自有 KnowQL/artifact 路线 |

**结论**：OKF 在 5 个月内完成"Karpathy gist → Google 规范 → LangChain 双模式默认输出"的链条，是当前唯一有跨大厂采纳势头的格式标准；但采纳方集中在"文档/wiki 编译器"一侧，平台型（WeKnora）与商业引擎（Nexus）仍在自有格式上。**"产出 OKF 兼容 bundle"是个人知识库项目免费获得互操作性的最低成本路径**。

### 5.2 实证数字汇总（所有可引用的评测结果）

| 实验 | 对比 | 结果 | 来源 |
| --- | --- | --- | --- |
| LangChain 111-doc 保险库 | wiki vs search（连接题） | 准确率 0.10→0.52（≈5x）；每正确答案 $0.55→$0.19 | evidence-graph 博客 |
| 同上 | + evidence graph | 准确率再 +27%；citation consistency ×2；中位时长 -40%；每正确答案成本 -58% | 同上 |
| 同上 | 简单查找（对照） | 0.84 vs 0.83——wiki 无优势且慢（9s→12s） | 同上 |
| 同上 | 编译成本 | 111 文档 $4.15（产出 1/10 体积 wiki）；增量 $0.09/篇 | 同上 |
| WikiBench | wiki+source vs 仅 source vs 仅 wiki | 前者最高分且更省；仅 wiki 最差（"guide not replacement"） | wikibench 博客 |
| WikiBench | 模型对比 | DeepSeek Flash ≈ GLM 5.2 质量、1/6 成本；全程 $0.44–$9.18、11–50 分钟 | 同上 |
| KRAFTBench | Nexus vs Agentic RAG vs coding agent | 0.680/0.413/0.585 准确率；22.7/37.9/84.1 秒；tokens 6,733/49,103/528,301 | Pinecone 博客 |

两套独立实验（LangChain 与 Pinecone）在"**预编译知识显著优于查询时检索（对跨源问题），简单查找不值得编译**"上互相印证——这是本调研目前最重要的可复用结论，且两家都量化了编译成本（$4.15/111 文档 vs "数天而非数月"）。

### 5.3 定位地图（大厂/商业公司动向一览）

| 产品 | 主体 | 场景重心 | 部署形态 | 对个人知识库项目的意义 |
| --- | --- | --- | --- | --- |
| OKF | Google | 标准层 | 规范文本 | 底层格式选择：直接采用 |
| OpenWiki | LangChain | 代码库 + 个人双模式 | 本地 CLI / npm | 最直接竞品（Personal Brain）；claims 仅覆盖 repo 证据是缺口 |
| WeKnora | 腾讯 | 企业知识平台（RAG 中心） | 自托管服务 | 中文生态标杆；非 wiki 中心、无 OKF、运维重——差异化空间 |
| llmwiki | Microsoft | VS Code 内个人 wiki | 扩展 + MCP | Karpathy 原教旨实现；绑 Copilot；star 少，方向验证而非威胁 |
| openwiki | Vercel | 公共仓库托管 wiki | Vercel 应用 | 工程实践样板（确定性质检/原子发布/失败保护） |
| Nexus | Pinecone | 企业 Knowledge Engine | 商业托管 | 论点盟友（编译>检索）；KnowQL vs OKF 是规范竞争观察点 |
| YANP | 个人 | 个人 vault 互操作 | 规范文本 | frontmatter 最小集与人机字段分工的参考 |

### 5.4 对本项目的直接启示（要点式）

1. **格式决策基本可以定案**：跟随 OKF v0.2（type/sources/generated/verified/status/stale_after + actor 约定），它已解决"跨工具可携带 + trust 信号"两件事，且 Google↔LangChain 双向背书；YANP 的个人 vault 语义（wikilink、周期笔记、rename 重写入链）可作为 OKF 之上的薄扩展层设计参考。
2. **trust 字段设计有现成模板**：OKF 的"记录信号不记录分数"、三层 trust tier（unverified/machine-confirmed/human-reviewed）、per-claim footnote-id 归属、"stable id 而非位置索引"（防 agent 重排静默错归）都可直接沿用；LangChain 的 Grounded Claims（版本化证据 URI + hash 变更触发确定性 staleness 标记）是其工程实现版本。
3. **评测方法可复用**：LangChain 111-doc/972-fact ledger 设计与 WikiBench 的 reader-agent + 双 judge（正确且 grounded 才给分）给出了两套可照抄的评测骨架；发布任何"wiki 优于 RAG"宣称前应自建同等严谨度的评测。
4. **成本量级锚点**：编译 ~$0.04–0.09/文档（LangChain 路径），个人百文档级知识库的 ingest 成本是几美元量级——"编译贵"的批评在此规模不成立，但复用频次决定回本（LangChain 原文结论）。
5. **竞争空隙**：中文 + 普通用户 + OKF 可携带 + git 可管的组合目前无人占据——WeKnora 重且 RAG 中心、OpenWiki Personal 无中文生态且 claims 不覆盖 connector 事实、Microsoft llmwiki 绑 Copilot 且英文。
6. **规范竞争观察点**：OKF 的 attested computation vs Pinecone KnowQL 的 by-construction 溯源；OKF deferred 清单（typed edges、erasure profile、.okfignore——注意 .okfignore 已被 OpenWiki 以 `.openwikiignore` 形式先行实现）标出了标准的演进方向，跟进即可吃到向后兼容红利。
