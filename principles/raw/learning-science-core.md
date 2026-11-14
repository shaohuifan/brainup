# 学习科学核心实证：什么真正促进长期保持与迁移

> 定位：`principles/raw/` 原始资料层。本文件只做**证据整理与校准**，不做产品决策；综合判断见 `principles/wiki/synthesis.md`。
> 调研日期：2026-11-14（`websearch` 不可用；改用 OpenAlex / Crossref / Europe PMC / Semantic Scholar / ERIC 做结构化检索，webfetch 直取一手摘要与开放全文）
> 覆盖：Dunlosky 2013 十技巧评级、检索练习、间隔、交错、生成/自我解释、合意困难、元认知错觉、认知负荷与多媒体、近/远迁移，以及 2023–2026 最新元分析与边界条件。
> 面向问题：brainup 下一阶段该不该做复习卡、测验、主动回忆、元认知提示；哪些"学习功能"有证据、哪些只是直觉。

## 0. 怎么读这份文件（证据分级）

沿用 `memory-pkm-evidence.md` 的分级，便于 synthesis 交叉引用：

| 级别 | 含义 | 本文件中的例子 |
|---|---|---|
| **A** | 大样本元分析 / 预注册 RCT / 多实验室重复 | Dunlosky 2013；Adesope 2017；Yang 2021；Ruitenburg 2026 |
| **B** | 同行评审单点实验、样本中等、课堂准实验 | Roediger & Karpicke 2006；Rohrer 2020 RCT；Deslauriers 2019 |
| **C** | 小样本、自评/相关性、单一材料 | Karpicke et al. 2009 调查；Hartwig & Dunlosky 2012 |
| **D** | 理论框架/专家综述，用于解释机制而非估计效应 | Bjork & Bjork 2011；Sweller 2019；Mayer 2024 |

**三条总论**（后面每条证据都是它的注脚）：

1. **实验室效应大，真实课堂打折。** 练习测试从实验室的 g≈0.50–0.61 降到真实课堂的 g≈0.37；间隔在严格课堂元分析中只有 g≈0.20（另一项应用元分析 d≈0.54，差异来自纳入标准与实施质量）；交错的 g≈0.40 相对稳定。产品若按实验室效应量做预期，会高估收益。
2. **有效性不取决于"用了哪种形式"，而取决于认知过程是否被真正触发。** 2026 年课堂元分析的结论是：只有练习中真正发生了提取、间隔、辨别/选择过程，效应才可靠出现（Ruitenburg et al., 2026）。
3. **学习者的主观感受是坏指标。** 流畅、熟悉、当堂表现好，常常与长期保持负相关；学习者系统性高估重读、划重点、集中练习（Bjork, Dunlosky & Kornell, 2013）。产品必须用**延迟、客观、可校准**的测量替代"感觉学会了"。

---

## 1. 一页结论：十种技巧的证据排序

| # | 方法 | 证据级别 | 典型效应量 | 最关键边界 | 对 brainup 的方向 |
|---|---|---|---|---|---|
| 1 | **练习测试 / 检索练习** | A | 实验室 g≈0.50–0.61；课堂 g≈0.37 | 必须有反馈；延迟测验才显出优势；复杂材料/低先验知识要搭支架 | **P0：默认学习动作** |
| 2 | **分散练习 / 间隔** | A | 课堂 g≈0.20；应用研究报告 d≈0.54 | 最优间隔随目标保持期变化；初次编码不足时无效 | **P0：排程，而非内容** |
| 3 | **交错练习** | A– | g≈0.40–0.42 | 只对"易混淆类别/需选择策略"的任务稳定；说明文、词汇表可能无效甚至反转 | **P1：按任务类型启用** |
| 4 | **自我解释** | B+ | g≈0.55（69 个效应量） | 需要提示与先验知识；泛泛"解释一下"效果弱 | **P1：结构化提示** |
| 5 | **生成效应** | B+ | d≈0.40（86 项研究） | 生成失败且无反馈会固化错误；新手高负荷时反噬 | **P1：生成 + 校验** |
| 6 | **精细化提问（为什么）** | B | 中等；证据多为孤立事实 | 低先验知识者难以生成解释 | **P2：可做，别夸大** |
| 7 | **预测试/前测问题** | B+ | 特定材料 g≈0.54；未测材料 g≈0.04 | 只对"被问到的内容"有效，不提升整体理解 | **P1：读前定向** |
| 8 | **总结/划重点/重读** | C–D | 低且不稳定 | 总结需长期训练；划重点对推断题可能有害 | **不作为核心** |
| 9 | **元认知提示/校准** | B | 无统一 d；改变策略选择与坚持 | 提示本身不教知识；需与客观测验绑定 | **P0：差异化能力** |
| 10 | **认知负荷/多媒体设计** | A– | 原则级小到中等效应 | Expertise reversal：对专家要撤支架 | **P1：渲染与分块** |

> 读法：效应量是"平均而言"；教育研究的异质性通常很大（交错元分析 I²=77%）。真正可执行的是**边界条件**，不是排名。

---

## 2. Dunlosky et al. 2013：十种技巧的效用评级

**出处**：Dunlosky, J., Rawson, K. A., Marsh, E. J., Nathan, M. J., & Willingham, D. T. (2013). *Improving Students' Learning With Effective Learning Techniques: Promising Directions From Cognitive and Educational Psychology.* Psychological Science in the Public Interest, 14(1), 4–58.
https://doi.org/10.1177/1529100612453266
（作者面向教师的改写版：https://www.aft.org/ae/fall2013/dunlosky）

### 2.1 评级结果

Dunlosky 等评的是**"效用"（utility）**，不是单一效应量。判定标准包括：证据是否来自有对照的实验、能否推广到不同材料/学习者/测验形式/教育情境、是否真正提升学业成就。因此"高效用"意味着"证据广、可迁移、值得教"，不等于"效应量最大"。

| 评级 | 技巧 | 核心结论 |
|---|---|---|
| **高效用** | **Practice testing（练习测试）** | 自测/模拟测验优于重读；对记忆与理解都有效；适用范围广；需反馈、需持续到正确提取 |
| **高效用** | **Distributed practice（分散练习）** | 同样总时长下，分散优于集中；对长期保持优势"压倒性"；学生却普遍低估 |
| **中等效用** | Interleaved practice（交错练习） | 问题解决/类别辨别有强证据；但研究量较少，且非所有学科都有效 |
| **中等效用** | Elaborative interrogation（精细化提问） | 问"为什么这是真的"促进理解；证据多集中在孤立事实，课堂证据少 |
| **中等效用** | Self-explanation（自我解释） | 解释"新信息如何与已知关联"或"为什么这样做"；对迁移有帮助；需提示与训练 |
| **低效用** | Summarization（总结） | 需要长期、明确训练才有效；对低龄/低写作能力者负担大 |
| **低效用** | Highlighting/underlining（划重点） | 与单纯阅读相比常无优势；对需要跨句推断的理解题可能有害（注意力被单个概念吸走） |
| **低效用** | Keyword mnemonic（关键词记忆术） | 对词汇表短期有效，收益不持久、适用范围窄 |
| **低效用** | Imagery for text（文本心像） | 对具体、可成像材料短期有效；抽象/复杂材料难用，收益短暂 |
| **低效用** | Rereading（重读） | 对回忆偶有短期帮助；对理解与长期保持不稳定；却是学生最常用策略（调查中 84%） |

### 2.2 关键数字与后续量化

- 2021 年一项对 Dunlosky 十技巧的独立元分析（Donoghue & Hattie, 2021, *Frontiers in Education*）纳入 **242 项研究、1,619 个效应量、169,179 名参与者**，总体平均效应 **0.56**；**分散练习与练习测试最强，划重点与总结最弱**。作者同时警告：多数研究测量的是**表层/事实性结果**，推广到深层关系性理解要谨慎；反馈、近/远迁移、学习者能力是重要调节变量。
https://doi.org/10.3389/feduc.2021.581216
- Dunlosky 原文对"高效用"的界定不是"效应量 > 0.8"，而是"在不同年龄、材料、测验、课堂情境中都能提升成就"。这解释了为什么练习测试（g≈0.5）比某些单点效应更大的技巧评级更高。

### 2.3 边界与误读

- **"低效用"≠"完全没用"**：重读能带来熟悉感，划重点能标记重点，总结本身是重要技能；问题是它们**不足以支撑长期保持与迁移**，不能作为核心学习机制。
- **"高效用"≠"任何情况下都有效"**：练习测试需要反馈与足够的初次编码；分散需要目标保持期信息；交错需要可辨别的类别结构。
- **评级基于 2013 年前的证据**；2023–2026 的新元分析基本支持"检索/间隔/交错优先"，但把效应量下调到真实课堂水平（见第 3–5 节）。

---

## 3. 检索练习 / 测试效应（retrieval practice / testing effect）

### 3.1 经典实验：测试优于重读，但只在延迟后显现

**Roediger & Karpicke (2006)**，*Test-Enhanced Learning: Taking Memory Tests Improves Long-Term Retention*，Psychological Science 17(3):249–255。
https://doi.org/10.1111/j.1467-9280.2006.01693.x

- 设计：大学生阅读说明文；比较"重复学习（SSSS）"与"学习后测试（STTT 等）"；即时测验（5 分钟）vs 延迟测验（2 天/1 周）。
- 核心数字（实验 2）：**一周后，STTT 组回忆 61%，SSSS 组 40%**；但在**5 分钟后的即时测验**上，方向相反：SSSS 83% > SSST 78% > STTT 71%。实验 1 的 1 周延迟同样显示测试优势（56% vs 42%，d=0.83）。
- 边界：材料为说明文；自由回忆；**无反馈**；延迟是关键。**"当堂感觉更好"与"一周后记得更多"方向相反**——这是元认知错觉的实验室原型。

**Karpicke & Roediger (2008)**，*The Critical Importance of Retrieval for Learning*，Science 319(5865):966–968。
https://doi.org/10.1126/science.1152408

- 设计：斯瓦希里语—英语词对；一旦首次正确，分别进入"继续学习""继续测试""两者都停"等条件。
- 核心结果：**学会之后再重复学习，对一周后回忆几乎无效；重复测试则产生大幅提升**；且**学习者对自己未来表现的预测与实际成绩不相关**。
- 边界：词汇配对，材料简单；但机制（提取本身改变记忆）可推广。

### 3.2 元分析：效应量随情境下降

| 元分析 | 纳入范围 | 核心效应量 | 关键调节 |
|---|---|---|---|
| **Rowland (2014)**, *Psychological Bulletin* | 实验室研究 | **g = 0.50** | 保持间隔 >1 天时 **g = 0.69**，<1 天时 **g = 0.41**；反馈、提取成功度调节 |
| **Adesope, Trevisan & Sundararajan (2017)**, *Review of Educational Research* | 200 余个实验 | **g ≈ 0.61**（常被引用的总体估计） | 有反馈显著大于无反馈；测验形式、材料、年龄调节 |
| **Yang, Luo, Vadillo, Yu & Shanks (2021)**, *Psychological Bulletin* | **222 项研究、48,478 名学生** | **g = 0.499** | 控制组策略、练习/考试形式匹配、反馈、重复次数、实施时点 |
| **Agarwal, Nunes & Blunt (2021)**, *Educational Psychology Review* | **50 个课堂实验、n=5,374** | **57% 的效应量为中或大** | 教育阶段、学科、测验延迟、形式都较稳健；但**仅 6% 研究来自非 WEIRD 国家** |
| **Pan & Rickard (2018)**, *Psychological Bulletin* | **192 个迁移效应、122 个实验、N=10,382** | **d = 0.40**（相对重学对照） | 对应用/推断题、医学诊断题最强；对"重排刺激—反应"、未测材料、样例题最弱 |
| **Ruitenburg et al. (2026)**, *Educational Psychology Review* | **53 项课堂研究、233 个效应量、7,303 人（2006–2024）** | **g = 0.37** | 知识类型、后测形式、练习—考试形式匹配、学习结果类型 |

**怎么读这组数字**：从实验室（0.50–0.61）→ 课堂元分析（0.499）→ 严格限定"真实课堂、初等/中等教育"（0.37），效应量逐级下降。这不是"测试效应不存在"，而是**实施质量与情境决定收益**。2026 年作者的原话：三种策略只有在练习中真正触发了其核心认知过程时才可靠有效。

### 3.3 机制（决定产品怎么做）

1. **提取努力（retrieval effort）**：越费力的成功提取，长期收益越大；但"费力到失败"需要反馈兜底。
2. **测试—延迟交互**：测试的优势随保持间隔延长而放大（Rowland, 2014）。所以**不要在学完当天就下结论**。
3. **前向测试效应（forward testing effect）**：测验不仅巩固已学，还能促进**后续**新内容的学习（Don et al., 2024 的机制分析之一）。
4. **反馈是放大器**：只给对错不够，需给正确答案/解释；无反馈时错误提取可能被固化。
5. **形式不必花哨**：自由回忆、简答、选择、填空都可产生效应；但**需要推断/应用**的题型更利于迁移（Pan & Rickard, 2018）。

### 3.4 边界条件（2023–2026 的新证据）

- **"嵌入学习流"优于"最后一次性大测"**：Don, Boustani, Yang & Shanks (2024), *JEP: LMC*，5 个实验 + 19 项研究的元分析，**interim tests（学一点、测一点）优于 end tests（全学完再大测），g = 0.25**；若中间测试太容易，效应消失；前向测试效应是主要机制。
https://doi.org/10.1037/xlm0001382
- **在线众包样本可能测不出**：2026 年两项 Prolific 实验（延迟后测、反馈、事实/应用题都具备）**未发现测试效应**。作者认为不是理论失效，而是"需要持续认知投入的学习现象"在众包环境难复现。
https://doi.org/10.3389/fpsyg.2026.1727423
- **真实小学课堂：检索有效，间隔操纵无效**：2025 年五年级历史文本研究，检索+反馈优于重读；但拉长首次阅读与复习的间隔**没有显著效果**——提示"间隔"在复杂课堂材料上不是自动生效的。
https://doi.org/10.3389/fpsyg.2025.1632206
- **数学应用题可能无效**：2023 年研究发现检索练习**不一定**改善数学应用题解决；材料复杂度与迁移需求会吃掉效应。
https://pmc.ncbi.nlm.nih.gov/articles/PMC9987560/
- **复杂材料不等于无效，但需要支架**：高阶检索不必以低阶事实为前提；事实检索与高阶检索宜从学习早期就结合（Agarwal, 2019 综述，https://doi.org/10.3389/feduc.2019.00005 ；Fraundorf et al., 2023，https://doi.org/10.1186/s41235-023-00508-8 ）。
- **非 WEIRD 样本严重不足**：Agarwal 2021 仅 6% 研究来自非 WEIRD 国家；跨文化推广需谨慎。

### 3.5 对产品的直接含义

- 每次摄入（论文/书/播客）后，**默认生成 3–7 个可检索的问题**，而不是只生成摘要。
- 问题要**混合事实、关系、应用/推断**；只考事实会高估"学会了"。
- **测验嵌入阅读过程**（读完一节就测），不要做成"期末复习模式"。
- **低风险、即时反馈、允许重试**；错误答案要显示正确答案与解释。
- 记录**延迟后测**（如 3 天/7 天）而非当堂正确率，作为真实学习指标。

---

## 4. 间隔重复 / 分散练习（distributed practice / spacing）

### 4.1 经典证据：间隔与保持期共同决定最优排程

**Cepeda, Pashler, Vul, Wixted & Rohrer (2006)**，*Distributed Practice in Verbal Recall Tasks: A Review and Quantitative Synthesis*，Psychological Bulletin 132(3):354–380。
https://doi.org/10.1037/0033-2909.132.3.354

- 规模：**184 篇文章、317 个实验、839 个分散练习评估**。
- 核心结论：**间隔（interstudy interval, ISI）与保持间隔（retention interval, RI）共同作用**；使最终保持最大化的 ISI 随 RI 增加而增加。不存在"一个万能最优间隔"。

**Cepeda, Vul, Rohrer, Wixted & Pashler (2008)**，*Spacing Effects in Learning: A Temporal Ridgeline of Optimal Retention*，Psychological Science 19(11):1095–1102。
https://doi.org/10.1111/j.1467-9280.2008.02209.x

- 规模：**1,350+ 名参与者**；学习事实后间隔最多 3.5 个月复习；最终测验延迟最多 1 年。
- 核心数字：在任一测验延迟下，间隔先增后减（倒 U）。**最优间隔占保持期的比例：1 周延迟时约 20–40%（约 1.4–2.8 天）；1 年延迟时约 5–10%（约 18–36 天）**。
- 边界：实验室事实材料；单一复习；个体差异存在。实践中的常用近似是"**间隔 ≈ 目标保持期的 10–20%**"（注意：Cepeda 2008 在 1 周保持期下给的是 20–40%，随保持期延长降到 5–10%；10–20% 是更保守的经验折中）。

**Cepeda et al. (2009)**，*Optimizing Distributed Practice: Theoretical Analysis and Practical Implications*，Experimental Psychology 56(4):236–246。
https://doi.org/10.1027/1618-3169.56.4.236

- 两项三阶段实验，材料含外语词汇、事实、视觉物体名称；**最优间隔使最终回忆提高最多 150%**；间隔效应是非单调的（先升后降）。

### 4.2 真实课堂与应用证据

- **课堂元分析（2025）**：22 份报告、31 个效应量、N>3,000；分散优于集中 **d = 0.54（95% CI 0.31–0.77）**；保持间隔更长、教育阶段更高、重复暴露更少时效应更大。作者同时指出，这低于早期综述的 d≈0.85，说明应用情境会缩水。
https://doi.org/10.3390/bs15060771
- **2026 年课堂元分析**：间隔效应 **g = 0.20**，受比较条件、保持间隔、ISI/RI 比例、后测形式调节。与检索（0.37）、交错（0.40）相比，**间隔在真实课堂的平均效应最小**——最可能的原因是实施质量参差（间隔太短、初次编码不足、没有反馈）。
https://doi.org/10.1007/s10648-026-10225-5
- **大规模真实世界证据（2024）**：美国家庭医学委员会 26,258 名医生/住院医随机进入对照或 5 种间隔重复条件；间隔重复组在 **第 6 季度学习测验 58.03% vs 43.20%（d = 0.62）**，在 **第 10 季度迁移测验 58.33% vs 52.39%（d = 0.26）**。两个数字的落差非常重要：**保持收益大，迁移收益小**。
https://doi.org/10.1097/acm.0000000000005856
- **2025 年小学课堂**：检索有效，但"把首次阅读与复习间隔拉长"没有显著效果（见 3.4）。说明间隔不是"设一个更长的数字"就自动生效，需要与初次编码质量、复习时的提取结合。

### 4.3 边界与实施规则

- **没有万能间隔**：先问"希望多久后还能用"（考试？三个月？一年？），再按 10–20% 规则排。
- **间隔必须配合提取**：单纯"再读一遍"的间隔收益远小于"间隔后先回忆再反馈"。
- **初次编码不足时，间隔无效**：如果学习者第一次就没理解，拉长间隔只会加速遗忘；应先做一次成功编码（讲解/样例/反馈）。
- **复杂材料的效果不稳定**：说明文、课堂材料上的间隔效应小于词汇/事实。
- **不要用"连续打卡天数"替代排程质量**：打卡衡量行为，不衡量保持。

> 与 `memory-pkm-evidence.md` 的分工：那边讲 FSRS 如何**预测**遗忘并排程；这里讲**为什么**间隔有效、以及间隔无法替代什么。结论：FSRS 是排程引擎，不是教学法。

---

## 5. 交错练习（interleaved practice）

### 5.1 经典证据：混合题型促进"选择策略"的能力

**Rohrer & Taylor (2007)**，*The Shuffling of Mathematics Problems Improves Learning*，Instructional Science 35:481–498。
https://doi.org/10.1007/s11251-007-9015-8

- 设计：大学生学习四类几何体体积计算；集中练习（同类题连续）vs 交错练习（不同类题混合）；两次练习相隔一周，一周后考试。
- 核心结果：**练习阶段集中组表现更好；一周后考试交错组大幅更好（Dunlosky 面向教师的总结称"约三倍"）**。机制：交错强迫学习者先**辨别题目属于哪一类**，再选择解法；集中练习让学习者无需辨别，直接套用上一步。
- 边界：数学问题解决；类别可辨别；有明确解法。

**Rohrer, Dedrick & Stershic (2020)**，*A Randomized Controlled Trial of Interleaved Mathematics Practice*，Journal of Educational Psychology 112(1):40–52。
https://doi.org/10.1037/edu0000367

- 预注册整群 RCT：**54 个七年级班级**，持续 4 个月，之后一个月进行**突击测验**；交错组显著优于集中组。这是"课堂规模 + 延迟测验"的最强证据之一。

**2021 年物理课堂**（Samani & Pan, 2021）：8 周、每周三次作业，交错 vs 按主题集中；在两次**未预告的挑战性测验**上，交错组回忆更多相关信息、更常给出正确解法。
https://doi.org/10.1038/s41539-021-00110-x

### 5.2 元分析：平均中等，但异质性极高

**Brunmair & Richter (2019)**，*Similarity Matters: A Meta-Analysis of Interleaved Learning and Its Moderators*，Psychological Bulletin。
https://doi.org/10.1037/bul0000209

- 总体 **g = 0.42**；但 **I² = 77%**，说明大部分变异来自研究间差异，而非抽样误差。
- 调节变量：**类别之间越相似、类别内部越不相似、材料越复杂，交错收益越大**；对说明文和词汇表要谨慎。
- 2024 年一篇综述用一句话总结：**"在许多情况下交错效应消失甚至反转"**（Yan, Sana & Carvalho, 2024, *Policy Insights from the Behavioral and Brain Sciences*）。
https://doi.org/10.1177/23727322231218906

**2026 年课堂元分析**：交错 **g = 0.40**，受**反馈是否提供、反馈时点**调节；是三种策略中在真实课堂里最稳定的。
https://doi.org/10.1007/s10648-026-10225-5

### 5.3 什么时候有效、什么时候无效

| 有效 | 无效/反转 |
|---|---|
| 易混淆的类别/概念（画家风格、鸟类、心电图、题型） | 说明文、词汇表（类别之间不需要辨别） |
| 需要"先判断题型再选策略"的问题解决 | 规则容易 verbalize、集中练习更能发现规则的类别学习 |
| 类别之间相似、类别内部差异大 | 类别之间一眼可分、类别内部高度相似 |
| 有反馈、有足够练习量 | 复杂多成分技能（网球/高尔夫不同击球）初期 |
| 延迟、突击式测验 | 即时测验（交错在练习阶段看起来更差） |

**2025 年的新边界**：交错还是集中更有效，取决于学习者**采用的学习策略**——想"记忆相似性"时交错更好，想"找规则"时集中更好（*Journal of Intelligence* / PMC12108632）。这意味着产品不能无条件"打乱"，而要根据任务类型与提示语设计。

### 5.4 对产品的含义

- 交错应作用于**"题型/概念辨别"**，不是"把无关主题混在一起"。
- 复习队列可以按**易混淆簇**混合（例如同一学科内相近概念），而不是随机打乱全部笔记。
- 对说明文/播客类内容，优先做**检索 + 自我解释**，不要强行交错。
- 交错练习阶段要允许"当下更差"，并用延迟测验展示收益，否则用户会误以为产品变差了。

---

## 6. 生成效应、自我解释、精细化提问

### 6.1 生成效应（generation effect）

**Bertsch, Pesta, Wiscott & McDaniel (2007)**，*The Generation Effect: A Meta-Analytic Review*，Memory & Cognition 35:201–210。
https://doi.org/10.3758/BF03193441

- 规模：**86 项研究、445 个效应量**。
- 核心效应：**d = 0.40**（生成条件优于阅读条件，约半个标准差）。
- 边界：生成约束越强、生成内容与目标越一致，效应越大；生成失败且无反馈时可能学到错误；对高负荷/新手可能反噬（认知负荷）。

### 6.2 自我解释（self-explanation）

**Bisra, Liu, Nesbit, Salimi & Winne (2018)**，*Inducing Self-Explanation: A Meta-Analysis*，Educational Psychology Review 30:703–725。
https://doi.org/10.1007/s10648-018-9434-x

- 规模：**69 个效应量、64 份报告**。
- 核心效应：**g = 0.55**（提示学习者自我解释 vs 不提示）。
- 调节：提示类型（"为什么" vs "怎么做"）、任务（解题/样例/文本）、学科、教育阶段、诱导方式、时长。**结构化、原则性提示**通常优于泛泛的"解释一下"。
- 边界：需要一定先验知识；低龄/低知识者需要教练；解释质量比"是否解释"更重要。

Dunlosky 的教师版给了一个直观例子：逻辑题练习中，**自我解释组最终测验约 90%，对照组不到 30%**（单实验，效应巨大，不宜当平均值）。

### 6.3 精细化提问（elaborative interrogation）

- 核心动作：对事实问"**为什么这是真的？**"，并尝试生成解释。
- Dunlosky 评级为**中等效用**：对事实/简单概念有效，但课堂证据少，且低先验知识者难以生成合理解释。
- 与自我解释的区别：精细化提问针对"事实为何成立"；自我解释针对"新信息如何与已知关联/为什么这样做"。

### 6.4 生成学习：八种策略与三种模式

**Fiorella & Mayer (2016)**，*Eight Ways to Promote Generative Learning*，Educational Psychology Review 28:717–741。
https://doi.org/10.1007/s10648-015-9348-9

八种策略：**总结、绘制概念图、画图、想象、自测、自我解释、教别人、动作表演（enacting）**。共同机制：让学习者主动选择、组织、整合信息，而不是被动接收。

**Fiorella (2023)**，*Making Sense of Generative Learning*，Educational Psychology Review。
https://doi.org/10.1007/s10648-023-09769-7

- 提出三种"意义建构模式"：**解释（explaining）、可视化（visualizing）、表演（enacting）**；三者功能互补：可视化/表演帮助组织与模拟，解释帮助概括与迁移。
- 边界：生成活动需要**指导、支架、反馈**；对新手或高负荷材料，纯生成可能失败。

**Lawson & Mayer (2024) 在线多媒体实验**：在动画学习中，**写总结有效，画图（未经训练）无效**；说明"生成"不是万能钥匙，活动必须与材料、学习者能力匹配。
https://doi.org/10.3389/fpsyg.2024.1452385

### 6.5 预测试/前测问题（pretesting / prequestions）

**St. Hilaire, Chan & Ahn (2023)**，*Guessing as a Learning Intervention: A Meta-Analytic Review of the Prequestion Effect*，Psychonomic Bulletin & Review。
https://doi.org/10.3758/s13423-023-02353-8

- **特定效应 g = 0.54（k = 97）**：被预问到的材料记得更好。
- **一般效应 g = 0.04（k = 91）**：对未被问到的材料几乎没有帮助。
- 机制：注意定向 + 生成尝试；需要后续反馈/学习。
- 边界：只做"读前问题"而不覆盖全部内容，会造成"选择性学习"，漏掉未问部分。

### 6.6 对产品的含义

- 把"生成"做成**有结构的动作**：不是"写个总结"，而是"用你自己的话解释这段论证为什么成立""如果条件反过来会怎样""教给一个外行"。
- **生成之后必须校验**：LLM 可以扮演"追问者/挑错者"，但不应直接给答案；否则生成变成复制。
- 预测试适合做**读前定向**（3 个问题），但不能替代全文覆盖。
- 对播客/视频，优先"暂停—回忆—解释"，而不是"自动摘要"。

---

## 7. 合意困难（desirable difficulties）

**Bjork & Bjork (2011)**，*Making Things Hard on Yourself, But in a Good Way: Creating Desirable Difficulties to Enhance Learning*，in *Psychology and the Real World*。
（UCLA Bjork Lab  PDF：https://bjorklab.psych.ucla.edu/wp-content/uploads/sites/13/2016/04/EBjork_RBjork_2011.pdf）

### 7.1 核心命题

- **学习（learning）≠ 当前表现（performance）**：训练中表现提升，可能并不产生长期保持；训练中表现变慢/变难，可能反而促进保持与迁移。
- 合意困难的例子：**变化练习条件、交错、间隔、用测试代替重复呈现、生成而非阅读**。
- **"合意"是关键词**：并非所有困难都有益。若学习者**缺乏背景知识或技能**，同样的困难会变成"不合意困难"，导致挫败与错误学习。
- 学习者会被**流畅性（fluency）**误导：重读带来的熟悉感被误读为理解；当前提取容易被误读为已掌握。

### 7.2 理论张力：合意困难 vs 认知负荷

**Pyke, Lunau & Javadi (2024)**，*Does Difficulty Moderate Learning? A Comparative Analysis of the Desirable Difficulties Framework and Cognitive Load Theory*，Quarterly Journal of Experimental Psychology。
https://doi.org/10.1177/17470218241308143

- 提出整合模型：**难度应随材料复杂度与学习者专长调整**。
- **低元素互动性（low element interactivity）任务**：增加难度（如间隔、提取）有益。
- **高元素互动性（high element interactivity）任务/新手**：增加难度会压垮工作记忆，应先降低外在负荷、给样例与支架。
- 这与"expertise reversal effect"一致：对专家有效的"少指导/高挑战"，对新手可能有害。

**Binks (2026)**，*Why Desirable Difficulties 'Work': A Review of the Evidence ... and Some Caveats*，Journal of Evaluation in Clinical Practice。
https://doi.org/10.1111/jep.70349

- 证据最扎实的合意困难：**形成性测试、交错/混合练习、分散练习、生产性失败（productive failure）**。
- 提醒：机制包含认知、元认知、动机、情感多层面；不能把"难"本身当成有效。

### 7.3 对产品的含义

- **不要优化"单次学习的顺滑感"**：太顺的阅读/总结/问答，可能只是流畅性错觉。
- 对新手：先给**样例、分解、支架**，再逐步撤除（guided fading）；对高阶用户：增加提取、交错、开放任务。
- 在 UI 上**预告"难是正常的"**：研究显示学习者会因努力感而回避合意困难（S2D2 框架，de Bruin et al., 2023）。
https://doi.org/10.1007/s10648-023-09766-w
- 用**延迟测验**而非当场满意度，作为产品效果的证据。

---

## 8. 元认知与流畅性错觉（metacognition / illusions of competence）

### 8.1 现象：学习者系统性地误判自己

**Bjork, Dunlosky & Kornell (2013)**，*Self-Regulated Learning: Beliefs, Techniques, and Illusions*，Annual Review of Psychology 64:417–444。
https://doi.org/10.1146/annurev-psych-113011-143823

- 学习者对"如何学习"持有错误心智模型；对"当前学得怎样"的判断被**当前表现**与**主观流畅感**污染。
- 结果：高估重读/集中练习，低估检索/间隔；过早停止练习；选择让自己"感觉会了"的策略。

**Kornell & Bjork (2008)**，*Learning Concepts and Categories: Is Spacing the "Enemy of Induction"?*，Psychological Science 19(6):585–592。
https://doi.org/10.1111/j.1467-9280.2008.02127.x

- 设计：学习不同画家的画作；集中 vs 交错；之后做类别归纳测验。
- 结果：**交错/间隔组的归纳成绩更好；但参与者认为集中练习更有效——即使在他们已经经历测验、看到自己成绩之后**。
- 意义：**偏好与效果脱钩**，且这种脱钩不易被一次反馈纠正。

**Karpicke, Butler & Roediger (2009)**，*Metacognitive Strategies in Student Learning: Do Students Practise Retrieval When They Study on Their Own?*，Memory 17(4):471–479。
https://doi.org/10.1080/09658210802647009

- 调查 **177 名大学生**：多数以**重读笔记/教材**为主，**很少自测**；学生报告使用测试多是为了"检查哪里不会"，而非"通过提取来学习"。
- Dunlosky 教师版引用：**84% 的学生通过重读来学习**。

**Deslauriers et al. (2019)**，*Measuring Actual Learning Versus Feeling of Learning in Response to Being Actively Engaged in the Classroom*，PNAS 116(39):19251–19257。
https://doi.org/10.1073/pnas.1821936116

- 大型物理课随机分入主动学习 vs 被动讲授；内容、讲义相同。
- 结果：**主动学习组实际学得更多，但主观"感觉学到"更少**；学生因此可能偏好低效的讲授。
- 意义：**满意度/感知学习不能作为教学或产品效果的代理指标**。

**Hartwig & Dunlosky (2012)**，*Study Strategies of College Students: Are Self-Testing and Scheduling Related to Achievement?*，Psychonomic Bulletin & Review。
https://doi.org/10.3758/s13423-011-0181-y

- 324 名本科生：自测与重读都与 GPA 正相关（自评、相关性，不能作因果）；**集中学习与更少的学习策略使用相关**；低成就者更可能熬夜学习。
- 启示：自评数据会混淆"好学生什么都做得多"，产品不能只靠问卷证明效果。

**2025 年中学生调查**：**72% 的学生偏好"集中练习"而非交错**，尽管交错被证明更有效（Hartwig & Rohrer, 2025, *Behavioral Sciences*）。
https://doi.org/10.3390/bs15081047

### 8.2 为什么会误判（机制清单）

1. **流畅性/熟悉感**：重读让材料"看起来眼熟"，被误认为掌握。
2. **提取流畅性**：当下容易想起，被误认为长期记得。
3. **稳定性偏差（stability bias）**：假设"现在会 = 以后会"，低估遗忘。
4. **即时表现偏差**：集中练习/交错前的集中练习让当堂表现更好。
5. **缺乏延迟反馈**：没有机会看到"一周后忘了"。
6. **朴素理论**："学习应该感觉越来越轻松"；困难被误读为无效。
7. **选择性注意**：划重点/总结让人感觉"处理过了"，但可能没建立关系。

### 8.3 对产品的含义（这是 brainup 的差异化机会）

- **不要问"你觉得学会了吗"作为主指标**；用**延迟测验 + 置信度校准**。
- 每次测验让用户给出**信心评分**，之后对比"信心—正确率"，生成校准曲线。
- 用**延迟判断（delayed JOL）**："不看答案，你 3 天后还能回忆吗？"比即时 JOL 更准。
- 明确告诉用户：**"现在感觉难，是设计的一部分"**；用数据展示"难但记得久"。
- 不要用**连续打卡、XP、阅读时长**暗示能力；这些是行为指标，不是学习指标。
- 对 AI 回答做**门槛设计**：先让用户尝试回忆/解释，再解锁答案，避免"看懂=学会"的错觉（详见 `ai-learning-2025-2026.md`）。

---

## 9. 认知负荷理论与多媒体学习

### 9.1 认知负荷理论（CLT）

**Sweller (1988)**，*Cognitive Load During Problem Solving: Effects on Learning*，Cognitive Science 12(2):257–285。
https://doi.org/10.1207/s15516709cog1202_4

**Sweller, van Merriënboer & Paas (2019)**，*Cognitive Architecture and Instructional Design: 20 Years Later*，Educational Psychology Review 31:261–292。
https://doi.org/10.1007/s10648-019-09465-5

核心假设：
- 人类认知架构：**工作记忆容量与时长有限**；**长时记忆容量无限**；学习是图式（schema）的获取与自动化。
- **元素互动性（element interactivity）**决定内在负荷：互相依赖的元素越多，理解越难。
- 负荷三分：**内在（材料本身）/外在（教学设计不当）/相关（用于图式建构）**。教学应降低外在负荷、优化内在负荷、把资源留给相关负荷。
- 经典效应：**样例效应（worked example）、分散注意效应（split-attention）、冗余效应（redundancy）、专长逆转效应（expertise reversal）、指导渐隐（guidance fading）**。
- 工作记忆容量：Cowan (2001) 综合证据认为约 **3–5 个 chunk**（常被引用为"4±1"），而非 Miller 的 7±2。
https://doi.org/10.1017/S0140525X01003922

### 9.2 多媒体学习原则（Mayer）

**Mayer (2024)**，*The Past, Present, and Future of the Cognitive Theory of Multimedia Learning*，Educational Psychology Review 36(1)。
https://doi.org/10.1007/s10648-023-09842-1

- 三大核心：**双通道（言语/视觉）、容量有限、主动加工（选择—组织—整合）**。
- 该综述总结 **15 条证据支持的多媒体设计原则**，包括：coherence（去无关信息）、signaling（突出结构）、redundancy（避免重复呈现）、spatial/temporal contiguity（图文邻近/同步）、segmenting（分段）、pre-training（先教关键概念）、modality（图+旁白优于图+文字）、multimedia（图文结合优于纯文字）、personalization（对话式）、voice（人声）、image（教师形象谨慎使用）、embodiment（手势/动作）、generative activity（生成活动）、testing（测验）等。
- 效应量随原则、材料、学习者而异，多为**小到中等**；不是"加了图就一定更好"。

**边界**：
- **专长逆转**：对专家，强指导/冗余信息反而有害；支架要随能力撤除。
- **合意困难 vs CLT**：低互动性任务可加难度；高互动性/新手要先降负荷（见 7.2）。
- **多媒体不是装饰**： seductive details（有趣但无关的细节）会挤占工作记忆，降低学习。

### 9.3 对产品的含义

- wiki 页面渲染遵循：**一段一义、标题信号、图文邻近、去装饰、分段呈现、先给关键概念（pre-training）**。
- 长文/长视频拆成**可测验的段落**，每段后插入检索或解释任务（segmenting + generative activity）。
- 对新手给**样例/模板**，对高阶用户给**开放问题/空白页**（guidance fading）。
- 不要用"信息密度高"当作专业感；对学习产品，**降低外在负荷**才是专业。

---

## 10. 迁移：近迁移 vs 远迁移

### 10.1 定义

- **近迁移（near transfer）**：在相似情境、相似任务、相似知识域中应用所学。
- **远迁移（far transfer）**：跨情境、跨领域、跨任务类型的应用（如"学拉丁语提升逻辑思维""玩脑力游戏提升学业"）。
- 分类框架：Barnett & Ceci (2002) 按**情境、知识域、功能、时间**四个维度划分迁移距离。
https://doi.org/10.1037/0033-2909.128.4.612

### 10.2 证据现状：近迁移可训练，远迁移很罕见

| 证据 | 核心数字 | 解释 |
|---|---|---|
| **Pan & Rickard (2018)** 测试效应迁移元分析 | **d = 0.40**（192 个效应、122 个实验、N=10,382） | 检索练习能迁移到**新题型、应用题、推断题、医学诊断**；对"重排刺激—反应"、未测材料、样例题最弱 |
| **Sala et al. (2019)** 二阶元分析（认知训练） | 近迁移存在；**远迁移很小或为零**；控制安慰剂与发表偏倚后总体效应≈0 | 工作记忆训练、脑力游戏、音乐/象棋等对一般认知/学业的远迁移缺乏可靠证据 |
| **Kassai et al. (2019)** 儿童执行功能元分析 | 训练成分对未训练成分 **g = 0.11，不显著** | 成分特异性强，难以自动泛化 |
| **Price et al. (2024)** 医生间隔重复 | 学习 **d = 0.62**；迁移 **d = 0.26** | 同一干预，迁移收益不到保持收益的一半 |
| **2023 年医学教育综述** | 远迁移"**罕见，甚至可以说不可能**" | 但近迁移（同领域新题、新情境）可观测 |

### 10.3 什么能促进迁移（有证据的做法）

1. **用应用/推断题练习**，而不是只考事实（Pan & Rickard, 2018）。
2. **变化练习条件**（不同情境、不同表述、不同例子），这是 Bjork 的"变化练习"。
3. **交错/对比案例**：让学习者辨别"何时用哪个原则"（第 5 节）。
4. **自我解释/讲原理**：解释"为什么"比记住"是什么"更利于迁移（第 6 节）。
5. **反馈 + 延迟**：让学习者在遗忘边缘提取，并纠正错误。
6. **明确教迁移**：提示"这个原则还能用在哪里"，并给跨情境任务。

### 10.4 对产品的含义

- 可以做"**跨来源综合**"：让用户把论文 A 的方法用到博客 B 的案例上——这是**近迁移/中迁移**，有证据基础。
- 不要承诺"学完这个知识库，你的思维能力全面提升"——**远迁移证据不支持**。
- 题目设计要覆盖：**同义改写、新例子、反例、应用题、跨文链接**。
- 评估迁移用**新题/新情境**，不要用原题复测。

---

## 11. 2023–2026 最新证据地图（按时间倒序）

| 年份 | 研究 | 设计/规模 | 关键数字 | 对本文件的修正 |
|---|---|---|---|---|
| **2026** | Ruitenburg, Goos, Lambert, Kirschner et al., *Educ Psychol Rev* | 53 项课堂研究、233 效应、7,303 人 | 测试 **g=.37**；间隔 **g=.20**；交错 **g=.40** | 真实课堂效应量系统性低于实验室；三者都受"过程是否被触发"调节 |
| **2026** | Prolific 复制研究, *Front Psychol* | 2 个在线实验 | 延迟后测**未发现**测试效应 | 众包样本/持续投入是边界；不能把 null 当理论否定 |
| **2026** | Binks, *J Eval Clin Pract* | 综述 | 形成性测试、交错、间隔、生产性失败证据最稳 | 合意困难有边界，不能浪漫化"难" |
| **2025** | 课堂分散练习元分析, *Behavioral Sciences* | 22 报告、31 效应、N>3,000 | **d=.54** | 应用情境的间隔效应中等，低于早期 d≈.85 |
| **2025** | 小学检索+间隔研究, *Front Psychol* | 五年级历史文本 | 检索有效；间隔操纵无效 | 间隔不是"拉长数字"就生效 |
| **2025** | Hartwig & Rohrer, *Behavioral Sciences* | 中学生调查 | **72% 偏好集中练习** | 元认知错觉在青少年中同样强 |
| **2025** | Little & Nepangue, *Behavioral Sciences* | 实验 | 策略×顺序交互 | 交错要按任务与提示设计；想"记忆相似性"时交错更好，想"找规则"时集中更好 |
| **2024** | Don, Boustani, Yang & Shanks, *JEP:LMC* | 5 实验 + 19 研究元分析 | 嵌入式中测优于末端大测 **g=.25** | 测验应嵌入学习流 |
| **2024** | Price et al., *Academic Medicine* | 26,258 名医生随机 | 学习 **d=.62**；迁移 **d=.26** | 迁移收益远小于保持 |
| **2024** | Pyke et al., *QJEP* | 理论综述 | 难度×元素互动性交互 | 合意困难对新手/高负荷材料可能有害 |
| **2024** | Mayer, *Educ Psychol Rev* | 40 年综述 | 15 条多媒体原则 | 设计原则有证据，但效应小到中等 |
| **2024** | Yan, Sana & Carvalho, *Policy Insights* | 综述 | 交错常消失/反转 | 交错有明确边界 |
| **2023** | Fiorella, *Educ Psychol Rev* | 综述 | 解释/可视化/表演三模式 | 生成活动需指导 |
| **2024** | Clinton-Lisell & Litzinger, *Front Psychol* | 21 研究、101 效应、1,712 人 | 学习风格匹配 **g=.31**，但仅 26% 指标显示交叉 | 学习风格匹配证据弱，不值得投入 |
| **2023** | de Bruin et al., *Educ Psychol Rev* | S2D2 框架 | 努力感导致回避 | 需要动机/情感支架 |
| **2023** | Roelle et al., *Educ Psychol Rev* | 综述 | 生成与检索功能互补 | 追随任务可同时做两件事 |
| **2023** | St. Hilaire et al., *Psychon Bull Rev* | 元分析 | 预问特定 **g=.54**；一般 **g=.04** | 前测只对被测内容有效 |

---

## 12. 综合：对 brainup 的启示（只列证据直接支持的）

### 12.1 三个核心判断

**判断 1：检索练习应是"默认学习动作"，而不是一个可选功能。**
- 证据：实验室 g≈0.50–0.61；课堂 g≈0.37；嵌入式中测 g≈0.25；迁移 d≈0.40。
- 设计：每次摄入自动生成问题；读完一节就测；低风险、即时反馈；混合事实/关系/应用题；记录延迟后测。
- 反模式：只生成摘要、只做"阅读进度"、把测验放到最后。

**判断 2：间隔与交错是"排程/编排"问题，必须按任务类型启用。**
- 证据：间隔课堂 g≈0.20–0.54；交错 g≈0.40–0.42，但对说明文/词汇表可能无效或反转。
- 设计：按目标保持期排程（10–20% 规则）；复习队列按"易混淆簇"混合；对说明文优先检索+解释，不强行交错。
- 反模式：随机打乱所有内容、用打卡天数代替排程质量、把 FSRS 当教学法。

**判断 3：元认知校准是 brainup 最有机会的差异化能力。**
- 证据：84% 学生重读；72% 偏好集中练习；主动学习"实际更好但感觉更差"；学习者预测与成绩不相关。
- 设计：信心评分 + 校准曲线；延迟自评；"难是设计的一部分"的叙事；用客观延迟测验而非满意度。
- 反模式：用 XP/连续天数/阅读时长暗示能力；用"你觉得学会了吗"作为效果指标。

### 12.2 功能优先级建议（证据 → 功能）

| 优先级 | 功能 | 证据依据 | 工程量 | 风险/边界 |
|---|---|---|---|---|
| **P0** | 摄入后自动出题（人审 + 质量门） | 检索 g=.37–.61；LLM 出题有初步证据但质量参差 | 中 | 题目质量、事实错误；必须可编辑/可反馈 |
| **P0** | 复习排程（FSRS/间隔） | 间隔 d=.54（应用）；g=.20（课堂） | 中 | 初次编码不足时无效；参数别自研 |
| **P0** | 延迟测验 + 信心校准 | 元认知错觉；测试—延迟交互 | 低–中 | 需要用户回来；可邮件/推送 |
| **P1** | 交错复习队列（按易混淆簇） | 交错 g=.40；边界明确 | 中 | 说明文/词汇不适用；要允许"当下更差" |
| **P1** | 结构化自我解释/教别人 | 自我解释 g=.55；生成 d=.40 | 中 | 需提示模板与反馈；新手要高支架 |
| **P1** | 读前预问（3 题） | 预问特定 g=.54 | 低 | 只覆盖被测内容，不能替代全文 |
| **P1** | 迁移题（新例子/反例/应用） | 迁移 d=.40（近） | 中 | 远迁移不要承诺 |
| **P2** | 多媒体渲染原则（分段/信号/邻近） | Mayer 15 原则 | 低–中 | 效应小到中等；别过度设计 |
| **P2** | 学习风格匹配 | 证据弱（g=.31，仅 26% 交叉） | 高 | **不建议做** |
| **P2** | 连续打卡/排行榜 | 无学习证据；可能强化流畅性错觉 | 低 | 谨慎，最多做"坚持"而非"能力" |

### 12.3 明确不建议做（或不应作为卖点）

1. **"学习风格匹配"个性化**：2024 元分析显示匹配收益小且不稳定，仅 26% 指标支持交叉交互；投入产出比差。
2. **以"总结/划重点/重读"为核心的学习闭环**：Dunlosky 低效用；总结需长期训练；划重点对推断题可能有害。
3. **"脑力训练/远迁移"承诺**：Sala 2019 等证据不支持；最多做近迁移。
4. **用满意度/留存/阅读时长证明学习效果**：Deslauriers 2019 显示感知与真实学习可相反。
5. **无护栏的 AI 直接给答案**：2025 PNAS 实验（Bastani et al., 2025, https://doi.org/10.1073/pnas.2422633122 ）显示，无护栏 GPT-4 访问在撤走后成绩比从未使用更差（-17%）；有护栏的导师版可缓解。AI 设计应"先问后答"。

### 12.4 待验证的产品假设（建议做实验）

| 假设 | 实验设计 | 指标 |
|---|---|---|
| 把测验嵌入阅读流 > 读完后统一测验 | 同一内容两种流程，随机分配 | 7 天延迟测验；完成率 |
| 信心校准提示能改善策略选择 | 测验前给信心评分 + 校准反馈 | 后续复习选择、延迟成绩 |
| 交错队列对"易混淆概念"有效、对说明文无效 | 按内容类型分层随机 | 延迟测验；用户主观难度 |
| "难是正常的"叙事能降低流失 | onboarding 文案 A/B | 7 日留存、复习完成率 |
| AI 先提问再解锁答案 > 直接答案 | 两种导师模式随机 | 延迟迁移测验；依赖度 |

---

## 13. 参考清单（按主题）

### 经典综述与元分析
- Dunlosky, Rawson, Marsh, Nathan & Willingham (2013). *Psychological Science in the Public Interest* 14(1):4–58. https://doi.org/10.1177/1529100612453266
- Donoghue & Hattie (2021). *Frontiers in Education* 6:581216. https://doi.org/10.3389/feduc.2021.581216
- Cepeda, Pashler, Vul, Wixted & Rohrer (2006). *Psychological Bulletin* 132(3):354–380. https://doi.org/10.1037/0033-2909.132.3.354
- Cepeda, Vul, Rohrer, Wixted & Pashler (2008). *Psychological Science* 19(11):1095–1102. https://doi.org/10.1111/j.1467-9280.2008.02209.x
- Cepeda et al. (2009). *Experimental Psychology* 56(4):236–246. https://doi.org/10.1027/1618-3169.56.4.236
- Rowland (2014). *Psychological Bulletin* 140(6):1432–1463. https://doi.org/10.1037/a0037559
- Adesope, Trevisan & Sundararajan (2017). *Review of Educational Research* 87(3):659–701. https://doi.org/10.3102/0034654316689306
- Yang, Luo, Vadillo, Yu & Shanks (2021). *Psychological Bulletin* 147(4):399–435. https://doi.org/10.1037/bul0000309
- Agarwal, Nunes & Blunt (2021). *Educational Psychology Review* 33(4):1409–1453. https://doi.org/10.1007/s10648-021-09595-9
- Pan & Rickard (2018). *Psychological Bulletin* 144(7):710–756. https://doi.org/10.1037/bul0000151
- Brunmair & Richter (2019). *Psychological Bulletin* 145(11):1029–1052. https://doi.org/10.1037/bul0000209
- Bisra, Liu, Nesbit, Salimi & Winne (2018). *Educational Psychology Review* 30:703–725. https://doi.org/10.1007/s10648-018-9434-x
- Bertsch, Pesta, Wiscott & McDaniel (2007). *Memory & Cognition* 35:201–210. https://doi.org/10.3758/BF03193441
- St. Hilaire, Chan & Ahn (2023). *Psychonomic Bulletin & Review* 31(2):411–441. https://doi.org/10.3758/s13423-023-02353-8

### 经典实验
- Roediger & Karpicke (2006). *Psychological Science* 17(3):249–255. https://doi.org/10.1111/j.1467-9280.2006.01693.x
- Karpicke & Roediger (2008). *Science* 319(5865):966–968. https://doi.org/10.1126/science.1152408
- Karpicke, Butler & Roediger (2009). *Memory* 17(4):471–479. https://doi.org/10.1080/09658210802647009
- Kornell & Bjork (2008). *Psychological Science* 19(6):585–592. https://doi.org/10.1111/j.1467-9280.2008.02127.x
- Rohrer & Taylor (2007). *Instructional Science* 35:481–498. https://doi.org/10.1007/s11251-007-9015-8
- Rohrer, Dedrick & Stershic (2020). *Journal of Educational Psychology* 112(1):40–52. https://doi.org/10.1037/edu0000367
- Deslauriers, McCarty, Miller, Callaghan & Kestin (2019). *PNAS* 116(39):19251–19257. https://doi.org/10.1073/pnas.1821936116
- Hartwig & Dunlosky (2012). *Psychonomic Bulletin & Review* 19:126–134. https://doi.org/10.3758/s13423-011-0181-y

### 理论/框架
- Bjork & Bjork (2011). *Making Things Hard on Yourself, But in a Good Way.* In *Psychology and the Real World*. https://bjorklab.psych.ucla.edu/wp-content/uploads/sites/13/2016/04/EBjork_RBjork_2011.pdf
- Bjork, Dunlosky & Kornell (2013). *Annual Review of Psychology* 64:417–444. https://doi.org/10.1146/annurev-psych-113011-143823
- Sweller (1988). *Cognitive Science* 12(2):257–285. https://doi.org/10.1207/s15516709cog1202_4
- Sweller, van Merriënboer & Paas (2019). *Educational Psychology Review* 31:261–292. https://doi.org/10.1007/s10648-019-09465-5
- Cowan (2001). *Behavioral and Brain Sciences* 24(1):87–114. https://doi.org/10.1017/S0140525X01003922
- Mayer (2024). *Educational Psychology Review* 36(1). https://doi.org/10.1007/s10648-023-09842-1
- Fiorella & Mayer (2016). *Educational Psychology Review* 28:717–741. https://doi.org/10.1007/s10648-015-9348-9
- Fiorella (2023). *Educational Psychology Review* 35(2). https://doi.org/10.1007/s10648-023-09769-7
- de Bruin et al. (2023). *Educational Psychology Review* 35(2). https://doi.org/10.1007/s10648-023-09766-w
- Yan, Sana & Carvalho (2024). *Policy Insights from the Behavioral and Brain Sciences* 11(1):59–66. https://doi.org/10.1177/23727322231218906

### 2023–2026 新证据
- Ruitenburg, Goos, Lambert, Kirschner, Jarodzka & Camp (2026). *Educational Psychology Review* 38(1). https://doi.org/10.1007/s10648-026-10225-5
- Binks (2026). *Journal of Evaluation in Clinical Practice* 32(1). https://doi.org/10.1111/jep.70349
- Sigayret, Parmentier & Silvestre (2026). *Frontiers in Psychology* 17. https://doi.org/10.3389/fpsyg.2026.1727423
- Mawson & Kang (2025). *Behavioral Sciences* 15(6):771. https://doi.org/10.3390/bs15060771
- Franzoi, Cembrani, Mulatti & Treccani (2025). *Frontiers in Psychology* 16. https://doi.org/10.3389/fpsyg.2025.1632206
- Hartwig & Rohrer (2025). *Behavioral Sciences* 15(8):1047. https://doi.org/10.3390/bs15081047
- Little & Nepangue (2025). *Behavioral Sciences* 15(5):662. https://doi.org/10.3390/bs15050662
- Don, Boustani, Yang & Shanks (2024). *JEP: LMC* 50(11):1791–1810. https://doi.org/10.1037/xlm0001382
- Price, Wang, O'Neill, Morgan, Chodavarapu & Bazemore (2024). *Academic Medicine* 100(1):94–102. https://doi.org/10.1097/acm.0000000000005856
- Pyke, Lunau & Javadi (2024). *Quarterly Journal of Experimental Psychology* 78(10):2181–2195. https://doi.org/10.1177/17470218241308143
- Lawson & Mayer (2024). *Frontiers in Psychology* 15:1452385. https://doi.org/10.3389/fpsyg.2024.1452385
- Clinton-Lisell & Litzinger (2024). *Frontiers in Psychology* 15:1428732. https://doi.org/10.3389/fpsyg.2024.1428732
- Roelle, Endres, Abel, Obergassel, Nückles & Renkl (2023). *Educational Psychology Review* 35(4). https://doi.org/10.1007/s10648-023-09810-9
- Huang, Zheng, Yu & Chen (2023). *Frontiers in Psychology* 14:1093653. https://doi.org/10.3389/fpsyg.2023.1093653
- Fraundorf, Caddick, Nokes-Malach & Rottman (2023). *Cognitive Research: Principles and Implications* 8:55. https://doi.org/10.1186/s41235-023-00508-8

### 其他
- Samani & Pan (2021). *npj Science of Learning* 6(1). https://doi.org/10.1038/s41539-021-00110-x
- Sala, Aksayli, Tatlidil, Tatsumi, Gondo & Gobet (2019). *Collabra: Psychology* 5(1):15. https://doi.org/10.1525/collabra.203
- Kassai, Futó, Demetrovics & Takács (2019). *Psychological Bulletin* 145(2):165–188. https://doi.org/10.1037/bul0000180

---

## 14. 检索方法与局限

**方法**：
- `websearch` 在本环境不可用；改用 **OpenAlex API**（题录、摘要、引用数）、**Crossref**（DOI、作者、卷期）、**Europe PMC**（开放全文 XML，用于核对数字）、**Semantic Scholar**（开放 PDF 链接）、**ERIC**（教育摘要）。
- 对关键论文优先取**一手摘要/开放全文**；对无法获取全文的论文，使用**多篇独立综述的交叉引用**核对数字（例如 Adesope 2017 的 g≈0.61 由 2018/2023 两篇综述交叉支持）。
- 效应量统一记为 Hedges' g 或 Cohen's d（两者在小样本下略有差异，本文按原文报告）。

**局限**：
1. **发表偏倚**：教育心理学元分析普遍存在小样本效应高估；2026 课堂元分析的平均值低于早期实验室元分析，提示早期文献可能高估。
2. **WEIRD 偏差**：多数研究来自北美/欧洲；Agarwal 2021 仅 6% 来自非 WEIRD 国家。
3. **材料差异**：词汇/事实类研究多，复杂概念/长文本/多媒体少；把实验室结论外推到"读论文/听播客"需谨慎。
4. **效应量异质性**：交错 I²=77%；同一方法在不同任务上可正可负，平均值会误导。
5. **元认知测量**：JOL/信心评分本身可能有反应性（提示"要判断"会轻微改变学习），不能完全等同于自然状态。
6. **AI 相关证据更新极快**：本文件只收录与学习机制直接相关的 2024–2025 研究；AI 教学设计请以 `ai-learning-2025-2026.md` 为准。

---

## 15. 一句话回答"什么真正促进长期保持与迁移"

**长期保持**：**检索（带反馈）+ 间隔 + 交错（限可辨别任务）** 是证据最稳的三件套；生成/自我解释是理解与迁移的放大器；划重点/重读/总结只能做辅助。

**迁移**：**近迁移可训练，远迁移很罕见**。要迁移，必须用**新情境、应用题、反例、跨来源综合**去练，并且不要承诺"学完就会通用思考"。

**产品**：把"难"设计进流程（检索、间隔、交错），把"校准"做进反馈（信心、延迟测验），把"生成"做成有支架的动作（解释、教别人），把"流畅"当作警告信号而不是成功信号。
