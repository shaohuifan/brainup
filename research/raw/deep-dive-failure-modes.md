# 深挖：LLM Wiki 实战实证证据与失败模式

> 调研笔记 · 2026-11-04
> 主题：真实运行数月之后的经验教训、失败机理、可操作对策
> 服务对象：个人知识库开源项目设计阶段的避坑输入
> 来源可靠性总评：全部为一手实证（自述运行数据），但样本均为 n=1 的单人/单团队经验，且部分作者有商业利益（见各节"可靠性备注"）

---

## 阅读指南

本笔记按"规模化失败教训 → 多实现横评 → 运维经验 → 横断归纳"组织。每个来源提取三类信息：**具体数字**、**失败机理**、**可操作对策**。最后归纳三个核心问题：什么场景 wiki 输、什么场景 wiki 赢、维护成本的真实曲线。

**来源获取说明**：3 篇来源（Medium ×2、rdworldonline）直接访问被 403 拒绝，分别通过作者 RSS feed 全文、Wayback Machine 存档、r.jina.ai 阅读代理获取。另发现任务清单中来源 6（`/guides/llm-wiki-github/`）与来源 10（`/guides/llm-wiki/`）为同一页面的两个别名 URL，内容完全一致，本笔记合并处理。

---

## 一、规模化的失败与教训（最重要）

### 1.1 数百页、四领域、6 个月：三种结构性失败

**来源**：Karpathy's LLM Wiki Works. Here's What Broke When I Ran It at Real Scale — Michael Tuszynski, 2026-08-13
**URL**: https://www.mpt.solutions/karpathys-llm-wiki-works-heres-what-broke-when-i-ran-it-at-real-scale/

#### 实验设置（失败模式由此 grounded）

- Obsidian vault（NEXUS 工作区结构）：`000-inbox/`、`200-knowledge/`、`300-entities/`、`400-daily/`，外加 `200-knowledge/context/` 下**每个领域一个 context 文件**（finance / health / content / jobsearch）
- 顶层 `CLAUDE.md` 定通用规则，每个领域文件做特化
- 实体（人/公司/服务/资产）为单文件，**以 wikilink 文本命名**（`[[Janney]]` 直接 grep 到 `vault/300-entities/orgs/Janney.md`）
- 规模：**数百 wiki 页、4 个活跃领域、2 月起每日写入、运行 6 个月**；根目录 `MEMORY.md` 存硬教训 34 条
- 定位：远超 Karpathy 玩具规模、远低于 RAG 规模问题——**原 gist 从未讨论的中间地带**

#### 三种结构性失败（同一形状："wiki 对自己的过去没有免疫系统"）

1. **同文件内部漂移**：文件顶部"近期变更"区与下方"工作原理"参考区矛盾。4 月记录的东西 7 月被推翻时，Claude 只在 changelog 追加一条带日期的条目就觉得完成了，下方仍把死系统描述为现行。读者（人或 agent）信任参考区，而它是错的。**写日志条目的感觉像记录了变更，但真正被读的现在时散文永远不被重访。**
2. **页面间静默矛盾**：同一账户两张实体卡——一张叫 "Janney"，一张叫 "Janney Montgomery Scott LLC"——下游聚合因 dedup key 是名称而**重复计数**。RAG 失败是静默的（检索悄悄漏掉 chunk）；wiki 失败是另一种静默：**两页都存在、各自内部自洽、互相不知道对方**。Claude 不会主动发现。
3. **孤儿页与死链累积快于 lint**：Karpathy 原文建议"偶尔跑 lint"。**在 300 页规模，"偶尔"不是频率，是祈祷。**（注：作者在后续文章中撤回了"每周 lint 能恢复大部分"的说法，见 1.2）

#### 三个对策

- **A. 让 build 失败的漂移 linter**：Python 检查，遍历 vault，将 "retired"/"decommissioned" 术语与所有文件交叉引用，标记权威文档中对死系统的活引用。pre-commit + 定时 cron 运行。实际战果：Ghost 被 Astro 静态站替换后，linter 抓出 **9 个文件**仍把 Ghost 发布路径描述为现行——含顶层 README。没有它，读者会去拿死凭证。
- **B. 每领域子 schema，而非一个巨型 CLAUDE.md**：gist 把 schema 当一个文件，"活不过第二个领域"。finance 与 health 的词汇、约定、"一页是什么"几乎零重叠。顶层定通用规则（语气、安全、wikilink 格式、验证协议），各领域 `<domain>-context.md` 特化。类比 scoped CSS。
- **C. wiki 旁边加向量索引，而非替换**：过了 **~100k token wiki 内容 + 100k session 日志 + 数万条历史对话**后，Claude 无法再把 index 放进 context。作者方案：wiki 仍是权威的 authored/curated 层，另加 pgvector 索引覆盖全语料（vault + session 历史 + 历史归档）做 recall——**Postgres 17 上 126k chunks，mxbai-embed-large，Mac mini 运行**。"不是 wiki 的替代，是当你忘了两个月前把某页写在哪个 slug 下时找到它的工具。"

#### Wiki 仍然赢的地方

- **综合、实体消解、"我注意到的这三件事如何关联"**：问"上个月 finance 日报的贯穿主线是什么"，答案依赖每条日志进来时就写好的综合页——**工作在 ingest 时发生过一次**。RAG 结构上做不到（检索无积累）。
- **实体卡**：每个公司/人一个文件，以 wikilink 文本命名，成为唯一真相源。事实变了改一个文件。"无聊的模式，每天都在回本。"

#### 模式失效的诚实边界（四个硬边界）

1. **多写者并发**：两个 agent 并发写同一页没有锁。作者靠约定单写者。若 fan out 多个 coding agent 都编辑 `SESSION-STATE.md`，需要 lockfile——gist 对此无话可说。
2. **跨 session 记忆**：wiki 不是记忆，Claude 每 session 重读。"上周二我们决定了什么"需要独立存储（daily logs + 向量索引）。
3. **热内容超过 ~100k token**：载重假设是 index 放得进 context。放不下时要么按领域分片（作者方案）、加检索层、要么接受降级答案。
4. **无 Claude 在环的人类可读性**：markdown wiki 对人可读，但 **Claude 为 Claude 写了数月的 wiki 有足够的 house-style 速记**，没有 schema 的新读者会丢失上下文。"wiki 可读；积累的约定不可读。"

#### 行动建议（原文给出）

- 从一个文件夹、一个 schema、5 个来源、一个你在主动思考的领域开始，**先跑两周再调整**。
- 开始觉得有效时（**约 30-40 页**），在后悔之前装上三样：标记死术语的 drift check、每周真跑一次的 lint、"任何迁移必须更新参考区而不只是 changelog"的规则。
- 向量索引只在 wiki 真的放不下时才加。**"多数人该写 schema 的时候去够 RAG。"**

**可靠性备注**：作者为云/平台工程师，同一 vault 的后续跟踪见 1.2（该篇撤回了本篇"每周 lint 恢复大部分死链"的主张——两篇应作为同一纵向数据集阅读，且是罕见的公开自我纠错）。

---

### 1.2 334 页 10 周 lint 遥测：检测 ≠ 修复，修复 ≠ 脚本能做的

**来源**：The Lint Ran Every Week. The Dead-Link Count Never Went Down. — Michael Tuszynski, 2026-10-23
**URL**: https://www.mpt.solutions/lint-ran-every-week-dead-link-count-never-went-down/

#### 核心数字（每周日定时检查器遥测）

| 日期 | 扫描页数 | 死链(原始) | 孤儿页 | 真实坏链 |
|---|---|---|---|---|
| Aug 2 / Aug 9 | **0** | 0 | 0 | 0 |
| Aug 16 | 261 | 116 | 117 | 109 |
| Sep 27 | 303 | 155 | 118 | 141 |
| Oct 18 | 334 | 170 | 124 | **146** |

- Aug 16 → Oct 18：页数 **+28%**，真实坏链 **+34%**；每页坏链率稳定在 **~0.42 → ~0.44**——**坏链随页数线性增长，不是收敛**
- **10 次周跑，坏链数一次都没降过**；孤儿 117 → 124
- 前 2 周扫描 0 页是独立事故：检查器指向迁移中已退役的文件夹，扫描 0 页报告"干净的 wiki"。**8 月 13 日发布的"lint 有效"博文，恰好基于最后一次零页运行之后 4 天内的数据。**（监控监控者：报告干净 ≠ 干净）

#### 修复脚本实测：185 条死链，0 条能自动修

```
vault-repair: 185 dead wikilinks — 0 confident fixes, 4 fuzzy suggestions, 181 unresolved
```

- 脚本策略：先大小写不敏感、再模糊匹配，只改写安全情况（大小写/空格差异）。**2.7 秒跑完，0 条安全修复，4 条建议全是同一类错误（食谱按文件夹路径而非笔记名链接），181 条无任何候选。**
- 不同工具不同日期计数不同（周日检查器 170 vs 修复脚本 185，作者未 diff）——**工具间的计数口径本身就是个坑**

#### 185 条死链的构成（最有信息量的部分）

| 死链指向 | 数量 |
|---|---|
| 有名字无笔记（人/公司/服务，41 条在已归档日报中） | **154** |
| 草稿管道留在旧博文草稿里的 CONFIRM 占位符 | 17 |
| 保存的第三方 README 里的示例语法 | 7 |
| 文件夹路径链接（4 条指向存在的食谱、3 条指向不存在的索引页） | 7 |

- **大头（154 条）恰恰是 agent 被要求写出来的**：操作文件要求 agent 给每个首次出现的人/公司/服务加 wikilink，好让后续同实体页面连回来。**这条规则有效，同时也是死链生成器**——每个新名字落笔即加括号，没有任何东西去创建背后的卡片。Schwab 被链 6 次、Plaid 3 次，多数是日报里出现一两次的名字。
- Karpathy 原始 gist 点名了这个发现（lint 找"被提到但没有自己页面的重要概念"）——**发现从来不是难处，每一条都是只有 wiki 主人能回答的决策**：这名字配一张卡吗，还是去掉括号？通话记录里提一次的名字大概不配；管你钱的机构配。
- 底部三行是噪声但同样有信息量：正则匹配一切双括号对 → **185 条中 24 条从来不是链接**（含 CONFIRM 占位符、README 示例）。"死链计数是括号对计数，不是坏知识计数。" Aug 16 时此类噪声 7 条，Oct 18 涨到 24（草稿管道开始留 CONFIRM 标记）——原始列涨得比真实列快的原因。

#### 为什么"自动建 stub"是伪解

- 死链数一夜归零的代价：**有标题无内容的 stub 就是一切意义上的孤儿**（除了名字）。没有任何有用的东西链入，也没有任何值得读的内容。已有 124 个孤儿，stub 会再加 **154 个**，检查器更好看，wiki 没更有用。
- 且违背实体卡的本意：卡有价值因为它是一个事实的唯一居所；stub 承诺居所存在然后什么都不放，**下一个读它的 session 学到名字和空**。

#### 适用边界（作者自述猜测）

- 单领域小 wiki 大概率不会撞上：名字少到可以随到随建卡。
- **有专职策展人的团队不会撞上：那个人就是缺失的科目。**
- 作者的系统在**跨多领域 + 日报提及人名快于任何人策展**时崩溃。

#### 核心论点（对预算设计的直接指导）

> "缺失的科目不是 lint。lint 很便宜。是修复，而修复大多是脚本做不了的决策。"
> "预算的是决策，不是 lint：数每周有多少新名字进入 wiki，谁决定每个是否成卡。"
> "我今天是 154 个未决决策，由 10 次没人行动的周报累积而成。脚本修了 0 条、建议了 4 条。其余需要 owner，而周报只有在有人周一读它时才有用。"

**可靠性备注**：与 1.1 同作者同 vault，构成完整的"宣称有效 → 遥测打脸"纵向记录。数据为作者自报，无第三方核验，但表格粒度与自我打脸细节（零页扫描事故）反而增加可信度。

---

### 1.3 严格结构化 vs 最小结构化：胜者靠运气赢了，而那才是真正的教训

**来源**：I Built Two AI Second Brains From the Same Documents. One Gave Better Answers. Here's Why — Deepak Singh, 2026-06-13
**URL**: https://medium.com/@dksingh0429/built-two-ai-second-brains-with-the-same-documents-one-gave-better-answers-heres-why-6e96483935a8
（注：Medium 直接访问 403，本文通过作者 RSS feed 全文获取）

#### 实验设计

- 同一批文档（PowerPoint、半成品 Word、会议记录、Teams 原始导出），建两个哲学相反的 vault：
  - **Vault A "The Database"**：重度结构化。SCHEMA.md 定义严格笔记类型（client/pursuit/project/research/concept/tool/person/decision 八类）、每笔记刚性 YAML frontmatter、严格命名 `ps-client-topic.md`、标签分类法、硬隔离规则（常青知识在 `concepts/`、客户特定发现在 `research/`，两者永不合并）
  - **Vault B "The Pile"**：轻度结构化。纯 markdown、几个基础标题（Overview/Status/Notes）、松散命名、零仪式
- 均为 Obsidian + 标准 wiki-links + 根部 CLAUDE.md（Claude Code 读 house rules）

#### 结果与反转

- 同一真实问题："Tool X 和 Accelerator Y 对下周客户 workshop 有影响吗？"
- **两个 vault 给出相反答案**：
  - Vault A："Tool X 是云迁移工具，你的客户没在迁移，别硬塞——不用。"推理干净、完全可辩护、**完全错误**。
  - Vault B："Tool X 的分析引擎能从客户遗留 BI 报告中抽取元数据/KPI/公式/血缘喂你的知识图谱，围绕它建 workshop PoC。"推理同样干净、**完全正确**。
- **根因不是结构，是数据**：Vault B 多一个文件——两天前丢进去的一条 Teams 原始碎片，同事随口提到在这个客户上用过 Tool X 的元数据引擎。**一句乱糟糟的句子翻转了整个建议。** A 从不完整信息无瑕疵推理，B 从完整信息无瑕疵推理。**完整性打败了结构。**
- 作者诚实承认实验被污染（两个 vault 在内容上不等价），但认为这个事故本身就是要点：

> "你可以花数周完善 schema，仍然因为缺一条笔记得到一个自信的错误答案。**格式从来不是瓶颈，数据才是。**"

#### 对 AI 而言什么重要/什么不重要（结构化投入的方向修正）

- **几乎不重要**：视觉格式（callout、主题、嵌套 markdown——"那是给你的眼睛的，不是给模型的 context window"）；frontmatter vs 散文（LLM 读句子里的事实和 key:value 一样好）
- **真正重要**：
  1. **唯一真相源**：冗余杀死 AI 推理。两个 vault 或重复文件更新不均，会给你自信的矛盾答案。（"问我怎么知道的。"）
  2. **可预测命名**：小写、连字符、类型前缀（`client-acme.md`）+ 激进的 `[[wiki-links]]` → AI 找到一个正确入口即可遍历全图
  3. **保质期隔离**：Vault A 的救场之处。常青（"知识图谱如何工作"）与易变（"客户 Z 截至 6 月的技术栈"）分开，阻止 AI 给出自信的过期答案
  4. **出处标记**：每笔记盖源戳（"generated from Deck_V2.pptx on June 12"），AI 可自行按最新输入解决冲突

#### 渐进结构化阈值（对我们项目的直接输入）

> "Start unstructured, scale with intent. Start like Vault B. Grow into Vault A. Never run both at once."

- **~50 笔记以下**：别让 schema 设计阻止捕获。"存在的一条乱糟糟的事实胜过一条你永远不会写的完美笔记。"
- **~300 笔记以上**：约定开始大幅回本（更低 token 成本、新鲜度信号、冲突消解）
- **添加顺序**：先收紧命名 → 再隔离常青知识 → 最后强制出处
- Level 2（100+ 笔记）铁律："**写/改任何文件前，先读并对照 SCHEMA.md 校验**"

#### 附带 build guide 要点

- `inbox/`（原始堆放区：decks/PDF/聊天导出）+ `wiki/`（已加工已验证知识），CLAUDE.md 规则：处理后**永不删除** inbox 内容（移 `_archive/`）；强制链接完整性；新数据与现有笔记矛盾时**在文件内打标，永不静默覆盖历史事实**

**可靠性备注**：作者自我暴露实验污染，诚实度高；结论"数据 > 结构"与 1.1 的"实体卡 + 完整捕获"、1.2 的"死链来自规则而非失误"相互印证。n=1 单问题对比，戏剧性大于统计力，用作方向性洞见而非量化依据。

---

### 1.4 Hybrid RAG vs LLM-Wiki：13 题 A/B 评测（唯一量化对照实验）

**来源**：Hybrid RAG vs LLM-Wiki：把 Karpathy 的概念拉去做 13 題 A/B 評測 — Kevin Wu, 2026-05-06
**URL**: https://osisdie.github.io/blog/2026/hybrid-vs-llm-wiki-eval/

#### 实验设置

- 内部 60 篇 markdown wiki（一次 bulk-build 花 **~194k tokens**；30 篇实体页 + 9 篇时序页 + 6 篇 FAQ + 7 篇政策页 + 其余彙总页）；底层检索 1,402 个 vector points
- 13 题（从原始 43 题抽出的单租户子集）：FAQ 四个子分类 + 3 paraphrase + 1 out-of-scope + 1 edge case；人工逐题判读
- **隐藏成本样本**：RAGAS judge 模型的 quota 被 wiki bulk-build 吃掉，4 个指标全 None——**wiki 维护成本吃掉了评测预算本身**

#### Headline 数字

| 指标 | Hybrid | LLM-Wiki | Δ |
|---|---|---|---|
| Accuracy（13 题） | **13/13 (100%)** | 12/13 (92.3%) | +1 |
| Has-answer rate | 0.923 | 0.923 | 平 |
| Avg confidence | 0.808 | **0.862** | wiki +0.054 |
| Latency p50 | 3.3 s | 8.2 s | **×2.5** |
| Latency p95 | 24.3 s | 27.3 s | +12% |
| Avg tokens/query | 1,407 | 13,055 | **×9.3** |
| LLM calls/query | 2 | 4 | +2 |
| 一次性维护成本 | 0 | ~194k tokens | bulk-build |

两个值得停下的数字：
1. **Confidence 0.808 → 0.862**：wiki 报告自己更有把握但 accuracy 更低。**confidence 是模型自评，不是命中率**。wiki 在唯一错题上 confidence 给到 0.9——高 confidence 配错答案比低 confidence 配错答案危险得多。
2. **Tokens ×9.3**：不是"多花一点"。query 平均 13k tokens，换更贵模型则线性放大。

#### 三种 wiki 失败模式（生产视角的机理拆解）

**1. 跨租户污染（cross-tenant contamination）——不能设为 default 的硬阻塞**
- 案例：问"本租户政策可转让吗"，wiki 答"当然可以"并列出**另一租户**的配额（X/Y/Z 份），confidence 0.9；GT 是本租户不可转让
- 三层根因：① bulk-build 的页面合并 key 是**实体名称**而非 tenant+entity → 多租户同类政策被合进同一页；② `INDEX_PICK` 无租户后过滤；③ persona prompt 只管口吻没写"只引用本租户事实"的红线
- 最低成本修法：`tenant_id` 进页面 frontmatter 必填字段，`INDEX_PICK`/`ANSWER` 两阶段都按租户过滤。代价是每个租户各自 bulk-build，"wiki 跨租户知识整合"的初衷打折

**2. 页面合成噪声"焊"进 wiki**
- 案例：问"有哪些取得方式"，答案某行夹 `الالكتروني the electronic ticket`——阿拉伯文+英文混进中文答案
- 不是检索失败：**bulk-build 阶段小模型在某次 page synthesis 引入多语种污染，写进了页面 markdown，之后每次 query 原样照抄**
- 特性：噪声"焊"在 wiki 上每次重现；比 Hybrid 偶发 hallucination 更难检测——**因为它是确定性的**；confidence 可能很高（wiki 自身无矛盾）
- 修法：bulk-build 加 lint pass（检测预期语种外字符/重复条目/空页）。"Karpathy 的 ops 流程里 lint 是 first-class step，但目前实现里还没做 nightly lint"

**3. Paraphrase 过度简化**
- 案例：短问法（"X 怎么做"）wiki 倾向单句答案，丢掉 Hybrid 会列的 A/B/C 三个限制条件
- 根因：`WIKI_ANSWER` prompt 模板鼓励简洁；遇到 paraphrase（GT 也短）时镜像了 GT 的简洁度
- **更隐性的失败**：binary accuracy 捕捉不到，要看 fact-point recall
- 修法：ANSWER prompt 显式加"列出所有相关限制"；或 intent classifier 多发一个 `mode_preference` 字段，paraphrase intent 直接路由到 hybrid

#### Token 经济学（维护成本摊提）

- Query-time：13 题 Hybrid 共 18,294 tokens vs wiki 169,715 tokens
- Wiki query 成本结构：`INDEX_PICK` 喂完整 index.md（~2-3k tokens）+ `ANSWER` 塞 1-4 篇正文（每篇 800-2,000 tokens）= 每题稳定 10k-15k
- Bulk-build 摊提：每天 regen +194k/day；每周 ~28k/day；**增量 ingest 每篇 3-5k tokens**（对应 Karpathy 的"一篇 source 触碰 10-15 页"）
- **本次 13 题中没有任何分类 wiki 的 accuracy 高过 Hybrid**——"要把 query-time 多花的 token 赚回来，wiki 需要在某类 query 上 dominate Hybrid；没有发生"

#### 路由建议（原文表格）

| 场景 | 推荐 | 理由 |
|---|---|---|
| 短/直接 FAQ | Hybrid | 快、便宜、检索已足够 |
| 需列条件的 paraphrase | Hybrid | wiki 常给过简答案 |
| 多文档综合（"最近有什么变动"） | 理论上 wiki 强 | **本次 13 题没覆盖，需新 GT 验证** |
| 跨租户比较 | **Hybrid only** | wiki 的 page grouping 会跨租户混 |
| Out-of-scope 拒答 | 任一（wiki 略快） | wiki 早退 1.6s vs 2.3s，唯一 latency 优势 |
| 高 confidence + 事实敏感 | Hybrid + 人工审 | wiki 有 high-conf-on-wrong 风险 |

- 结论：**default 维持 Hybrid，wiki 留作 per-request `rag_mode=wiki` 覆写**
- 换 wiki 之前先把 Hybrid 调好：cross-encoder reranker（Recall@5 ~0.7→~0.82）、contextual retrieval（Anthropic 2024，chunk 前置 doc summary）、intent-aware routing、租户维度 metadata filter、RRF k 调参

**可靠性备注**：13 题为小样本；场景是多租户客服 bot 而非个人知识库（跨租户失败模式对个人 KB 场景弱相关，但对"多项目/多身份"个人 vault 的隔离设计有迁移价值）；无多文档综合题的 GT——恰是 wiki 理论强项未被测到。数字自报但完整公开了失败案例细节。

---

### 1.5 MindBase：把模式做成产品，难点是阻止 LLM 写

**来源**：I built Karpathy's LLM Wiki as a product — the hard part was stopping the LLM from writing — frank chu, 2026-10-26
**URL**: https://dev.to/frankchu/i-built-karpathys-llm-wiki-as-a-product-the-hard-part-was-stopping-the-llm-from-writing-819

#### 定位与核心论点

- MindBase：开源（MIT，135 星）、纯 markdown 落地在用户自己磁盘、默认免费本地模型；三种运行形态（web UI `npx mindbase-app` / Claude Code 插件含 5 个 sub-agent / 50 工具 MCP server）
- 目录：`sources/contributors/<you>/`（**append-only，AI 永不改写**）、`sources/research/`（AI 写、逐条人工批准）、`context.md`（合成 wiki，LLM 写、人批准）、`index.yaml`（自动目录）、`logs/`（append-only）、`state/`+`artifacts/`（派生态：快照、lint 发现、可重建）
- 三操作闭环：ingest（AI 读源→与人讨论 takeaways→提计划→仅批准项写入）、build（重建 context.md）、lint（AI 审计自己的矛盾/过期/孤儿）
- **核心论点**："一个 LLM 往里写的 wiki，只有在你信任它写的东西时才值得拥有。所以大部分工程花在了阻止 LLM 写上。" "复利对垃圾同样成立。MindBase 最重要的代码不是写 wiki 的代码，**是说不的代码**。"

#### 四个信任机制（对我们写路径设计的直接参考）

**规则 1：模型只提议 JSON，永不直接向磁盘写散文**
- 单引擎流程：`gather → 一次受约束的 LLM completion → (checkpoint) → zod 校验 → executor 应用 → 追加 logs/<date>.md`
- 模型全部输出 = 单个 JSON plan，Zod schema 校验。**动作词表全集只有 4 个动词**：`create_research_page` / `update_context` / `append_context_section` / `add_wikilinks`，每个带长度上限（markdown ≤100k 字符、section ≤20k、links 1-10、每 plan ≤20 个 action）
- schema 里**故意不包含任何能写 `sources/contributors` 或 `sources/raw` 的动作——append-only 层从 schema 上不可达**
- 金句：**"一个说'请别改用户源文件'的 prompt 是建议。一个缺失的 enum 变体是墙。"** 模型可以幻觉出第五种 action kind，schema parse 失败、什么都不会执行、op 报错。executor 应用时还会对每个 path 再查一遍项目根（belt and braces）

**规则 2：没有人工勾选，任何东西不 apply**
- completion 产出 takeaways + plan，UI 把 plan 渲染成**复选框**，apply 步骤只取你实际勾选的索引——未勾选的 action 永不运行
- plan 存内存、**10 分钟过期**（过期的批准卡不能明天才触发）；pending plan 预留它想创建的 slug（两个并发 contribute 不会在写时碰撞）

**规则 3：builder agent 没有手**
- 重建 context.md 的 builder sub-agent 工具白名单**只有 Read + MCP 工具，无 Edit/Write/Bash**——写系统最重要文件的 agent 没有文件写工具
- 唯一落盘路径 `mindbase_atomic_write_context` 的四重防：① 快照当前版到 `state/builder/snapshots/<ts>.md`（每次 build 可回滚）② 写临时文件再 `rename()`（原子，无撕裂写）③ **context.md 400 行上限**（溢出不是静默截断也不膨胀，溢出到 `context-overflow-<stamp>.md` 并留指针）④ 追加日志
- 其他 agent 同模式：lint curator 只读；researcher 可读全网但只能通过 append-only 的 `research_save` 持久化
- 金句：**"藏在源文件里的 prompt injection 可以让模型想写任何地方。白名单决定它能写哪里。"**

**规则 4：lint 发现必须带引用，引用要被核验**
- lint 声称两页矛盾时，finding 必须含每页一段 **8-300 字符的逐字引用**；runner 重读磁盘上的页面、核验引用真的在里面（大小写/空白/markdown 归一化后）
- 模型编造的句子 → `verified: false`，而不是作为事实进收件箱
- 金句：**"能编造自己证据的审计者比没有审计者更糟，所以审计者不被允许这么做。"**

#### 为什么单次 completion 而非 agent loop

- 默认本地免费 → 默认大脑可能是 8GB 笔记本上的 3B 模型；**3B 不能被信任跑 12 步工具循环，但能填一份 JSON**
- 单发、temperature 0.2、schema 校验、JSON 解析失败则恰好重试一次（附上 parse error："Respond again with ONLY the corrected JSON"）
- "故意无聊。wiki 是长生命周期工件；每一次写入都应尽可能接近确定性。"
- 模型分层：8GB→llama3.2:3b；24GB+→qwen3:14b（~30s/completion）；32GB+ Apple Silicon→30B（后台 lint/build，矛盾发现能引用确切冲突句）

#### 工程细节的可信度信号

- README 写 49 个 MCP 工具，作者自己数了 `register` 调用实为 **50**——"某天第五十个工具溜了进来而 README 没收到通知"（自曝式诚实）
- 测试 57/58 通过，唯一红测（Brave search API 沙箱里挂起而非快速报错）**原样展示不裁剪**
- 状态：0.4.6 早期访问，beta 到 2026-Q4；路线图：浏览器捕获、Whisper 音频、团队项目+人工审查

**可靠性备注**：作者为产品作者（showdev 性质），有宣传动机，但四机制附真实代码路径与自曝缺陷，工程可信度高。四机制是本批来源中对"写路径防护"最完整的工程化答案。

---

## 二、多实现横评

### 2.1 Dexio 指南：12 个开源实现 + 46 个公开 wiki 实证研究 + 自家 4-agent 运维

**来源**：Karpathy's LLM wiki: what it is and how we run one with four agents — Dexio（更新于 2026-10-23）
**URL**: https://dexio.wiki/guides/llm-wiki-github/ （= https://dexio.wiki/guides/llm-wiki/，两 URL 同页）

#### 12 个开源实现（GitHub API 数据，2026-10-01）

| 仓库 | 形态 | Stars | License |
|---|---|---|---|
| nashsu/llm_wiki | 桌面应用 | 20,132 | GPL-3.0 |
| AgriciDaniel/claude-obsidian | Claude Code skills + Obsidian | 15,325 | MIT |
| inkeep/open-knowledge | markdown 编辑器应用 | 4,360 | GPL-3.0 |
| SamurAIGPT/llm-wiki-agent | agent skill | 3,593 | MIT |
| Astro-Han/karpathy-llm-wiki | Agent Skills skill | 2,395 | MIT |
| atomicstrata/llm-wiki-compiler | CLI 编译器 | 2,156 | MIT |
| lucasastorian/llmwiki | Web 应用 + MCP（Chrome 剪藏） | 1,658 | Apache-2.0 |
| nvk/llm-wiki | Claude Code/Codex/OpenCode 插件 | 1,362 | MIT |
| kytmanov/obsidian-llm-wiki-local | Ollama 本地管道 | 828 | MIT |
| GD4AI/obsidian-llm-wiki | Obsidian 插件 | 677 | Apache-2.0 |
| praneybehl/llm-wiki-plugin | 插件+skill | 116 | MIT |
| microsoft/llmwiki | VS Code 扩展 | 67 | MIT |

- **12 个中 10 个 9 月及以后仍有 push**——生态极新，细节依赖 README 复核
- 入门建议："gist + 一个 skill 是最便宜的起点；因为一切都是纯 markdown，以后可迁移到任何实现"

#### 46 个公开 LLM wiki 实证研究（2026-09）

- 纳入标准：仓库含 ≥20 个 markdown 页 + ≥30 条 `[[wikilinks]]`；合计 **7,195 页，中位数 76 页/仓**
- **46 个中 13 个是模板或位于示例目录**——"**最近的、条目多的 `log.md` 是真实使用的更好信号，胜过高 star 数**"
- 46 个中 28 个 wiki 放在仓库根目录、与项目自身 README/docs 混在一起；建议用 `wiki/` 文件夹隔开

#### 自家 4-agent wiki 运维（最重要的一手数据）

- 2026-09-06 起，4 个 Hermes agent 写同一个 wiki（建 Dexio 的、做营销的、运营第二家公司的、记个人财务的）；09-25 起托管化，agent 走 MCP 无本地副本
- 10-23 状态：**115 页、13 个文件夹、606 条链接、约 206,700 词**
- **关键架构决定：09-27 退役了 index.md 和 log.md**（Karpathy 模式的两个核心文件！）
  - index 行迁入每页 frontmatter 的 `description:` 字段，列页工具直接返回它——"**列表即目录，不可能与页面脱节**"
  - log 变为每次变更自带的 note：页面历史记录谁/何时/为何改，全 wiki 历史即 recent-changes feed
  - 退役理由：这两个文件是**每次 ingest 都会重写的文件，因此是两个 agent 同时写时必然相撞的地方**；它们只对"无搜索/无列表/无历史的纯文件工具"有意义
- schema 本身也是 wiki 里的一页（约 1,070 词）。agent 做实质工作前的仪式：读 schema → 列页 → 读 recent changes → **创建任何新东西前先搜索**
- query 答案确实归档：115 页中 24 页在 `queries/` 文件夹
- log 落在主题页而非全局文件：营销 agent 的搜索内容页已长到 ~9,600 词
- lint 是单次调用（孤儿/可能过期/被提名但未链接）；10-23 结果：**1 个孤儿、0 过期**。"我们不把孤儿当问题，因为 agent 靠搜索找页"
- **枢纽页持续膨胀**：Dexio 自身页 93 条链接、约 47,400 词；schema 说 ~200 行应拆分，该页还没拆

#### 本地 wiki 的三个崩溃点（多写者场景）

1. **两个写者编辑同一文件**：每次 ingest 重写 index.md、log.md + 最多 10-15 页 → 同步文件夹会丢保存或留冲突副本；git 给你散文的合并冲突
2. **lint 间隔中页面变陈旧**：页面保留被新源替代的声明，每个读到它的 agent 重复旧声明
3. **没人知道哪个 agent 写了什么**：无 git 的文件夹不保存历史；有 git，commit 带的作者名是 agent 被给的名字——通常就是你的

#### 共享方案对比

- git repo：agent 工作前 pull、工作后 commit、用自己的作者名；得到历史和 diff，代价是共享文件冲突 + **浏览器聊天 agent 无法跑 git**
- 同步文件夹：单人双机容易；同样的覆盖问题 + 零归属记录
- 托管 wiki over MCP：单一副本、无同步无合并；**写操作可携带 `base_version`（乐观并发控制，一个 agent 永不覆盖另一个的编辑）**；页面历史 `page_history` 记 agent 名；**可只读/编辑一节而非整页（省 token）**

**可靠性备注**：Dexio 卖托管 wiki（AGPL-3.0 开源 + 商业托管），"本地会崩→托管"的叙事有商业利益；但并发冲突的力学分析（index/log 是写热点、base_version 方案）技术上成立，且"退役 index/log"的实测决定本身就是高价值数据点——说明 Karpathy 的两个核心文件在多写者场景是负债。

---

### 2.2 五实现一周横评（单用户体验报告）

**来源**：I Tested 5 'LLM Wiki' Implementations So You Don't Have To — Mike Written | AI Trends 24（约 2026-07-09）
**URL**: https://medium.com/@aitrends24/i-tested-5-llm-wiki-implementations-so-you-don-t-have-to-d68ba7cc9100
（注：Medium 直接访问 403，经 Wayback Machine 2026-07-12 快照获取）

#### 测试方法

- 同一 10 源（4 文章 + 3 YouTube 转录 + 2 X threads + 1 PDF）喂 5 个实现，5 个递增难度问题，最后一题**只能靠连接两个不相关源回答**；评分维度：setup 时间、ingest 质量、检索准确性、"第 7 天还管不管用"（没人谈的指标）
- 背景：gist 发布一周内 GitHub 出现 50+ 新仓库

#### 五个实现的判词

1. **engram**（jeromeetienne/engram，TS CLI + Claude Code agent）——"工程师之选" 9/10（开发者）/4/10（其他）
   - 架构硬线：**CLI 从不调用 LLM；agent 从不猜 CLI 能算出的事实**。每页校验 frontmatter、坏链自动标记、**永不删除只弃用**
   - 实测：10 次 ingest 后 **0 孤儿、0 坏链**；lint 命令真的有用
   - 坏处：假设你会 npm 和终端，非开发者朋友几分钟就弹开
2. **Tome**（Claude Code 插件 + Quartz 渲染）——"最好看的输出" 7.5/10
   - 洞见：**"一个你从不看的知识库就是一个你会抛弃的知识库。"** 渲染成带反链和 graph view 的可浏览网站，让作者"为了好玩而浏览自己的笔记"——"这是工具和习惯的区别"
   - 坏处：ingest 纪律不如 engram，**10 篇摘要中 2 篇漏掉较长转录的要点**
3. **obsidian-llm-wiki**（liyading1818，Obsidian + Cursor agent skills）——"Obsidian 原生" 8/10
   - 最低摩擦入口；`video2wiki` 是五个工具中最好的单项功能：40 分钟讲座 → 1 摘要页 + 4 概念页 + 正确链入既有笔记
   - 坏处：绑定 Cursor，用 Claude Code/Codex 要手工改 skill
4. **pm-llm-wiki**（AliMahmoud15486，PM 专用 schema）——"专家" 8.5/10（对 PM）
   - 最大惊喜与全周最重要洞见：**"通用模式只是起点，schema 才是价值所在。"** 因为它知道"决策"和"干系人"是什么，工作相关查询的答案最直接有用
   - 坏处：不做 PM 型工作就没用——除非把它当自己领域 schema 的模板
5. **jarvis-vault**（erikschlegel，"自组织 AI 第二大脑"）——"过度承诺者" 5/10，**第 5 天 20 分钟内删除**
   - "demo 惊艳，现实不然。'自组织'的意思是'按开发者的思维组织自己，不是按你的思维'。" 第 4 天：没选过也改不动的文件夹分类法；一条 X thread 被归档到三个不同地方
   - 金句：**"全自动是错误的承诺。Karpathy 的模式恰恰因为 schema 把 agent 拴在皮带上才有效。解开皮带，你得到的是自信的混乱。"**

#### 三条横切教训

1. **"schema 文件是产品的 80%。"** 强制纪律的工具（engram、pm-llm-wiki）产出可信任的 wiki；"帮你搞定一切"的产出需要你复查的 wiki——**这 defeats the entire purpose**
2. **ingest 质量胜过检索聪明。** 简单题人人会答；只有严格"一源一摘要"规则的实现答对了那道跨源难题
3. **"你不会看它，你就会抛弃它。"** 渲染站点和 graph view 让人回流；纯 CLI wiki 靠意志力

#### 诚实部分（对成本预期的校准）

- 5 个实现全都不到两周新，真实摩擦存在；**重度 ingest 日 API 花费 $2-4**
- "每个实现仍然要求你本人出现并喂它源。**一个空的 LLM wiki 只是一个精致的文件夹结构。**"
- "如果你已有一套能用的笔记系统而且你真的会复查它，你还不需要这些。**工具修不了习惯。**"

**可靠性备注**：文章末尾推销作者的付费 prompt 手册，评分为主观单用户一周印象；但"schema 是 80%""ingest>检索""可看性决定留存"三条与 1.1/1.3/2.1 相互独立地收敛，可信。

---

## 三、运维经验

### 3.1 490 页 / 880 commit：3 个月运维报告（最完整的运维方法论）

**来源**：The LLM Wiki at 490 Pages: What 3 Months of Agent-Maintained Knowledge Actually Takes — webvise（Sebastian Kehle），2026-07-28
**URL**: https://www.webvise.io/blog/llm-wiki-3-month-report

#### 核心论点与规模数字

- **"agent 维护的知识库在你不再是它的图书管理员时才能存活。"** 手搓 second brain 死法一致：价值在维护，维护在第 3 周停止（Notion 坟场）。agent 不会无聊，"会在某个周二晚上开心地修 40 条坏链"
- 规模：**490 页、5 月以来 880 commit**；**运行成本：每天 5 分钟 + 周日一次 30-45 分钟的 agent session**
- 作者几乎没手写过任何一页

#### 分治所有权（可维护性的第一决定）

- raw 层（**341 篇存档文章、20 篇转录**、笔记、日志——agent 读永不改写）/ wiki 层（agent 拥有；**纠正在对话里发生而非手工**）；知识单向流动
- "当人类笔记和 agent 笔记共享文件，每次 agent 编辑都可能覆盖你本想保留的东西 → 你最终复查一切 → 图书管理员工作回来了。分层后复查缩为一个问题：**编译的理解是否忠于源？**"

#### 规则生长史（"每条规则对应一次失败"）

- AGENTS.md 246 行（宪法：目录树、页面模板、源规则、索引系统）；CLAUDE.md 一行（shim，让 Claude Code 读同一份文件）
- 四条核心规则：**无发明**（每个声明可溯源或标记 unverified）；**聊天不是源**（清洗摘录先存文件再引用文件——"'用户在聊天里说的'是一个你永远无法重新打开的引用"）；**每个易变事实一个 owner 页**（其他页链接不复制）；**已知实体的每次提及都是链接**（未链接的事实对图和检索不可见）
- 失败驱动的规则生长实例：某天早上指令文件被同步工具清零成 **0 字节** → vault 从文件同步迁入 git repo + commit gate；无法溯源的聊天引用反复出现 → 聊天被禁为源；CRM 式记录污染知识页 → 记录整体迁出 vault
- 金句：**"在缺失 costing 你东西的那一周写下规则，跳过 50 条投机规则。"**

#### 六操作封闭集（对抗 agent 即兴发明工作流）

| 操作 | 触发 | 做什么 |
|---|---|---|
| Ingest | raw 层落新文件 | 编译源为 wiki 页，对既有页去重 |
| Update | "file this" | 把陈述的事实应用到唯一 owner 页 |
| Query | "wiki 里 X 是什么" | 索引优先查找，带引用回答 |
| Lint | 每周或按需 | 两层完整性检查（机械+语义） |
| Enrich | "complete this page" | 从源/repo/网络研究填空 |
| Reorganize | "split this" / "merge these" | 结构性移动，带完整映射计划+确认 |

- 护栏示例：**ingest 把存档文章内嵌的指令当不可信内容**（"阅读清单是攻击面：一篇说'忽略你之前的指令'的文章被存为一篇这么说的文章；文章说的任何话都不能在同一 pass 内授权 schema 变更"）；**query 硬底线**：只有全文搜索为空后才能声称 vault 缺信息（否则"索引没显示"会变成"它不存在"）；reorganize 要求完整新旧映射 + 显式确认

#### 确定性闸门（本批来源中最强的工程主张）

- **1,671 行 Python linter、仅标准库、20 项检查、全量跑约 2 秒**；结构问题 = error（坏 wikilink、畸形 frontmatter、索引条目指向不存在文件）；漂移问题 = warning（孤儿页、索引计数失配、90 天未触碰的页）
- **13 行 pre-commit hook 以 strict 模式跑 linter（warning 也阻断 commit）**——低于门槛的任何东西进不了 git 历史
- 金句：**"agent 尊重一个 failing 的 gate，漂移过一条书面 guideline。你可以把'保持索引同步'写进规则书看它一周内腐烂；也可以让失同步的索引 fail 掉一个 blocking check，问题永久消失。"**
- 闸门读一切内容包括关于闸门的写作：写本报告时，一个用作例子的德语截止短语被 linter 解析为已过期截止；一个示例引用戳被登记为源清单缺源——**两段话都被迫改写后 commit 才通过**（linter 误报的真实样本）
- 三方分工表：链接/计数/命名/日期/存在性 → 脚本；矛盾/过期判断/合并决策 → 模型；品味/优先级/杀什么 → 我
- 金句："三个月的调优收敛到一个方向：**每当一个判断能变成一个 check，它就变成了 check。成本降、可靠性升。模型是系统里最贵最不可重复的组件，所以它只被花在判断上。**"

#### 页数曲线（健康的知识库有时会缩小）

> 188（4 月中）→ 279（5 月初）→ **263（合并收缩）** → 479（7 月初）→ **430（合并收缩）** → 490（7 月底）

- **"两次收缩是日志里最健康的两周"**（把薄页/重复页折进 owner）
- 金句："**无人维护的知识库只会增长。如果你的页数从来没降过，没人在打理花园。**"

#### 审计与评分方法（可复制的评估设计）

- 6-22 全库审计：一张定价表**在 4 个不同页面重述**、一个项目的故事**以段落长度讲了 3 遍**——"每一份副本写下时都是对的，每一份副本都是未来的谎言，因为下一次变更 会命中其中一份而漏掉其余。" 修复是**所有权而非合并**：registry 为每个易变事实指定唯一 owner 页；小单主题页保持小，"**因为那个形状检索最好**"。同一审计：400+ 页中 **0 条硬性事实矛盾**——"结构让矛盾无处可活"
- 记分卡方法：写下知识库最需要回答的 **15 个问题**，冷问，每题评 single-clear / scattered。结果 **13 single-clear，2 scattered——两题都是关于品味的，活在没人写下过的决策里**。"系统是否一跳内回答真实问题，才是指标。"

#### 仍然坏掉的部分（诚实的遗留问题清单）

1. **检索质量是未决赌注**："agent 总能找到一个 plausible 的页面，而 wrong-but-plausible 比 miss 更糟，因为看起来没有东西坏了。" 工作立场：**~10,000 页以下，对结构良好的 markdown 做关键词搜索是 right-sized**；490 页离阈值远未测试到
2. **标签蔓延照样发生**：**662 个不同标签**，一次一个 plausible 标签地加上来——"agent 免费生成 plausible 标签"
3. **陈旧性成本不停**：约 **30 页**被标记为 authoritative-but-stale，尽管有 as-of 日期戳和 90 天 lint 警告
4. **写快于读**：4 月 vault 运行在 **0.68 个原始源/编译页**——"系统写得比读得快。当写作零成本，无源页成为最小阻力路径，**无发明规则是知识库和一堆非常有组织的断言之间的唯一东西**"

#### 生态佐证

- Google 2026 年 6 月发布了匹配的 open knowledge format（markdown bundles + typed frontmatter，"几乎逐字段镜像这个布局"）——作者读作"形状是对的"的趋同证据

**可靠性备注**：webvise 卖 AI 咨询/实施服务，文中有转化钩子；但方法细节（linter 行数、误报案例、页数曲线含收缩）具体到无法编造的程度，是本批来源中运维方法论最完整的一篇。

---

### 3.2 760 页 / 30 天：科技媒体的实测（中立视角）

**来源**：Is Karpathy's viral LLM wiki helpful? Mostly yes, one month in — R&D World（2026-06-12）
**URL**: https://www.rdworldonline.com/is-karpathys-viral-llm-wiki-helpful-mostly-yes-one-month-in/
（注：直接访问 403，经 r.jina.ai 阅读代理获取）

#### 现象热度（模式传播的量化）

- Karpathy 4 月发 gist 前的推文 **21M+ 阅读**；gist 本身数千 star，评论区像小型开源会议：secure-llm-wiki、AutoSci、Dense-Mem、LLM-Wiki-v3、memwiki 等一打分支

#### 设置

- raw 层：文章、访谈转录、新闻稿、PDF、**system cards**（AI 模型卡）等
- wiki 层：**Quartz 静态站生成器**托管，公开可浏览；组织为 companies/topics/products/platforms/sources/people/institutions
- 规模：**约 760 页**（文中视频是过期的 ~200 页计数）；**其中约 430 页经过足够审查上公开站，其余是构建时隐藏的草稿和骨架**

#### 纪律机制（与 3.1 高度趋同）

- schema 文档规定**允许的章节标题**；**每个事实句必须有行内引用——"没有源的声明是缺陷，不是风格选择"**；lint 脚本组守门——违规页 fail gate 而非靠 agent 的善意 slipping through
- 接 MCP server：Claude on the web 可搜 wiki、读页、拉新源、**通过受守卫的 intake 路径提议编辑而非直接写文件**
- 部分自动化已接线：**监控循环自主运行，向已审查页面追加带日期带源的事实；每次自动编辑写一条可事后审计的 ledger 条目**。更重的操作（新页/重构）仍走半手动路径

#### 一个月结论（对"值不值"的中立标定）

- **"维护 wiki 花的时间与它省我的时间大致打平（roughly a wash）。"**
- 有效场景：**综合开放网络覆盖良好的技术主题**。例：问前沿模型"哪些 LLM 最强"常得到过期/部分答案（知道某实验室最新模型但漏掉另一家或中国公司的强者）；加入一手 system cards + 第三方报道后能得到好概览——**但 Artificial Analysis 这类站点已做得更深**
- "wiki 默认不自更新，我得持续喂——但这是轻活，容易折进日常工作流"
- **反向边界："如果你做的研究开放网络已覆盖良好，除非你真要在给定主题上深钻，否则努力大概率不值。"**
- 不消除人工事实核查的必要，但结果扎实（因为主要让模型从其他文档做摘要）；幻觉风险可降：从人工审查到**基于源材料做对抗性审查的 agent**
- 长期展望：可能持续变好，"**也可能长到其规模要求新架构**"

**可靠性备注**：科技媒体作者、无产品可卖（文章末尾无转化钩子），是本批中最中立的视角；代价是数据粒度粗（无 lint 遥测、无 token 成本）。

---

## 四、横断归纳

### 4.1 什么场景 wiki 输（及为什么）

| 场景 | 证据 | 机理 |
|---|---|---|
| 短/直接事实查询 | 1.4：13 题无任何分类 wiki 准确率胜过 hybrid；token ×9.3、p50 ×2.5 | 查询路径固定吃 index+选页+读页（10-15k tokens），检索型问题用 1.4k 就够 |
| 需列全条件的 paraphrase | 1.4：wiki 单句答案丢 A/B/C 限制 | ANSWER 模板鼓励简洁 + 镜像问句的短；binary accuracy 测不出，fact-point recall 才可见 |
| 多租户/多边界隔离 | 1.4：页面合并 key 是实体名 → 跨租户政策焊进同页，confidence 0.9 的错答 | 合成阶段无租户过滤；确定性污染比偶发幻觉更难发现 |
| 开放网络已覆盖好的研究 | 3.2：Artificial Analysis 类站点做得更深；"除非深钻，否则不值" | 编译一次的综合无法胜过专职维护的公共资源 |
| 缺失一条关键数据时 | 1.3：Vault A 从不完整信息"无瑕疵地"推理出自信的错误 | 格式不是瓶颈，数据是；结构完美不补数据洞 |
| 无人读 lint 报告/无人做实体分诊 | 1.2：10 次周报零修复，154 个未决决策累积 | 检测≠修复；修复是只有 owner 能做的成卡决策 |
| 多写者写纯文件 | 2.1：index.md/log.md 是每次 ingest 的重写热点 → 必然相撞；同步丢写/冲突副本；git 给散文合并冲突 | 无锁、无乐观并发、无归属 |
| 想要模型 confidence 当信任信号 | 1.4：wiki avg confidence 更高但准确率更低，错题给 0.9 | confidence 是自评不是命中率；wiki 内部自洽所以自我感觉良好 |
| 隔着 session 的记忆 | 1.1：wiki 不是记忆，每 session 重读 | 需要独立的 daily logs + 检索层 |

### 4.2 什么场景 wiki 赢（及为什么）

| 场景 | 证据 | 机理 |
|---|---|---|
| 跨源综合（"上月日报的贯穿主线"） | 1.1："没有别的东西接近"；工作在 ingest 时发生过一次 | 检索无积累 vs 编译一次；RAG 结构上做不到 |
| 实体消解与唯一真相源 | 1.1：实体卡"每天都在回本的无聊模式" | 一实体一文件，改一处全局生效 |
| 跨源连接题 | 2.2：只有严格一源一摘要的实现答对了"连接两个不相关源"的难题 | ingest 纪律 > 检索聪明 |
| 快变小众领域的时效 | 3.2：问"哪些 LLM 最强"，wiki 加一手 system cards 后胜过前沿模型的过期答案 | 前沿模型知识有过期边界；wiki 随 ingest 保鲜 |
| 降幻觉（有纪律时） | 3.1：400+ 页 0 硬性矛盾——"结构让矛盾无处可活"；3.2："结果扎实因为让模型从其他文档摘要" | 无发明规则 + 行内引用 + owner 页注册表 |
| 领域定制 schema | 2.2：pm-llm-wiki 8.5/10，"通用模式是起点，schema 才是价值"；2.2 金句"schema 是产品的 80%" | 领域词汇/页面形状/仪式被编码进 schema |
| 人类留存 | 2.2："你不会看它就会抛弃它"——Quartz 渲染/graph view 让人回流 | 工具与习惯的区别 |
| 周期性收缩整理 | 3.1：两次页数收缩是最健康两周；薄页/重复页折进 owner | 无人维护的库只涨；gardening 信号 |
| 单人 5 分钟/天的可持续性 | 3.1：490 页 880 commit 的成本 = 每天 5 分钟 + 周日 30-45 分钟 | agent 承担了第 3 周死掉的手搓维护 |

### 4.3 维护成本的真实曲线（按规模阶段合并所有来源）

```
规模阶段            关键事件与成本                              来源
────────────────────────────────────────────────────────────────────
第 3 周            手搓 second brain 死亡线：维护停止          3.1
~30-40 页          装 drift check + 周跑 lint + 迁移规则       1.1
~50 笔记以下        别让 schema 设计阻止捕获；"乱但存在的        1.3
                  事实 > 永远不写的完美笔记"
~100+ 笔记         SCHEMA.md + 铁律"写前先读并校验"            1.3
~300 页           "偶尔 lint"变成祈祷；坏链率 0.42-0.44/页     1.1/1.2
                  线性不收敛；修复靠人不成靠脚本
~300 笔记以上       约定开始大幅回本（token 成本/新鲜度/冲突）    1.3
跨入第二领域        单一巨型 schema 活不下去 → 每领域子 schema    1.1
多领域+日报         实体策展崩溃：人名进入快于成卡；154 未决      1.2
                  决策的累积
~100k token 热内容  index 放不进 context → 按领域分片或加       1.1
                  pgvector 检索层（wiki 仍为权威层）
稳态（490 页）      5 分钟/天 + 周日 30-45 分钟 agent session    3.1
稳态（760 页）      "维护时间与省下的时间大致打平"               3.2
一次性/增量成本     bulk-build 194k tokens；增量 ingest 3-5k/源  1.4
                  重度 ingest 日 $2-4 API                     2.2
远期（~10k 页）     关键词搜索的 right-sized 上限；"可能长到     3.1/3.2
                  要求新架构"
```

**曲线形状总结**：维护成本不是随页数超线性爆炸（agent 吸收了体力活），而是**随"决策债"累积**——死链分诊、实体成卡、矛盾仲裁、品味判断。这些决策的累积速度 ≈ 新名字进入 wiki 的速度。工程手段（linter/闸门/封闭操作集）能把体力部分压到每天 5 分钟，压不掉决策部分；**没有策展预算的 wiki，决策债按周复利**（1.2 的 10 周遥测就是复利曲线）。

### 4.4 失败模式 → 对策映射总表

| # | 失败模式 | 机理 | 已验证对策 | 来源 |
|---|---|---|---|---|
| 1 | changelog 更新但参考区腐烂 | 写日志的"感觉"替代了重写现在时散文 | 迁移完成的定义 = 参考区匹配；drift linter 进 pre-commit 阻断 build | 1.1 |
| 2 | 同一实体两张卡静默重复计数 | dedup key 是名称字符串 | 实体规范化命名（wikilink 文本=文件名）；待验证：稳定实体 ID | 1.1 |
| 3 | 死链随页数线性增长 | "每个实体首次提及即加链"规则=死链生成器 | 拒绝自动建 stub（移动数字不移动问题）；实体分诊人工预算；周报必须有人周一读 | 1.2 |
| 4 | 监控假阴性 | 检查器指向退役目录扫描 0 页报"干净" | 监控监控者：校验扫描基数>0 | 1.2 |
| 5 | 自信的错误答案 | 数据不完整时完美推理 | 捕获习惯 > schema 完美；不可达层防覆盖 | 1.3 |
| 6 | 跨边界污染 | 页面合并 key 缺隔离维度 | frontmatter 必填 boundary 字段（tenant_id）+ 两阶段过滤 | 1.4 |
| 7 | 合成噪声永久焊接 | bulk-build 一次性污染，每次 query 复现 | bulk-build 后 lint pass（语种字符/重复条目/空页） | 1.4 |
| 8 | 过度简化丢限制条件 | ANSWER 模板鼓励简洁 | 显式"列出所有相关限制"指令；intent 路由到检索 | 1.4 |
| 9 | LLM 写垃圾进库 | prompt 是建议不是墙 | Zod 封闭动作词表（4 动词+长度上限）；append-only 层 schema 不可达；executors 二次校验路径 | 1.5 |
| 10 | 批准滞后/过期 | 旧批准卡晚触发 | plan 10 分钟过期；checkbox 精确到 action 索引；slug 预留防并发碰撞 | 1.5 |
| 11 | 写路径撕裂/膨胀 | 直接写目标文件 | 快照→临时文件→rename 原子写；400 行上限+溢出文件留指针 | 1.5 |
| 12 | 审计者编造证据 | lint 发现无核验 | 发现必须带 8-300 字符逐字引用，runner 重读磁盘核验 verified 标志 | 1.5 |
| 13 | 多写者写热点冲突 | index.md/log.md 每次 ingest 重写 | 退役两文件：description 入 frontmatter、log 入页面历史；写携带 base_version 乐观并发 | 2.1 |
| 14 | 规则腐烂 | 书面 guideline 一周内被漂移过 | 判断变 check：20 项检查 pre-commit strict 模式阻断 | 3.1 |
| 15 | 易变事实多副本 | "每份副本都是未来的谎言" | 一事实一 owner 页 + registry；小单主题页（检索形状最好） | 3.1 |
| 16 | prompt injection 经源文件 | 阅读清单是攻击面 | 源内嵌指令一律按不可信内容存储；文章的话不能授权 schema 变更 | 3.1 |
| 17 | "索引没有"→"不存在" | 查询早退 | 声称缺信息前必须全文搜索为空 | 3.1 |
| 18 | 聊天引用不可复开 | "用户说的"无法重放 | 聊天不是源：先落文件再引用文件 | 3.1 |
| 19 | 写快于读 | 写作零成本→无源页成最小阻力 | 监控 源/编译页 比率（4 月 0.68 是警报）；无发明规则 | 3.1 |
| 20 | 标签无限蔓延 | agent 免费生成 plausible 标签 | 约束标签词表（尚未有来源给出成功解） | 3.1 |
| 21 | 孤儿页焦虑 | 孤儿被当缺陷 | 重定义：agent 靠搜索找页时孤儿不是问题（1 孤儿 0 过期的反例） | 2.1 |
| 22 | 全自动承诺 | "按开发者的思维组织" | schema 拴住 agent；人保留品味/优先级/杀什么的决策 | 2.2/3.1 |

### 4.5 对我们项目的设计启示（避坑清单，按优先级）

**P0 — 写路径（信任是一切的前提）**
1. LLM 永不直接写散文：一切写操作走"单次受约束 completion → schema 校验（Zod 式封闭动作词表）→ executor 应用"（1.5 规则 1）
2. raw 层从 schema 上不可达：动作枚举里故意不存在能写 sources 的动作——"缺失的 enum 变体是墙"（1.5）
3. 原子写 + 快照回滚 + 页面上限 + 溢出指针（1.5 规则 3 的四重防）
4. lint/审计发现强制带逐字引用且服务端核验（1.5 规则 4）——这是对"agent 审计 agent"幻觉问题的唯一已验证解
5. 人工批准以 action 为粒度（checkbox），plan 短过期，slug 预留（1.5 规则 2）

**P1 — 检测/修复分离与策展预算（lint 的真正含义）**
6. 把"lint 报告"设计成**决策队列**而非计数仪表盘：每条死链/缺卡实体是一个待分诊决策，有 owner、有状态、可批量裁决（1.2 的教训直接产品化）
7. 绝不自动建 stub 去清零死链计数（1.2 反模式）
8. 监控监控者：lint 自身报告扫描基数、时间戳、覆盖范围（1.2 零页事故）
9. 工具间计数口径要统一（1.2 的 170 vs 185）

**P2 — 结构演化路径（对普通用户最重要的产品决策）**
10. 默认从"Pile"起步：≤50 笔记零 schema 压力，捕获习惯优先（1.3）
11. 渐进结构化按序添加：命名规范 → 常青/易变隔离 → 出处戳（1.3 顺序有依据）
12. ~100 笔记触发 SCHEMA 提示，~300 触发约定回本（1.3 阈值）
13. 跨领域时拆子 schema，顶层只留通用规则（1.1 "scoped CSS"）
14. 领域 schema 模板库是产品护城河："schema 是产品的 80%"，pm-llm-wiki 证明领域定制完胜通用（2.2）

**P3 — 并发与多 agent**
15. 从 day one 避免"每次 ingest 重写的全局文件"（index/log 是写热点）：description 入 frontmatter、历史入 page history（2.1 实测退役了 Karpathy 的两个核心文件）
16. 写操作带 base_version 乐观并发（2.1）
17. 保留 index.md 作为可选兼容层而非核心依赖——中位公开 wiki 76 页、13/46 是模板，真实使用信号是活跃 log（2.1 的 46 wiki 研究）

**P4 — 查询层**
18. 不做 either/or：wiki 为主、检索为兜底/路由（1.4 default hybrid + opt-in wiki 的镜像：个人 KB 场景 default wiki + 检索兜底）
19. paraphrase/列举类查询加"列出所有限制条件"指令或路由（1.4 失败模式 3）
20. 永不向用户展示模型 confidence 作为信任信号；用引用核验替代（1.4）
21. 声称"不知道"前强制全文搜索（3.1 query 硬底线）

**P5 — 规模天花板要作为产品路线图内置**
22. ~100k token：领域分片或加检索层，wiki 保持权威层（1.1 对策 C）
23. ~10k 页：关键词搜索上限（3.1 立场）
24. 页数收缩（consolidation）作为官方操作与正面健康信号（3.1 六操作之一 + "页数只涨=没人打理"）
25. 监控 源/编译页 比率（<1 警报）、每页坏链率、标签基数（3.1）
26. 记分卡作为产品内置评估：15 个冷问题 single-clear/scattered（3.1 方法）

**P6 — 安全**
27. 源文件内嵌指令 = 不可信内容；源说的话不能授权 schema 变更（3.1）
28. ingest 管道对输入做注入消毒假设（3.1 + 1.5 的 allowlist 思路）

### 4.6 值得带进设计讨论的未解问题（各来源自己承认的开放项）

- **检索的 wrong-but-plausible 问题**（3.1）："agent 总能找到 plausible 页面"——没有任何来源给出解
- **多文档综合的量化验证缺失**（1.4）：wiki 理论最强项（"最近什么变了"）恰恰没有 GT 覆盖——需要一个能测它的评测
- **孤儿页的定位矛盾**：1.1/1.2 视为累积问题，2.1 视为非问题（搜索找页即可）——取决于检索机制，我们的架构选型会决定站哪边
- **标签蔓延无解**（3.1 的 662 标签）：约束词表未验证
- **聚合页/枢纽页膨胀**（2.1 的 47,400 词 Dexio 页 vs 自己 schema 的 200 行规则）：自查规则自己不执行
- **维护打平点之后的价值曲线**（3.2 的"roughly a wash"）：760 页一个月打平，长期是复利还是新架构需求，无数据

---

## 附：来源清单与获取方式

| # | 来源 | URL | 获取方式 |
|---|---|---|---|
| 1 | mpt.solutions 规模化失败 | https://www.mpt.solutions/karpathys-llm-wiki-works-heres-what-broke-when-i-ran-it-at-real-scale/ | 直接 |
| 2 | mpt.solutions lint 遥测 | https://www.mpt.solutions/lint-ran-every-week-dead-link-count-never-went-down/ | 直接 |
| 3 | Medium 两个 second brain | https://medium.com/@dksingh0429/built-two-ai-second-brains-with-the-same-documents-one-gave-better-answers-heres-why-6e96483935a8 | 403 → 作者 RSS feed 全文 |
| 4 | osisdie A/B 评测 | https://osisdie.github.io/blog/2026/hybrid-vs-llm-wiki-eval/ | 直接 |
| 5 | dev.to MindBase | https://dev.to/frankchu/i-built-karpathys-llm-wiki-as-a-product-the-hard-part-was-stopping-the-llm-from-writing-819 | 直接 |
| 6 | dexio 12 实现+46 wiki | https://dexio.wiki/guides/llm-wiki-github/ | 直接（与 #10 同页） |
| 7 | Medium 5 实现横评 | https://medium.com/@aitrends24/i-tested-5-llm-wiki-implementations-so-you-don-t-have-to-d68ba7cc9100 | 403 → Wayback Machine 2026-07-12 快照 |
| 8 | webvise 3 个月报告 | https://www.webvise.io/blog/llm-wiki-3-month-report | 直接 |
| 9 | rdworldonline 一个月 | https://www.rdworldonline.com/is-karpathys-viral-llm-wiki-helpful-mostly-yes-one-month-in/ | 403 → r.jina.ai 阅读代理 |
| 10 | dexio 4-agent 运维 | https://dexio.wiki/guides/llm-wiki/ | 直接（与 #6 同页，别名 URL） |
