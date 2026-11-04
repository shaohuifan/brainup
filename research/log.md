# 调研操作日志（append-only）

## [2026-11-04] ingest | 生态主清单与 gist 评论区入库
- 抓取 gavischneider/awesome-llm-wiki 全文（~200 条目）→ raw/awesome-llm-wiki-readme-2026-11-04.md
- 摘录 Karpathy gist 原文要点 + 评论区 14 个社区实现与关键批评 → raw/karpathy-gist-and-comments-2026-11-04.md
- 交叉抓取 SingggggYee/awesome-llm-knowledge-bases（工具链清单）与 arXiv:2607.04576（Progressive Disclosure 预注册消融）摘要

## [2026-11-04] synthesis | 全景综述初版
- 写 wiki/landscape.md：时间线、规模、9 类生态位、标准化进程（OKF 收敛）、9 家大厂动作、6 项社区技术趋同、初步格局判断
- 关键判断：工具层红海（150+ 项目）、面向普通用户的产品层蓝海、格式标准跟随 OKF 而非自造

## [2026-11-04] ingest | 派出三个并行深挖子代理
- deep-dive-standards-vendors（OKF/OpenWiki/WeKnora 等）
- deep-dive-papers（14 篇论文）
- deep-dive-failure-modes（10 个一手运维报告）
- 产出落 raw/，完成后并入 synthesis

## [2026-11-04] ingest | 标准化与大厂深挖完成
- 抓取 12 个一手来源 → raw/deep-dive-standards-vendors.md：OKF v0.1/v0.2 规范全文与两篇发布公告、LangChain OpenWiki（repo + 4 篇博客：wiki-memory/evidence-graph/WikiBench/Brains）、腾讯 WeKnora v0.9.0、Microsoft llmwiki、Vercel openwiki、Pinecone Nexus、YANP v0.2
- 关键实证：111 文档语料 wiki vs 检索 0.10→0.52（5x），+evidence graph 再 +27%/引用一致性×2/成本-58%；编译 $4.15 全量、$0.09/篇增量；KRAFTBench Nexus 0.680 准确率 vs RAG 0.413（tokens 1/7）；WikiBench 确认 wiki+source>仅source>仅wiki
- 关键判断：OKF 是唯一有跨大厂采纳势头的标准（Google 制定、LangChain 双模式默认输出）；"编译>检索（跨源问题）+简单查找不值得编译"获 LangChain/Pinecone 双独立验证；中文+普通用户+OKF+git 组合无人占据

## [2026-11-04] ingest | 实证证据与失败模式深挖完成
- 抓取 10 个一手来源（3 篇 403 经 RSS/Wayback/r.jina.ai 绕行）→ raw/deep-dive-failure-modes.md：6 个月数百页三结构失败、10 周 lint 遥测（死链 109→146 从未下降、自动修复 0/185）、双 vault 结构化对照（~300 笔记阈值）、13 题 A/B（wiki 全输：12/13 vs 13/13、token×9.3、p50×2.5）、MindBase 产品化"说不"工程、490 页 880 commit 确定性闸门、Dexio 退役 index.md/log.md 写热点、760 页月报
- 关键机理：wiki 对自己的过去无免疫系统（changelog 漂移/静默矛盾/孤儿累积同形恶化）；lint 检测≠修复（154/185 死链是人的分诊决策）；维护成本本质是"决策债"按新名字进入速度复利
- 设计阶段必须内置的三个决定：写路径防护（P0）、lint 报告=决策队列而非计数仪表盘（P1）、渐进结构化路线 Pile→Database（P2）

## [2026-11-04] ingest | 学术论文深挖完成
- 13/14 篇一手抓取（1 篇被作者撤稿，二手信息标注未验证）→ raw/deep-dive-papers.md
- 关键结论：查询成本三杠杆（渐进披露 -33~50%、答案写回 -84.6%、路由 O(1)）可叠加；结构性衰减（~1000 文件自引用投毒、盲编译灾难失败率 53-60%）是核心风险，缓解手段跨论文收敛（单向流防火墙/声明级 ADD-REVISE-DEPRECATE/verify 抽样/Error Book）；评估方法学危机（裁判间一致性 rho=0.04）→ 对外只能用同域差分+人工抽检
- 学术空白确认：普通用户/小规模/本地优先/人机 curation 工作流零研究

## [2026-11-04] synthesis | 调研综合报告完成
- 写 wiki/synthesis.md：证据调和（wiki 胜负边界与成本真相）、定位空隙三重确认、设计约束 P0-P7（写路径信任/决策队列/渐进结构化/单向流分层/并发/查询规模/度量评估/安全）、风险清单、6 个设计讨论题、诚实声明（撤稿论文/hyunsoo36 批评仍无产品级完整反驳）
- 调研阶段结束，转入设计阶段（待用户拍板讨论题）

## [2026-11-04] design | 设计方向确认与提案起草
- 用户确认：场景=读书/学习型；形态=CLI + MCP 工具先行（引擎优先，GUI 后续包壳）
- 起草 design/design-proposal-v0.1.md（讨论稿）：定位、Vault 三层单向流、读书领域 schema（作品/章节/概念/人物/主题/分歧/复习七类页）、渐进结构化四阶段、CLI+MCP 操作面、写路径信任管道、MVP 范围与北极星指标、v0.1-v0.3 路线图
- 待定：技术栈（推荐 Python/uv）、模型默认（推荐 OpenAI-compat 统一+中文云 API）、许可证、命名

## [2026-11-04] design | 设计定稿
- 用户确认四项：技术栈=Python 3.12+/uv；模型=BYOK 全兼容（OpenAI-compat 统一 + Anthropic，小模型路由+大模型综合）；许可证=Apache-2.0；命名=双语
- design/design-proposal-v0.1.md 标记已确认，第七节改为决策记录；AGENTS.md 当前状态同步
- 剩余：具体命名 → git init + 脚手架 → 进入实现阶段
