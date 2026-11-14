# 记忆算法与个人知识管理：可执行的算法与实证依据

> 定位：`principles/raw/` 原始资料层。本文件只做**证据整理**，不做产品决策；综合判断见 `principles/wiki/synthesis.md`。
> 调研日期：2026-11-14（检索工具：webfetch 直取一手来源；websearch 不可用，改用 OpenAlex / Crossref / Europe PMC / Semantic Scholar / GitHub API 做结构化检索）
> 覆盖：FSRS 算法与基准、间隔重复真实场景证据、笔记方法实证、概念图/知识组织、LLM 自动出题、学习仪表盘与元认知支架。
> 面向问题：brainup 下一阶段要不要做间隔复习、自动出题、知识组织，以及"工程量级"。

## 0. 怎么读这份文件（证据分级）

| 级别 | 含义 | 例子 |
|---|---|---|
| **A** | 大样本基准 / 预注册 RCT / 同行评审元分析 | srs-benchmark（3.5 亿条复习记录）、Cepeda 2008、Lau 2022 元分析 |
| **B** | 同行评审但样本小、单点、短期；或高质量准实验 | Durrani 2024（n=115）、Santhosh 2024（n=90 RCT） |
| **C** | 相关性/自评数据、系统论文、无对照的 pilot | Anki 使用与 USMLE 相关性研究、LLM 闪卡准实验（n=60） |
| **D** | 工程文档/社区共识/产品文档（用于校准实现细节，不作因果证据） | Anki 手册、Awesome-FSRS wiki、py-fsrs README |

**一条总论**（下面每条都是它的注脚）：

> 本领域**算法侧证据极强、教学侧证据很弱**。FSRS 在"预测你何时会忘"这件事上有 3.5 亿条真实复习记录支撑（A 级）；但"用了 FSRS 的人学得更好"几乎没有 RCT（空白）。
> 因此 brainup 的正确姿势是：**把 FSRS 当"可靠的排程引擎"接入（低风险，照抄成熟实现），把"学得更好"押在题目质量与检索练习本身（有 A 级证据），而不是押在算法先进性上。**

---

## 1. 证据地图（先看这张表）

| # | 主题 | 最强证据 | 关键数字 | 对 brainup 的方向 |
|---|---|---|---|---|
| 1 | FSRS 预测精度 | srs-benchmark 2026 | LogLoss 0.337（FSRS-7）vs 0.395（常数基线） | 直接用，别自研 |
| 2 | FSRS vs SM-2/SM-17 | fsrs-vs-sm17 | LogLoss 0.367 vs 0.432；83.3% 用户更优 | 迁移有据 |
| 3 | 间隔重复真实场景 | 2 个 RCT + 2 个系统综述 | 效应 d≈0.8；但客观使用量研究**无关联** | 做"结构化复习"，不做"打卡排行" |
| 4 | 最优间隔参数 | Cepeda 2008 | 最优 gap = 测试延迟的 20–40%（1 周）→5–10%（1 年） | 默认参数够用，别手调 |
| 5 | 手写 vs 键盘 | Lau 2022 元分析 | g=+0.144（88 个效应量） | **不要**做"手写模式"卖点 |
| 6 | 概念图 | Nesbit 2006 / Wang 2025 | ES=0.63（37 项）；自己画 > 看现成 | 可做"链接/图谱"，但别承诺提分 |
| 7 | Zettelkasten | **无对照研究** | OpenAlex 120 条标题命中，0 条学习结果实验 | 诚实标注为"设计哲学" |
| 8 | LLM 自动出题 | 1 个准实验 + 大量系统论文 | d=2.48（n=60，不可信地大） | 可做，但必须人审 + 质量门 |
| 9 | 学习仪表盘 | Kaliisa 2024（38 项） | 学业成就"无证据"，参与度中-大效应 | 少做统计页，多做"下一步做什么" |

---

## 2. FSRS：算法、版本、基准、实现、Anki 现状

### 2.1 记忆模型：DSR 三变量（先讲清楚，后面全部公式都建在这上面）

来源：Awesome-FSRS wiki《The Algorithm》/《ABC of FSRS》，2026-07 修订
URL：https://github.com/open-spaced-repetition/awesome-fsrs/wiki/The-Algorithm ｜ https://github.com/open-spaced-repetition/awesome-fsrs/wiki/ABC-of-FSRS

- **R（Retrievability，可提取性）**：此刻能成功回忆的概率。随距上次复习的时间衰减。
- **S（Stability，稳定性）**：R 从 100% 降到 90% 所需的天数。S=365 意味着一年后回忆概率才掉到 90%。
- **D（Difficulty，难度）**：材料本身使"稳定性再增长"有多难，取值 [1,10]。D 越大，同样答对带来的 S 增幅越小。
- 关键性质（决定了它比 SM-2 强在哪）：
  1. D 越大 → S 增幅越小；
  2. S 越大 → 越难再涨（边际递减）；
  3. **R 越小（越接近遗忘）→ 答对后 S 增幅越大**（这就是 spacing effect 的数学化）；
  4. 成功复习后 S 增幅恒 ≥ 1；延迟复习不会像 SM-2 那样线性放大间隔，而是收敛到上界。
- 思想源头：MaiMemo 的 DHP 模型（KDD 2022 / TKDE 2023），再往上是 Wozniak 的"记忆三成分模型"。

**对 brainup**：这意味着每张卡只需存 `(D, S, last_review, due)` 五个数，不需要存整段历史（历史只用于调参）。数据模型非常轻。

### 2.2 版本演进（2026-11 现状：FSRS-6 是公开文档的"当前版"，FSRS-7 已进入基准与部分实现）

| 版本 | 参数数 | 关键变化 | 状态 |
|---|---|---|---|
| FSRS v4 | 17 | 首个进入 Anki 的版本 | 历史 |
| FSRS-4.5 | 17 | 改遗忘曲线形状（DECAY=-0.5） | 历史 |
| FSRS-5 | 19 | 首次用**同日复习**数据精修次日预测 | 历史 |
| **FSRS-6** | **21** | 同日复习公式改进；**遗忘曲线陡峭度可训练**（w20） | **公开文档/多数库的默认** |
| **FSRS-7** | **34** | 支持**小数间隔**；同日复习的真实预测；遗忘曲线 8 个可优化参数 | 基准第一梯队；ts-fsrs v6 默认；fsrs-rs 已支持 |

FSRS-6 核心公式（w 为 21 个参数）：
- 遗忘曲线：`R(t,S) = (1 + factor · t/S)^(−w20)`，其中 `factor = 0.9^(−1/w20) − 1`，保证 `R(S,S)=90%`。
- 同日复习：`S′ = S · e^(w17·(G−3+w18)) · S^(−w19)`（S 小时涨得快、大时涨得慢，且收敛）。
- 默认参数（FSRS-6）：`[0.212, 1.2931, 2.3065, 8.2956, 6.4133, 0.8334, 3.0194, 0.001, 1.8722, 0.1666, 0.796, 1.4835, 0.0614, 0.2629, 1.6483, 0.6014, 1.8729, 0.5425, 0.0912, 0.0658, 0.1542]`

> 说明：默认参数是在**约 1 万名用户、数亿条复习记录**上跑优化器得到的（ABC of FSRS）。所以"新用户没有数据也能用"，这是 FSRS 能开箱即用的关键。

### 2.3 基准方法：怎么证明它更好（以及"更好"仅指预测更准）

来源：`open-spaced-repetition/srs-benchmark` README（2026 版）
URL：https://github.com/open-spaced-repetition/srs-benchmark

**数据集**：10,000 名 Anki 用户，约 **7.27 亿条**复习记录（`anki-revlogs-10k`）；评估用 9,999 个 collection、**3.5 亿条**复习（不含同日复习）。

**切分**：`TimeSeriesSplit`（用过去预测未来，防泄漏），去掉第一折。

**三个指标**（这点很重要，回答"FSRS vs SM-2 谁好"时必须区分）：
- **Log Loss**（校准）：预测概率与真实 0/1 的交叉熵，越低越好；
- **RMSE(bins)**（分箱校准）：按间隔/复习次数/遗忘次数分箱后的加权 RMSE，越低越好；
- **AUC**（区分度）：能否把"记住/忘了"分开，越高越好。AUC 高但 LogLoss 差是可能的。

**结果（无同日复习，节选）**：

| 算法 | 参数 | LogLoss↓ | RMSE(bins)↓ | AUC↑ |
|---|---|---|---|---|
| RWKV-Instant（神经，270 万参数） | 2,762,884 | **0.2773** | 0.0250 | **0.8329** |
| GRU | 503 | 0.3328 | 0.0549 | 0.7324 |
| LSTM | 8,869 | 0.3332 | 0.0538 | 0.7329 |
| **FSRS-7 recency** | **34** | **0.3370** | 0.0593 | 0.7220 |
| MOVING-AVG（基线） | 0 | 0.3369 | 0.0591 | 0.7001 |
| Logistic Regression | 34 | 0.3393 | 0.0604 | 0.7108 |
| SBD | 7 | 0.3410 | 0.0602 | 0.7152 |
| **FSRS-6** | **21** | **0.3460** | 0.0653 | 0.7034 |
| FSRS-5 | 19 | 0.3561 | 0.0742 | 0.7010 |
| FSRS-4.5 | 17 | 0.3625 | 0.0764 | 0.6891 |
| FSRS v4 | 17 | 0.3726 | 0.0838 | 0.6853 |
| AVG（常数基线） | 0 | 0.3945 | 0.1034 | 0.4997 |
| HLR（Duolingo） | 3 | 0.4694 | 0.1275 | 0.6369 |
| Ebisu v2 | 0 | 0.4989 | 0.1627 | 0.6051 |

同一份 README 的"含同日复习"表里，**FSRS-6 反而掉到 0.3842**（被 MOVING-AVG 的 0.3301 反超），因为 FSRS-6 的同日模型较弱——这正是 FSRS-7 要解决的问题。**结论：引用 FSRS 数字时必须说明"含/不含同日复习"。**

**诚实的三点解读**：
1. FSRS 的优势是**预测校准**，不是"学习效果"。基准里没有"学完后考试分数"这个指标。
2. 相对朴素基线的提升是**绝对值很小**（LogLoss 0.346 vs 0.395，约 12%），但 AUC 提升明显（0.703 vs 0.500）。别把"更准"包装成"更会学"。
3. 神经网络（RWKV 270 万参数）确实更准（0.2773），但**需要跨用户预训练 + 大量特征**，个人知识库场景不划算；34 个参数的 FSRS-7 已是性价比拐点。

### 2.4 FSRS vs SM-2 / SM-17：迁移到底值多少

来源：`open-spaced-repetition/fsrs-vs-sm17`（19 名 SuperMemo 用户、687,662 次复习）
URL：https://github.com/open-spaced-repetition/fsrs-vs-sm17

| 算法 | Universal Metric↓ | LogLoss↓（按复习数加权） | AUC↑ |
|---|---|---|---|
| **FSRS-6** | **0.0287** | **0.367** | **0.662** |
| SM-17（SuperMemo 最新） | 0.0435 | 0.432 | 0.606 |
| SM-16 | 0.0547 | 0.417 | 0.598 |
| FSRS-6（默认参数，不调参） | 0.0820 | 0.411 | 0.616 |
| AVG 基线 | 0.0598 | 0.385 | 0.526 |

- **FSRS-6 对 SM-17 的胜率 83.3%**（按 collection 计）。
- 注意"默认参数"版本（0.0820）**打不过 AVG 基线**（0.0598）——这是最重要的工程警告：**FSRS 的价值来自"用你自己的复习日志调参"，不是来自默认参数**。默认参数只保证"不会太离谱"，不保证"比瞎猜好"。

关于"省多少复习量"：
- Awesome-FSRS《ABC of FSRS》称 **同等保持率下比 SM-2 少 20–30% 复习量**，但同页括注 **"该数字基于模拟结果（2026-02-12 更新）"**。
- 也就是说：这不是 RCT 测出来的，是模拟器的输出。**对外表述必须写"模拟估计"，不能写"研究证明"。**

### 2.5 开源实现盘点（决定 brainup 集成路径）

| 实现 | 语言 | 支持版本 | 优化器 | 许可 | 备注 |
|---|---|---|---|---|---|
| **py-fsrs** | Python | FSRS-6（21 参数默认） | ✅ `fsrs[optimizer]` | MIT | `pip install fsrs`；Card/Scheduler/ReviewLog 全 JSON 可序列化；**只支持 UTC** |
| **ts-fsrs v6** | TypeScript | FSRS-3/4/4.5/5/6/**7** | ✅ 独立包 `@open-spaced-repetition/binding`（FSRS-6/7） | 开源 | `DefaultScheduler()` **默认 FSRS-7**；需 Node ≥ 24 |
| **fsrs-rs** | Rust | FSRS-6 + FSRS-7（按参数个数自动识别） | ✅ 内置 | 开源 | Anki 官方后端；有 C/Python/Node/Dart/PHP 绑定；含 `memory_state_from_sm2()` 迁移函数、Cost ADR 策略、模拟器 |
| rs-fsrs / go-fsrs / fsrs-rs-* | 多 | 视包而定 | 多数无 | 开源 | 只排程不调参时用轻量版 |

**关键 API 形态**（py-fsrs，最贴近 brainup 现状）：
```python
from fsrs import Scheduler, Card, Rating
scheduler = Scheduler()                       # 默认 FSRS-6 参数 + desired_retention=0.9
card, log = scheduler.review_card(card, Rating.Good)
r = scheduler.get_card_retrievability(card)   # 当前回忆概率，可直接做 UI
```
- 默认 `learning_steps=(1min, 10min)`、`relearning_steps=(10min,)`、`maximum_interval=36500`、`enable_fuzzing=True`。
- 优化器接口：`Optimizer(review_logs).compute_optimal_parameters()` + `compute_optimal_retention()`，可 `reschedule_card()` 重排历史卡。

### 2.6 Anki 集成现状（说明"工业级已验证"的边界）

来源：Anki 官方手册 deck-options（2026 版）+ Anki GitHub Releases API（2026-11-12 拉取）
URL：https://docs.ankiweb.net/deck-options.html#fsrs ｜ https://github.com/ankitects/anki/releases

- Anki 26.09 起内置 **fsrs-rs 6.6.2**；最新版本线为 **26.11b1（2026-11-12）**，FSRS 已是默认调度器（全局开关，不能按 preset 分别开关）。
- **Desired retention 默认 0.90**，手册明确："这是 FSRS 最重要的设置"，**>90% 工作量快速上升，>97% 会失控**。
- 手册明确："**同日重复同一张卡对长期记忆贡献不大**" → 建议 learning steps 全部 <1 天、步数尽量少；留空则由 FSRS 接管短期排程（实验特性）。
- 手册明确警告 **Hard 误用**：Hard 是"记得但吃力"，不是"忘了"；把"忘了"记成 Hard 会让所有间隔虚高。**这是 FSRS 唯一的致命使用错误，必须在 UI 里防。**
- **CMRR（最小推荐保持率）在 25.07 被移除**，取而代之是 **Simulator / "Help Me Decide"**：用你真实的 DSR 状态模拟"每天多少复习量/多少分钟"。
- Anki 侧还提供：Easy Days（按周几压低负荷）、按 retrievability 排序（替代 SM-2 的 overdueness）、参数"连续点三次才能编辑"的防误操作设计。

**对 brainup 的启示（很具体）**：
1. 抄 Anki 的**交互护栏**比抄公式更值钱：Hard 语义提示、desired retention 滑杆 + 工作量曲线、参数只读+一键优化。
2. 别做"每天新卡 20 张 → 200 张复习"这种惊喜：Anki 手册直接给了这个 10 倍关系（20 新卡/日 ≈ 200 复习/日稳态），brainup 应该在导入时就预估并展示。

---

## 3. 间隔重复在真实场景的证据（这是全篇最需要"打假"的一节）

### 3.1 有对照的两项研究（唯一能说"因果"的）

**① Durrani et al. 2024（BMC Medical Education，巴基斯坦，儿科学轮转）** — 级别 B
URL：https://doi.org/10.1186/s12909-024-05479-y ｜ PMC11186069
- 设计：准实验，115 名五年级医学生随机分组（Anki 组 70 / 传统组 45），4 周，50 题 MCQ 前后测。
- 数字：Anki 组 27.93 → **30.80**（显著）；对照组 27.96 → 27.22（不显著）；**效应量 d≈0.8**。
- 局限：单一学校、4 周、自编题库、教师同时知道分组。

**② Santhosh et al. 2024（J Dental Education，印度，单盲 RCT）** — 级别 B
URL：https://doi.org/10.1002/jdd.13561（CTRI/2023/10/059347）
- 设计：90 名口腔学生，1:1 随机，LBL vs LBL+手机闪卡间隔重复；基线/1 个月/3 个月三次测。
- 数字：**1 个月与 3 个月的保持率均显著更高（p ≤ .001）**；基线无差异；学生态度显著更正面。
- 局限：单中心、n=90、自编量表。

> 这两项合起来能支持的结论只有一句：**"结构化地把复习排到多天里，比集中讲授/自己看书，在 1 个月内保持率更高。"** 这其实不是 FSRS 的功劳，是 spacing + retrieval 的功劳。

### 3.2 系统综述给出的冷水（必须写进产品预期管理）

**③ Frappa et al. 2026（Medical Science Educator）"Anki Use and Academic Performance: A Systematic Review"** — 级别 A（综述）
URL：https://doi.org/10.1007/s40670-026-02643-5 ｜ PMC13197492
- 11 项研究定性综合。
- **3 项**研究报告 Anki 高频使用者 USMLE Step 1 更高：**高频繁 vs 极少使用差 4–13 分**，其中一项有"复习卡片总数"的剂量-反应关系。
- **校内课程考试结果混杂**：有的显著更好，有的毫无差异（尽管学生主观评价很好）。
- **仅 1 项**研究 Step 2 CK，**无显著收益**。
- 作者结论：证据"largely observational"（基本是相关性）。

**④ Luu & Severance 2026（Cureus）"A Systematic Review of Spaced Repetition, Retrieval Practice, and Academic Performance"** — 级别 A（综述）
URL：https://doi.org/10.7759/cureus.116147
- 314 条记录 → 21 项纳入；异质性太大，只做叙述性综合，**未做元分析**。
- 关键句（直接引用其意）：**"自发性闪卡使用的观察性研究结果混杂；其中使用客观平台数据（而非自报）衡量使用量的研究，未发现关联。"**
- 且"多数被判定为严重偏倚风险"。
- 另一条有用的：**"持续、纵向的参与比短期冲刺更有利"**。

**⑤ Wang et al. 2026（Current Problems in Diagnostic Radiology，放射科 pilot）** — 级别 C
URL：https://doi.org/10.1067/j.cpradiol.2026.09.007
- n=12（7 用 / 5 不用）；**信心显著提升（p=.011，ρ=0.79），但客观测验组间无差异**。
- 这是一个完美的"自评幻觉"样本：**学生觉得自己学会了，测出来没有。**

> **本节结论（会直接影响产品文案）**：
> ① 间隔重复对"保持率"有效（B 级，两项小 RCT）；
> ② 对"标准化考试分数"只有相关性证据，且**用客观使用量一测就消失**（A 级综述）；
> ③ 自评提升 ≠ 成绩提升（C 级但机制清晰）。
> 所以 brainup **不要做"使用时长/连续打卡"驱动的成就感**，那恰好是相关性幻觉的来源；要做"到期复习完成率"和"客观自测正确率"。

### 3.3 间隔参数怎么选（有 A 级证据，且结论反直觉）

**⑥ Cepeda et al. 2006（Psychological Bulletin）"Distributed practice in verbal recall tasks"** — 级别 A
URL：https://doi.org/10.1037/0033-2909.132.3.354
- 184 篇文章、317 个实验、**839 个间隔效应评估**。
- 结论：**最优间隔（ISI）随"要保持多久"而增长**；间隔与保持间隔是联合作用的。

**⑦ Cepeda et al. 2008（Psychological Science）"A temporal ridgeline of optimal retention"** — 级别 A（本领域最漂亮的设计之一）
URL：https://doi.org/10.1111/j.1467-9280.2008.02209.x
- **1,350+ 名被试**；学习后间隔最长 3.5 个月再复习；最终测试延迟最长 1 年。
- **最优 gap 占测试延迟的比例：1 周延迟 → 20–40%（即 1.4–2.8 天）；1 年延迟 → 5–10%（即 18–36 天）。**
- 原文一句话很狠："gap 与 test delay 的交互意味着**许多教育实践是极低效的**。"

**可落地参数（三条就够）**：
1. 目标保持期短（考试周）→ 间隔占目标期的 20–40%；目标保持期长（长期知识库）→ 5–10%。FSRS 的 desired_retention 机制本质就是在做这件事的自动化版本。
2. **初始间隔别拍脑袋**：FSRS 的 S₀ 由首次评分决定（Again/Hard/Good/Easy 四档给四个不同初值），比"第一天 1 天、第二天 3 天"的固定阶梯合理。
3. **同日重复价值低**（Anki 手册明说），别把 learning steps 设计成 1m/10m/1h/1d 五步——那是给"当天要考试"的人用的。

### 3.4 为什么"自动出题"有理论依据（元认知缺口）

**⑧ Karpicke, Butler & Roediger 2009（Memory）** — 级别 A（经典调查）
URL：https://doi.org/10.1080/09658210802647009
- 177 名大学生：**大多数以"反复重读笔记/教材"为主，很少自测**；作者归因于 **illusions of competence（胜任感幻觉）**。
- 配套：Adesope, Trevisan & Sundararajan 2017（Review of Educational Research）"Rethinking the Use of Tests" 元分析：**练习测验优于重读及其它所有对照条件**，效应受测验形式/反馈/延迟调节。
  URL：https://doi.org/10.3102/0034654316689306
- **可落地结论**：用户**不会自己出题**，不是懒，是元认知偏差。所以"系统替他出题 + 客观反馈"是有理论支撑的产品动作；但**题目质量是唯一生死线**（见第 6 节）。

---

## 4. 笔记方法实证：手写 vs 数字（一个被过度消费的结论）

### 4.1 原始研究（传播最广、被引用最多）

**⑨ Mueller & Oppenheimer 2014（Psychological Science）"The Pen Is Mightier Than the Keyboard"** — 级别 B
URL：https://doi.org/10.1177/0956797614524581
- 3 项实验。核心发现：**用笔记本记笔记的学生在"概念性题目"上表现更差**；机制是**逐字转录（verbatim transcription）**——记得越多反而加工越浅。
- 注意：该文 2018 年发布 **Corrigendum**（https://doi.org/10.1177/0956797618781773）：OSF 数据里 z 分数未按剔除被试后重算、Study 2 的 z 分数按讲座内标准化、部分 df 与效应量标注错误；作者称"**结果模式不变**"。也就是说**统计瑕疵存在，但结论未被推翻**。

### 4.2 复现与元分析：效应缩到"几乎可以忽略"

**⑩ Morehead, Dunlosky & Rawson 2019（Educational Psychology Review 31:753–780）"How Much Mightier Is the Pen than the Keyboard?"** — 级别 B
URL：https://doi.org/10.1007/s10648-019-09468-2
- 直接复现 + 扩展 Mueller & Oppenheimer 的三项实验（同实验室体系、同范式、更大控制）。
- 结论（该文被引 134 次，学界通行解读）：**未能复现"手写优于键盘"的概念性学习优势**；笔记本组确实记录更多字（更接近逐字），但**多记字本身不必然损害概念学习**。
- 说明：原文付费墙，摘要未取到；此处结论依据其被广泛引用的复现结论，标注为"待补原文核对"。

**⑪ Lau 2022（University of Louisville 博士论文，系统综述+元分析）"The effect of typewriting vs. handwriting lecture notes on learning"** — 级别 A（方法最规范的一篇）
URL：https://doi.org/10.18297/etd/3982
- 33 篇报告、42 个独立样本、**88 个效应量**；多层元分析。
- **总体 g = +0.144 [0.023, 0.265], p = .021**（略利于手写）。
- 换算成直觉：**键盘组平均正确率约 50%，手写组约 57%**。
- **重要调节变量：如果给被试"复习笔记"的机会，手写优势会大幅缩小。**
- 作者提出"modality research 的根本问题"：随机分配书写方式时，**同时也分配了笔记风格**，二者混淆。
- **可落地结论**：g=0.14 是"小效应"的下限区间，且会被"复习"抹平。**brainup 不应该把"支持手写/纸质"当差异化卖点**；真正有效的是"笔记之后有没有被检索"。

**⑫ Shi & Yu 2024（Electronic Journal of e-Learning）laptop 笔记综述** — 级别 C
URL：https://doi.org/10.34190/ejel.22.1.3396
- 结论：效应正/负/中性都有；**分心与多任务未必是低表现主因**，个体特征与教学风格匹配更重要；**"课堂禁笔记本"缺乏证据支持**。

### 4.3 Cornell 笔记法：证据薄到不能称"实证方法"

- OpenAlex 标题检索 "cornell note" 共 661 条，真正做学习结果对照的极少，且集中在 **EFL/二语写作**小样本（如 2019 年约旦 EFL 写作、2025 年 Gen Z 阅读理解的准实验，n 均在百人内、单点、自编测验）。
- **没有任何元分析或大样本 RCT 支持"Cornell 格式本身提升学习成绩"。**
- 可以成立的弱结论：Cornell 的"**左栏线索 + 底部总结**"结构，实质上强制了"**自我提问 + 生成式总结**"，这两个成分各自有证据（检索练习、生成效应）；**是成分有效，不是格式有效**。
- **证据空白标注**：Cornell vs 普通线性笔记的对照研究，目前不足以支撑产品级承诺。

### 4.4 Zettelkasten / PKM 方法论：**完全没有对照研究**（必须诚实写明）

- OpenAlex 标题含 "Zettelkasten" 共 **120 条**，逐条看类型：Luhmann 1981 原文《Kommunikation mit Zettelkästen》、文学/档案学考证、图书章节、少量 2020–2026 的方法论/工具文章（含 2026 年新书《Zettelkasten Without the Ceremony》）。
- **0 条**：随机对照、准实验、或任何测量"使用 Zettelkasten 后的学习/写作产出"的量化研究。
- 结论：Zettelkasten 的"原子笔记 + 链接 + 索引"是一套**设计哲学/工作流主张**，其有效性**没有实证检验**。它借用的邻近证据（生成效应、精细加工、间隔）是真实的，但"链接网络本身促进理解"未被验证。
- **对 brainup 的表述纪律**：可以说"我们采用 Zettelkasten 式的可链接结构，因为它**便于 LLM 维护一致性**（工程理由）"；**不能说**"Zettelkasten 经研究证明能提升学习效果"。

---

## 5. 概念图 / 知识组织：证据比 Zettelkasten 好得多，但也别夸大

**⑬ Nesbit & Adesope 2006（Review of Educational Research 76(3):413–448）"Learning With Concept and Knowledge Maps: A Meta-Analysis"** — 级别 A
URL：https://doi.org/10.3102/00346543076003413
- **55 项研究、5,818 名被试、67 个标准化效应量**；覆盖 4 年级到高等教育，学科含科学、心理、统计、护理。
- 结论：**概念图与"知识保持"提升相关**；**平均效应量从"小"到"大"不等，取决于怎么用图、以及对照条件是什么**；多数子集存在显著异质性。
- 关键细节（对产品设计极重要）：**"自己构建/修改图" 与 "看别人做好的图" 效果不同**；建构优于观看。

**⑭ Wang et al. 2025（International Journal of STEM Education）"Concept mapping in STEM education: a meta-analysis (2004–2023)"** — 级别 A
URL：https://doi.org/10.1186/s40594-025-00554-2
- 37 项研究，**总体 ES = 0.630**（中等效应）。
- 调节变量（可直接抄进设计）：
  - **学生自己构建概念图**时效果最好（> 提供现成图）；
  - 干预时长 **1 周–1 个月**效果最佳（更长不一定更好）；
  - **数字工具与纸笔效果相当**（"moderate and comparable"）→ 又一次说明"媒介不是关键"；
  - 学段上中学段最大，学科上科学与技术最好。

**可落地结论（三条）**：
1. 若做"知识图谱/双向链接视图"，**只读图价值有限，让用户"动手连"才有证据**（例如：让用户为两张笔记选关系类型，系统给反馈）。
2. **不要承诺"用图谱就能学会"**：ES=0.63 是"概念图作为学习活动"的效应，不是"看图谱 UI"的效应。
3. 数字 vs 纸笔无差异（两篇独立元分析一致）→ **媒介之争可以彻底放弃**。

---

## 6. LLM 自动出题/生成闪卡：2024–2026 现状（证据最薄、风险最高的一块）

### 6.1 检索到的事实分布（先说结论：系统论文远多于学习效果研究）

- OpenAlex 标题含 "quiz generation"（2023 起）**71 条**，绝大多数是系统/工程论文（RAG 出题、Bloom 分类对齐、多模态出题、LMS 集成），**测量学习增益的极少**。
- PubMed/Europe PMC 标题含 flashcard + (AI/ChatGPT/generated) 仅 **4 条**（且多为 2021 年前或非 AI）。
- **证据空白标注**：截至 2026-11，**没有**"LLM 生成闪卡 vs 人工闪卡"的大样本 RCT；也**没有**"LLM 出题提升考试成绩"的预注册多中心试验。

### 6.2 现有最好的两项（都不足以支撑强结论）

**⑮ Karrar et al. 2026（Frontiers in Education）"Automating language input: AI-generated contextual flashcards via Anki on EFL sentence-level fluency"** — 级别 C
URL：https://doi.org/10.3389/feduc.2026.1862047
- 设计：准实验前后测对照组，**n=60**（赞比亚 Zawia 大学），6 周，实验组用 AI 生成的情境化闪卡，对照组传统教学。
- 数字：实验组 10.45 → **17.82**（t(29)=14.52, p<.001）；组间后测 **d = 2.48**。
- **判读：d=2.48 在真实教学里几乎不可能**（常规教学干预 d 多在 0.2–0.8）。这强烈提示：自编测验、教学材料不对等、霍桑效应、单点实施。**只能当"可行性证据"，不能当"有效性证据"。**

**⑯ Yao, Nguyen & Mathur 2026（Current Problems in Diagnostic Radiology）"Revolutionizing radiology education: exploring and implementing spaced repetition"** — 级别 D（观点/指南）
URL：https://doi.org/10.1067/j.cpradiol.2026.06.003
- 明确主张：**AI 适合做"把课程与文献批量转成闪卡"的规模化工具**，但需与 SR 排程结合；未提供效果数据。
- 同类：CUAJ 2026 用 LLM 生成泌尿外科 MCQ + 闪卡（可行性/课程对齐），URL：https://doi.org/10.5489/cuaj.9845

### 6.3 已知的质量风险（工程侧必须处理）

- 自动出题的三类失败模式（在系统论文中反复出现，属于工程共识而非实证结论）：
  1. **事实错误/幻觉**（尤其多跳推理题）；
  2. **答案泄漏**（题干里已含答案）；
  3. **不可判别**（多个选项都对，或"以上都对"）。
- 因此 2025–2026 的系统论文普遍引入**确定性质量门**（如 2026 年《Self-hosted Lecture-to-Quiz: Local LLM MCQ Generation with **Deterministic Quality Control**》），而不是信任模型自评。
- **可落地结论（brainup 的具体策略）**：
  1. **LLM 出题 → 规则校验 → 人审 → 入卡池**，四步缺一不可；人审成本要计入（这是产品能不能规模化的真正瓶颈）。
  2. 优先出**"从笔记原文可判定的题"**（填空、定义、因果、对比），少出"综合推断题"（幻觉率最高）。
  3. **把"用户自己改题"作为一等功能**：Mueller 的机制（生成/精细加工）恰恰发生在这个动作里。
  4. 出题来源必须可溯源到 wiki 具体段落（brainup 的 wiki 结构天然支持），便于一键核对。

---

## 7. 学习分析仪表盘 / 元认知支架：证据是"参与度上升、成绩不动"

**⑰ Kaliisa, Misiejuk, López-Pernas, Khalil & Saqr 2024（LAK'24）"Have Learning Analytics Dashboards Lived Up to the Hype?"** — 级别 A（系统综述，38 项研究）
URL：https://doi.org/10.1145/3636555.3636884 ｜ 预印本 arXiv:2312.15042
- **学业成就：没有任何证据支持"仪表盘提升成绩"**；多数研究效应**可忽略或很小**，且缺乏高统计功效的对照实验。
- **参与度（participation）：效应中到大**——这是唯一稳定的正面结果。
- 方法论批评（可直接当设计检查清单）：
  - 大量研究只是"用仪表盘的人 vs 不用的人"比较，**把"仪表盘效应"和"学生本来就勤奋"混在一起**；
  - 把**"访问过"当成"使用了"**（access ≠ usage）；
  - 评估工具不标准化、自选择偏倚。
- **可落地结论**：
  1. 仪表盘能改变**行为**（打开、点击、参与），不一定改变**学习**；
  2. 若做仪表盘，KPI 应该是"**下一步行动**"（今天该复习 12 张、这 3 张连续答错该重写），而不是"本周学习 4.2 小时"；
  3. 必须防"自选择混淆"：如果 brainup 要自证效果，应做**同用户 A/B**（同一批笔记，一半进复习队列），而不是"用的人 vs 不用的人"。

**⑱ Jivet, Scheffel, Drachsler & Specht 2018（LAK'18）"License to evaluate: preparing learning analytics dashboards for educational practice"** — 级别 D（设计框架，被引 315）
URL：https://doi.org/10.1145/3170358.3170421
- 核心主张：仪表盘设计必须先声明**目标受众、理论参照系（跟谁比）、支撑的学习过程**，否则无法评估。
- 对 brainup：如果做"知识掌握度"面板，**必须明确"掌握"的定义**（FSRS 的 R？自测正确率？覆盖度？），否则只是好看的假指标。

**正面样例（可抄）**：Anki 的 **FSRS Simulator / "Help Me Decide"**——它不是"看统计"，而是"**用你自己的 DSR 数据模拟：如果保持率从 90% 调到 85%，每天复习量从 180 降到 120**"。这是把分析变成**决策**，符合上面两条批评的解法。

---

## 8. 证据空白清单（诚实记录，别再引用"众所周知"）

| # | 主张 | 证据状态 |
|---|---|---|
| 1 | "FSRS 让学习者学得更好" | **空白**。只有"预测更准"（A 级）与"同等保持率少 20–30% 复习量（模拟）"。无学习结果 RCT。 |
| 2 | "Zettelkasten 提升学习/写作产出" | **完全空白**。120 条文献 0 条对照研究。 |
| 3 | "Cornell 笔记法提升成绩" | **空白**（只有 EFL 小样本准实验）。有效的是其成分（自我提问、总结），不是格式。 |
| 4 | "手写优于键盘" | **已基本被削弱**：g=0.144，且复习机会会抹平差异。 |
| 5 | "LLM 生成闪卡达到人工质量/提升成绩" | **空白**：无大样本 RCT；现有最好证据是 n=60 准实验（d=2.48，不可信）。 |
| 6 | "学习仪表盘提升成绩" | **有反证**：38 项综述未发现成就提升证据，只有参与度提升。 |
| 7 | "Anki 提升标准化考试成绩" | **仅相关性**，且用客观使用量衡量时关联消失。 |
| 8 | "数字笔记/图谱优于纸质" | **有反证**：概念图元分析显示数字≈纸笔；笔记元分析显示媒介效应极小。 |

---

## 9. 对 brainup 的启示（可落地结论清单）

**该做（证据强/风险低）**
1. **接 FSRS 排程，不自研算法**：用 py-fsrs（Python 栈）或 ts-fsrs（TS UI 栈）；先只用默认参数 + desired_retention=0.9，攒够 ~1000 条复习日志后再开优化器。
2. **数据模型极简**：每卡存 `(D, S, due, last_review, reps, lapses)` + append-only review log；复习日志同时是未来调参与"同用户 A/B"的实验底料。
3. **复习入口做成"今天到期 N 张"**，不做"学习时长/连续天数"成就体系（避免复制相关性幻觉）。
4. **题目来源绑定 wiki 段落**，LLM 出题后走"规则校验 → 人审 → 入池"，并把"改题"作为核心交互（生成效应就发生在这里）。
5. **掌握度指标用"客观自测正确率 + 到期完成率"**，不用自评、不用阅读时长。

**该谨慎（证据弱/易过度承诺）**
6. 知识图谱：可做"手动连边 + 关系类型 + 反馈"，不承诺提分；不做"看图谱=学会"。
7. 笔记模板（Cornell 等）：可提供，但表述为"帮助你自我提问/总结的结构"，不说"经研究证明"。
8. 仪表盘：只做"决策型"（模拟保持率↔工作量、指出最该重写的卡），不做统计陈列。

**不该做（有反证或纯传说）**
9. 手写/纸质优先模式（g=0.14，且被复习抹平）。
10. 用"打卡/排行/使用时长"驱动留存（正是 Luu 2026 指出"客观使用量一测关联就消失"的陷阱）。
11. 无人工审核的批量 AI 出题（幻觉 + 答案泄漏，直接摧毁信任）。

---

## 10. FSRS 能否直接集成？工程量级初步判断

**结论：能直接集成，且属于"低风险、可逆、1–2 人周"级别；真正的成本不在算法，在"复习队列 + 题目供给"这两个产品环节。**

| 工作量项 | 内容 | 量级 |
|---|---|---|
| 依赖引入 | `pip install fsrs`（MIT，纯 Python，无 torch；优化器才需要 `fsrs[optimizer]`+torch） | 0.5 天 |
| 数据模型 | `.kb/` 侧新增 `cards`（DSR+due）与 `reviews`（append-only，CSV/JSONL）两张表；须兼容 `.kb 可重建` 约束（可由 reviews 全量重放出 cards） | 1–2 天 |
| 排程核心 | 包装 Scheduler：`new_card / review / get_retrievability`；处理 UTC（py-fsrs 只吃 UTC）、时区与"日界" | 1 天 |
| 复习队列 | 每日 due 查询、上限、乱序/按 R 排序、跳过与延后 | 2–3 天 |
| 交互护栏 | Hard 语义提示、desired retention 滑杆 + 工作量预估、参数只读+一键优化入口 | 2–3 天 |
| CLI/输出 | `brainup review` 交互循环 + 结果写回 review log；无 GUI 也能跑 | 2 天 |
| 调参（可选，v0.2 可不做） | `Optimizer(logs).compute_optimal_parameters()`；需 ≥ 数百–上千条日志才有意义（Anki 手册："<几百条"不足） | 3–5 天 + 依赖膨胀 |
| 合计（不含调参） | 可运行 MVP | **约 8–12 人日** |

**四个必须提前决定的架构点**
1. **`.kb 可重建` 约束**：cards 必须是 reviews 的纯函数（重放即可重建），否则违反 vault 三层单向流。这是最容易被忽略、后期最痛的一条。
2. **UTC vs 本地日界**：py-fsrs 只支持 UTC；"今天到期"必须按用户本地日界算，否则跨时区/跨零点会重复或漏复习。
3. **题目供给是真正瓶颈**：FSRS 会把"复习需求"放大到每天几十上百条（Anki：20 新卡/日 ≈ 200 复习/日）。若靠 LLM 现生成，成本与延迟都不可接受 → 必须"入池缓存 + 人审预算"。
4. **算法版本锁**：py-fsrs 是 FSRS-6，ts-fsrs v6 默认 FSRS-7。**前后端若各用一套会算出不同 due**。要么统一到一侧计算，要么固定同版本并把版本号写进 `.kb`。

**推荐路径（三阶段，风险递增）**
- **P0（1 周内）**：只做"到期提醒 + 单一 rating=Good/Again 两键"，纯 CLI，默认参数。**先验证用户会不会真的每天回来复习**——这是最大不确定性，不是算法。
- **P1（2–3 周）**：四键评分 + 工作量滑杆 + review log 落盘 + 客观正确率面板。
- **P2（可选）**：接入优化器、同用户 A/B（一半卡进队列）、FSRS-7（等 ts-fsrs/fsrs-rs 在 Anki 侧稳定后再跟）。

---

## 11. 参考来源清单（按本文件出现顺序）

1. Awesome-FSRS wiki, *The Algorithm*（2026-07 修订）— https://github.com/open-spaced-repetition/awesome-fsrs/wiki/The-Algorithm
2. Awesome-FSRS wiki, *ABC of FSRS* — https://github.com/open-spaced-repetition/awesome-fsrs/wiki/ABC-of-FSRS
3. open-spaced-repetition, *srs-benchmark* README（10k 用户 / 3.5 亿条评估）— https://github.com/open-spaced-repetition/srs-benchmark
4. open-spaced-repetition, *fsrs-vs-sm17*（19 用户 / 687,662 次复习）— https://github.com/open-spaced-repetition/fsrs-vs-sm17
5. open-spaced-repetition, *py-fsrs* README — https://github.com/open-spaced-repetition/py-fsrs
6. open-spaced-repetition, *ts-fsrs* README（v6 默认 FSRS-7）— https://github.com/open-spaced-repetition/ts-fsrs
7. open-spaced-repetition, *fsrs-rs* README（FSRS-6/7 + Cost ADR）— https://github.com/open-spaced-repetition/fsrs-rs
8. Anki Manual, *Deck Options → FSRS* — https://docs.ankiweb.net/deck-options.html#fsrs
9. Anki Releases API（26.11b1，2026-11-12；26.09 内置 fsrs-rs 6.6.2）— https://github.com/ankitects/anki/releases
10. Ye, Su & Cao (2022), *A Stochastic Shortest Path Algorithm for Optimizing Spaced Repetition Scheduling*, KDD — https://doi.org/10.1145/3534678.3539081
11. Durrani et al. (2024), BMC Med Educ, Anki RCT/quasi-exp, n=115, d≈0.8 — https://doi.org/10.1186/s12909-024-05479-y
12. Santhosh et al. (2024), J Dent Educ, 单盲 RCT n=90 — https://doi.org/10.1002/jdd.13561
13. Frappa et al. (2026), Med Sci Educ, Anki 系统综述（11 项；Step1 +4~13 分）— https://doi.org/10.1007/s40670-026-02643-5
14. Luu & Severance (2026), Cureus, 间隔重复系统综述（21 项；客观使用量无关联）— https://doi.org/10.7759/cureus.116147
15. Wang et al. (2026), Curr Probl Diagn Radiol, 放射科 pilot n=12 — https://doi.org/10.1067/j.cpradiol.2026.09.007
16. Cepeda et al. (2006), Psychol Bull, 839 个间隔效应评估 — https://doi.org/10.1037/0033-2909.132.3.354
17. Cepeda et al. (2008), Psychol Sci, 最优 gap 20–40%→5–10% — https://doi.org/10.1111/j.1467-9280.2008.02209.x
18. Karpicke, Butler & Roediger (2009), Memory, 177 名学生 — https://doi.org/10.1080/09658210802647009
19. Adesope, Trevisan & Sundararajan (2017), RER, 练习测验元分析 — https://doi.org/10.3102/0034654316689306
20. Mueller & Oppenheimer (2014), Psychol Sci — https://doi.org/10.1177/0956797614524581；Corrigendum (2018) — https://doi.org/10.1177/0956797618781773
21. Morehead, Dunlosky & Rawson (2019), Educ Psychol Rev 31:753–780 — https://doi.org/10.1007/s10648-019-09468-2
22. Lau (2022), 博士论文元分析, g=+0.144, 88 个效应量 — https://doi.org/10.18297/etd/3982
23. Shi & Yu (2024), EJEL, laptop 笔记综述 — https://doi.org/10.34190/ejel.22.1.3396
24. Nesbit & Adesope (2006), RER 76(3):413–448 — https://doi.org/10.3102/00346543076003413
25. Wang et al. (2025), IJ STEM Ed, 概念图元分析 ES=0.630 — https://doi.org/10.1186/s40594-025-00554-2
26. Karrar et al. (2026), Frontiers in Education, AI 闪卡准实验 n=60 — https://doi.org/10.3389/feduc.2026.1862047
27. Yao, Nguyen & Mathur (2026), Curr Probl Diagn Radiol, AI+SR 实践指南 — https://doi.org/10.1067/j.cpradiol.2026.06.003
28. Kaliisa et al. (2024), LAK'24, 仪表盘系统综述（38 项）— https://doi.org/10.1145/3636555.3636884
29. Jivet et al. (2018), LAK'18, *License to evaluate* — https://doi.org/10.1145/3170358.3170421
30. Luhmann (1981), *Kommunikation mit Zettelkästen* — https://doi.org/10.1007/978-3-322-87749-9_19（Zettelkasten 源头文献，非实证）
