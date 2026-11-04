# LLM Wiki 生态全景图（2026-11）

> 综合自：Awesome LLM Wiki 清单（261★，576 commits，2026-05 起）、Karpathy gist 评论区、两个 awesome 清单交叉比对。
> 深挖笔记见 `research/raw/deep-dive-*.md`（标准与大厂 / 论文 / 失败模式）。

## 1. 时间线与热度

| 时间 | 事件 |
|---|---|
| 2026-04-03 | Karpathy 发推描述 "raw data → LLM 编译 .md wiki → CLI 问答与增量增强" 工作流，170 万浏览 |
| ~2026-04 | 发布 LLM Wiki idea file（gist），7 个月内 5000+ stars |
| 2026-05 | gavischneider 开始维护 Awesome LLM Wiki；Hacker News 热帖（id 47640875） |
| 2026-05~08 | 实现爆发期：100+ 项目涌现，多为个人项目 |
| 2026-09 | LangChain 发布 OpenWiki 及 WikiBench；Google OKF v0.2 加入信任信号；Meta 工程博客披露组织级部署 |
| 2026-10 | Obelyth Cortex v2、MindBase 0.4.6、Link 5.0 等社区项目进入工程化迭代 |
| 2026-11（现在） | 生态位初步成形但高度碎片化，无统治级产品 |

## 2. 规模

- Awesome LLM Wiki 收录约 **200 条目**（去重后估计 150+ 独立项目），另有 SingggggYee/awesome-llm-knowledge-bases（41★，工具链导向）等平行清单
- 学术侧：**20+ 篇**arXiv/zenodo 论文（2603~2609 编号区间，即 2026 年 3-9 月提交），含多篇预注册实证研究
- 评测侧：WikiBench（LangChain/Harbor）、Agentic Memory Index（12 记忆架构 56 会话横评）、memory-arena 等基准出现

## 3. 生态位分类（按产品形态）

| 形态 | 数量级 | 代表 | 特征 |
|---|---|---|---|
| **Agent Skill / 插件** | ~40+ | second-brain-skill、Obsidian Second Brain、Hermes 内置 skill | 最轻量：一组 slash 命令 + schema 约定，寄生于 Claude Code/Codex/Cursor 等终端 agent |
| **CLI 编译器/守护进程** | ~30 | GBrain、scribe、Kenjaku、Patina(Rust)、Secure-LLM-Wiki | 独立编译管线，常含 cron 后台维护、Ollama 本地模型 |
| **MCP Server** | ~20 | Link、mindbase、qmd、Dexio、pie-llm-wiki | 把 wiki 作为工具暴露给任意 agent，跨客户端共享记忆 |
| **桌面应用** | ~15 | Nash Su llm_wiki(Tauri)、OpenKnowledge、Curated Thoughts、Brainstead | 面向 GUI 用户，内置人审队列与可视化 |
| **Web 应用/自托管** | ~15 | Kompl、the-curator、Silica、WikiMind、cabinet | 浏览器操作，部分含 3D 知识图 |
| **托管平台** | ~10 | WikiBrain、Dexio、Mana、wikihub.md、Agent Wikis | Git-backed 托管 + 权限/协作 |
| **框架/库** | ~15 | mykg、OpenKB、Graphify、llm-wiki-v2(CROW) | 供开发者组装管线 |
| **代码库文档生成** | ~15 | OpenWiki(LangChain/Vercel)、DeepWiki-Open、Graft、EKOS | 相邻赛道：源代码→agent 文档（DeepWiki 模式），与个人知识库部分重叠 |
| **Starter 模板** | ~15 | cerebro、Karpathy-LLM-Wiki-Stack、hippocampus(OKF) | fork 即用的目录+schema 约定 |

## 4. 标准化进程（关键变量）

- **Google Open Knowledge Format (OKF)**：v0.1（2026 前期）→ v0.2（2026-09 加入 trust signals / attested computations）。正式把 Karpathy 模式固化为厂商中立的目录结构 + YAML frontmatter 契约。LangChain OpenWiki 0.2 已采纳；expo-llm-wiki、Silica、sturlese/hippocampus 等十余项目跟进
- **YANP**（spinchange）：纯文本、工具无关的 vault 规范，势力较小
- 观察：**格式标准之争基本收敛向 OKF**，但"操作语义"（ingest/query/lint 的确切行为）仍无标准

## 5. 大厂/商业玩家

| 玩家 | 动作 | 意图解读 |
|---|---|---|
| **LangChain** | OpenWiki（**17.7k★**，Code/Personal 双模式，均输出 OKF v0.2）→ OpenWiki Brains（通用 agent 记忆）→ WikiBench（评测）→ Grounded Claims/evidence graph | 全栈卡位：格式（OKF）+ 引擎 + 基准 |
| **Google** | OKF 规范 v0.1（2026-06-13，明确声明"将 Karpathy 模式形式化"）→ v0.2（2026-07-25，trust 四族字段 + Attested Computation） | 定义格式标准，云端数据目录生态延伸 |
| **腾讯** | WeKnora（**36.4k★**，中文生态头部；RAG/Agent/Wiki 三模式共享知识库，wiki 是文档组织视图而非中心；RBAC 企业基因重；未采纳 OKF） | 企业+个人双线，对轻量个人场景错配 |
| **Microsoft** | llmwiki（104★，VS Code 扩展 + @wiki Copilot 参与者，Karpathy 三层原教旨实现） | IDE 内嵌，实验性质 |
| **Vercel** | openwiki（生成+托管+定时更新源引用 wiki） | 部署/托管层 |
| **Pinecone** | Nexus（商业知识引擎）；KRAFTBench 实证：准确率 0.680 vs Agentic RAG 0.413，tokens 省 7x；KnowQL 字段级溯源 vs OKF attestation 构成规范竞争 | 向量数据库公司向"编译层"转向的信号 |
| **Meta** | 工程博客：组织第二大脑（200+ 文件知识图 + OKF + 自动改进飞轮） | 企业内部实践背书 |
| **Cognition** | DeepWiki（为 Devin 编译代码库 wiki 的规模化架构） | 代码赛道 |
| **OceanBase** | ex-brain + seekdb（LLM 消化笔记为"当前状态"而非追加） | 数据库厂商入场 |

## 6. 社区项目的技术趋同点（gist 评论区 + 清单交叉分析）

不同独立实现正在收敛出相同的解法，这些是**事实上的社区共识**：

1. **确定性验证层**：引用核对不放给 LLM——Cortex（引用核对到 Git commit）、EXIA SEED（数字/日期/专名不在来源行即拒绝）、mindbase（磁盘引用验证）、OKF attested computations、secure-llm-wiki（7 阶段防注入管线）
2. **人审门控写入**：几乎所有成熟实现都有 review queue / diff 审批（mindbase 复选框审批、MemexOS 独立 worktree + 异家族模型复审、Mana 全量 Git diff、Curated Thoughts 审查队列）
3. **去重优先于新建**（Extend, don't create）：podcast-wiki 明确总结；MindBase near-duplicate 检测；crow-hq 发现 ingest 72% token 花在"决定"而非"写作"→小分类器接管
4. **矛盾与过时的显式建模**：SUPERSEDED 标记（Cortex/Link）、ADD/REVISE/DEPRECATE 操作（TrajWiki）、supersedes 谱系（Link）、bi-temporal 时间戳（多篇论文）
5. **混合检索兜底**：规模越过 ~100k token / 数百页后普遍加 BM25/向量/图检索（qmd 成为常用件；pgvector 侧car；Neo4j 轻量图）
6. **MCP 作为 agent 接口**：新项目默认带 MCP server，跨 Claude Code/Codex/Cursor 共享同一 vault

## 7. 初步格局判断（待深挖笔记校正）

- **赢家场景**（证据较强）：跨文档综合与多跳关系问题——LangChain 111 文档实证：wiki vs 检索 0.10→0.52（5x），每正确答案 $0.55→$0.19；+evidence graph 再 +27%、成本再 -58%；Pinecone KRAFTBench 独立验证（0.680 vs 0.413）。**简单查找无优势**（0.84 vs 0.83）——编译成本 $4.15 全量/$0.09 每篇增量，回本取决于复用频次
- **输家场景**（证据较强）：异常密集的决策支持（wiki 不敌 RAG 的预注册负面结果，待论文深挖确认）、开放式未见问题的细节检索（hyunsoo36 批评）、>1000 文件的规模化（Provenance-First 论文）
- **结构性空白**：
  1. 几乎全部实现以**开发者**为前提（终端 + Claude Code/Codex）；面向普通用户（非程序员）的成熟产品极少——而 Karpathy 模式的本意恰恰是服务"任何人"
  2. 中文生态供给薄弱：WeKnora（36.4k★）重企业、未采纳 OKF；second-brain-skill 支持 zh 但偏极客；**"中文 + 普通用户 + OKF 可携带 + git 可管"组合无人占据**
  3. ingest 成本问题（编译 vs 检索的经济性）已有论文级证据但无产品级解法
  4. "操作语义"无标准——各实现的 ingest/query/lint 互不兼容，OKF 只解决了文件格式
- **竞争烈度**：工具层红海（150+ 项目），但**产品层（普通人可用的完整体验）蓝海**；标准层已被 OKF 占位，跟随而非另造格式是合理策略

## 8. 与本项目的关系（初步）

- 我们的定位空间大概率在：**面向普通用户（尤其中文用户）的产品层** + **复用 OKF 等既有标准**而非自造格式
- 待三个深挖笔记返回后，需细化：ingest 经济性对策、验证层设计选型、与 WeKnora 等的差异化管理
