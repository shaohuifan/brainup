# AI × 学习：2025–2026 最新研究（双刃剑证据汇编）

> 定位：`principles/raw/` 原始资料层。本文件只做**证据整理**，不做产品决策；综合判断见 `principles/wiki/synthesis.md`。
> 调研日期：2026-11-14（检索工具：websearch + webfetch；一手论文页/机构页优先，媒体解读仅作补充）
> 覆盖：MIT 认知债、宾大"无护栏 AI"、哈佛 AI 导师 RCT、2025–2026 元分析群、认知卸载/批判性思维、反馈研究、Bloom 2σ 再讨论、EDUCAUSE/SCALE/Learning Scientists。

## 0. 怎么读这份文件（证据分级）

| 级别 | 含义 | 例子 |
|---|---|---|
| **A** | 预注册 RCT / 大样本面板 / 同行评审顶刊 | Bastani 2025 (PNAS)、Kestin 2025 (Sci Rep)、Strömberg 2026 (CEPR DP) |
| **B** | 同行评审但样本小/单点/短期；或高质量准实验 | Gerlich 2025 (Societies)、Fütterer 2026 (EPR) |
| **C** | 预印本、未评审、或只有相关性/自评数据 | Kosmyna 2025 (arXiv)、Lee 2025 (CHI，自评) |
| **D** | 机构报告/权威博客/评论（用于校准共识，不作因果证据） | EDUCAUSE Horizon 2026、SCALE 2026 |

**本文件的一条总论**（下面每条证据都是它的注脚）：

> 决定学习效果的不是"有没有 AI"，而是**任务期间 AI 替学生完成了哪一段认知劳动、以及之后是否在无 AI 条件下被检验**。
> 同一批 2026 年元分析给出的平均效应是 **g ≈ 0.36–0.68**，但**预测区间包含 0 甚至负值**；正负号由设计决定，不由模型能力决定。

---

## 1. 证据地图（先看这张表）

| # | 研究 | 设计 | 关键数字 | 方向 |
|---|---|---|---|---|
| 1 | Kosmyna 2025（MIT） | 54 人 EEG，4 个月，3 组 | LLM 组脑连接最低（最多低 55%）；83% 无法引用自己刚写的句子 | 负（机制） |
| 2 | Bastani 2025（PNAS） | ~1000 名土耳其高中生 RCT | 练习 +48%/+127%；撤掉 AI 后考试 **−17%**；导师模式 −0.4%（不显著） | 负/中性 |
| 3 | Strömberg 2026（CEPR） | 26,811 人 × 30 个月面板 | 作业分 +18%、时间 −30%；月考 **−20%（1.4 SD）**；高考/中考 −18%/−24% | 负 |
| 4 | Liu et al. 2026（CMU） | 3 个 RCT，N=354/667/201 | 撤掉 AI 后解题率 −0.42 SD，放弃率翻倍；只对"直接要答案"的人有害 | 负（坚持性） |
| 5 | Liu et al. 2026（大学 RCT） | 2,379 名学生，30 位教师 | 期末成绩 **−0.27~−0.37 SD**，课程活动参与 −0.90 SD | 负 |
| 6 | Gerlich 2025（Societies） | 666 人横断面 | AI 使用 × 批判性思维 r = −0.68；卸载中介 | 负（相关性，方法论有瑕疵） |
| 7 | Lee et al. 2025（CHI） | 319 名知识工作者，936 例 | 越信任 AI → 批判性思维投入越少 | 负（自评） |
| 8 | Kestin 2025（Sci Rep） | 194 人交叉 RCT，哈佛物理 | 后测中位数 4.5 vs 3.5；**0.63 SD（分位回归 0.73–1.3 SD）**；49 分钟 vs 60 分钟 | 正 |
| 9 | StudentBench 2026 | 2,383 人，GRE | AI 导师 ≈ 人类导师（p=.015），成本低 918× | 正 |
| 10 | De Simone 2025（World Bank） | 尼日利亚 1,328 人 RCT | +0.31 SD；校内英语考试 +0.21 SD | 正 |
| 11 | Henkel 2024（Ghana） | 11 校 477 人 | d = 0.36（8 个月，每周 2×30 分钟） | 正 |
| 12 | Harrison 2026（GCSE） | 929 人微 RCT | g = 0.33（四周，AI 批改） | 正 |
| 13 | Oreopoulos & Low 2026（Khanmigo） | 6,902 学生·学期，2 年 | +0.06~0.08 SD/年（≈纯练习软件） | 弱正 |
| 14 | 元分析群（2025–2026） | 19–58 项研究 | g = 0.36 ~ 0.86；调节变量＞主效应 | 条件性正 |
| 15 | CMU GAITAR 2026 | 18 项校内实验 | 总 g=0.36；"思考伙伴+迁移测验" 0.57；"代做+不测验" 0.56；"思考伙伴+不测验" 不显著 | 条件性正 |

---

## 2. 负面证据之一：MIT Media Lab《Your Brain on ChatGPT》

**Kosmyna, N., Hauptmann, E., Yuan, Y. T., Situ, J., Liao, X.-H., Beresnitzky, A. V., Braunstein, I., & Maes, P. (2025).**
*Your Brain on ChatGPT: Accumulation of Cognitive Debt when Using an AI Assistant for Essay Writing Task.* arXiv:2506.08872（v1 2025-06-10；v2 2025-12-31；216 页，仍为预印本）。
URL: https://arxiv.org/abs/2506.08872 ｜机构页 https://www.media.mit.edu/projects/your-brain-on-chatgpt/publications/

**设计**：54 名波士顿地区大学生（18–39 岁），3 组 × 4 个月：①只用 GPT-4o；②只用 Google 搜索；③"只用大脑"。每场 20 分钟写 SAT 风格议论文（如"我们说话前应该总是先思考吗"）。第 4 场交叉换组：LLM→Brain（18 人中一部分）、Brain→LLM。测 EEG（dDTF 有向连接）、NLP 文本分析、两位英语教师评分 + AI judge、访谈。

**关键数字**
- 脑连接强度随外部支持递减：Brain-only 最强 → 搜索居中 → **LLM 组最弱；报道称 LLM 组连接性比 Brain-only 低至 55%**。
- **83.3%（15/18）LLM 组受试者无法准确引用自己几分钟前写的句子**；搜索组与纯脑组各只有 11.1%（2/18）失败（F(2,51)=79.98, p<.001）。
- 交叉后 LLM→Brain 组出现 alpha/beta 连接下降（"投入不足"），**78% 仍无法引用自己的文章**；Brain→LLM 组则表现出更高的回忆与更成熟的提示策略。
- 文本同质化：LLM 组内 NER/n-gram/主题本体高度相似；LLM 组使用的命名实体是其他组的 2–3 倍，但原创性更低。
- 所有权感（ownership）：LLM 组最低，纯脑组最高。
- 作者提出 **"cognitive debt（认知债）"**：短期省力，长期以批判性思维、创造力、独立判断与深层加工为代价；建议"在学习者完成足够的自主认知努力之前，推迟 LLM 介入"。

**边界条件与批评（必须一起读）**
- 不是学习效果研究：测的是**写作过程中的神经投入与记忆/所有权**，不是考试成绩。
- 样本小（54/18）、单任务、单次 20 分钟、非随机长期追踪；作者本人在 Nature 采访中明确反对过度解读："这不是'脑子变笨'"。
- **dDTF 是网络连接指标，不直接等于努力、思考质量或学习**（alphaXiv 评论；Nature 2025-06-25 报道 https://www.nature.com/articles/d41586-025-02005-y）。
- 但**"引用不出自己刚写的东西"是可复现的行为学信号**，对产品设计极有价值（见 §11 的"引用探针"）。

**为什么仍要重视它**：它是目前唯一给出"神经层面 + 行为层面 + 文本层面"三重同向证据的研究，且"节省的认知劳动会以记忆与所有权为代价"这一机制，后来被 Strömberg 2026 与 Liu 2026 在真实学业结果上重复出来。

---

## 3. 负面证据之二：宾大"无护栏的生成式 AI 会伤害学习"

**Bastani, H., Bastani, O., Sungu, A., Ge, H., Kabakcı, Ö., & Mariman, R. (2025).** *Generative AI without guardrails can harm learning: Evidence from high school mathematics.* **PNAS** 122(26): e2422633122.
URL: https://www.pnas.org/doi/10.1073/pnas.2422633122 ｜SSRN 2024 版 https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4895486

**设计**：土耳其一所大型高中，9–11 年级约 50 个班、**近 1,000 名学生**，2023 年秋季，4 次 90 分钟复习课。每次课三段：教师讲题 → **随机分组的练习段**（唯一干预点）→ **闭卷无 AI 的 30 分钟考试**（考题与练习题概念同构）。三臂：
- **GPT Base**：普通聊天界面，system prompt 里带当前题目并要求"当家教"；
- **GPT Tutor**：同一界面，但 prompt 内嵌**教师写的正确解法 + 常见错误 + 只给提示不给答案**的指令；
- **Control**：只有课本和笔记。

**关键数字**
- 练习段（有 AI）：Base **+48%**、Tutor **+127%**（对照组均值 0.284，0–1 量表）。
- 闭卷考试（无 AI）：**Base −17%**（−0.054，约 −0.19 SD）；Tutor −0.004（不显著，即"伤害被消除但没有额外收益"）。
- 机制：Base 组最常见的行为是**直接索要答案并抄写**；2023 年的 GPT-4 在这类题上只有 **51% 正确率**。
- **学生完全没意识到自己学得更差**：两臂自评学习感都高于实际。
- 交互演化：Tutor 组随时间提出更少表层问题；Base 组相反。

**边界条件**
- 单一学校、单一学科（数学）、Fall 2023 的 GPT-4、短期（4 次课）、只测即时后测。
- 作者自己列出：模型已进步（错误率机制被削弱），但**"抄答案"机制不因模型变强而消失**。
- **重要细节：连"扮演家教"的 prompt 都挡不住伤害**——说明软提示不是护栏，结构才是。

---

## 4. 负面证据之三：中国 26,811 人面板（目前最强的"长期学业代价"证据）

**Strömberg, D., Lei, V., & Wu, Y. (2026).** *The Generative AI Learning Penalty: Evidence from Chinese Secondary Education.* CEPR DP 21577 / SSRN 6868618（NBER 会议稿 PDF 可读）。
URL: https://cepr.org/publications/dp21577 ｜VoxEU 解读 https://cepr.org/voxeu/columns/generative-ai-learning-penalty-secondary-school

**设计**：中国中部某县，**26,811 名 7–12 年级学生，30 个月行政数据，9 个学科**；把每周作业（分数 + 平台记录的完成时长）与月考、县统考、中考、高考打通。用**交错采用（staggered adoption）的 DiD**，不是 RCT。

**关键数字**
- 采用 AI 后 6 个月内：**作业分 +18%**，单次作业时间 **64 分钟 → 45 分钟（−30%）**；
- 同期**闭卷月考 −20%**（= **1.4 SD**）；全期平均 −13%；
- 高利害考试：**中考 −24%、高考 −18%**（1.5 / 1.3 SD），且**要两年才达到最大伤害**（→ 短期研究系统性低估长期代价）；
- 异质性：**81% 的 AI 使用者行为符合"作业外包"**（比最快的非 AI 学生更快 + 作业分异常高）；这部分人承担了几乎全部损失；**保持与非 AI 学生相同作业时长的 AI 使用者，损失很小（考试分接近）**；
- 学科：社科 −27%（政治/地理最重）> STEM −22% > 英语 −17% > 语文 −9%；
- 人群：**初中生、高成就学生、男生**损失更大；
- 时间趋势：同样 5 个月暴露，2023 年初的估计惩罚约 25%，到 2025 年 6 月降到约 16%（人在适应，但未归零）。

**边界条件**：非实验设计（依赖平行趋势）；作业时长是代理变量；无法区分"AI 降低了学习效率"与"AI 挤出了其他学习行为"（作者计算作业时间减少只占总学习时间 5–6%，远小于 20% 的分数跌幅，暗示还有课堂参与等渠道）。

**为什么它对 brainup 最重要**：它把"作业表现 ↑ / 无辅助考试 ↓"的分裂，放大到了**两年后的高利害结果**上；并且给出了一个可操作的分界线——**"用时有没有塌缩"**。

---

## 5. 负面证据之四：AI 削弱"坚持性"（机制最干净的一组实验）

**Liu, G., Christian, B., Dumbalska, T., Bakker, M. A., & Dubey, R. (2026).** *AI Assistance Reduces Persistence and Hurts Independent Performance.* arXiv:2604.04721（CMU / Oxford / Berkeley / MIT / UCLA）。
URL: https://ai-project-website.github.io/AI-assistance-reduces-persistence/ ｜ https://arxiv.org/abs/2604.04721

**设计**：三个预注册 RCT。被试先在有 GPT-5 侧栏的条件下做 12 道题，**然后 AI 被无预警撤走**，再做 3 道测试题。

**关键数字**
- 实验 1（分数运算，N=354）：测试段解题率 **0.57 vs 0.73**（p<.001，**d = −0.42**）；**跳过率 0.20 vs 0.11**（d=0.25）。
- 实验 2（N=667，加前测排除能力差、控制组同款侧栏界面）：复现，**0.71 vs 0.77**（d = −0.19）。
- 实验 3（SAT 风格阅读理解，N=201）：**0.76 vs 0.89**（d = −0.42）；跳过率 0.08 vs 0.01。
- **归因**：**61% 的人直接用 AI 拿答案**，全部损害集中在这部分人身上；**用 AI 求提示/澄清的人，与对照组无显著差异**。
- 暴露时长：**仅约 10 分钟**。

**边界条件**：成人/在线样本、单次会话、即时测试；但**跨算术与阅读理解双重复现**，且"提示 vs 答案"的分野与 Bastani、Strömberg 完全一致。

**一句话**：**伤害不是来自"用了 AI"，而是来自"把生成动作交给了 AI"**；10 分钟就足以削弱坚持性。

---

## 6. 负面证据之五：大学规模的"默认设置"灾难

**Liu, J., Sweet, T., Chen, M. H., Engelberg, J., Masters, M. C., Clark, M., Persaud, A., Lancaster, A., Hollingsworth, J. K., & Rice, J. K. (2026).** *The effects of course-integrated AI tutoring on student performance and engagement: A randomized university trial.* EdWorkingPaper 26-1598.
URL: https://doi.org/10.26300/y3f8-vh05 （经 Avanti 文献库转述，2026-10-26 打开）

**设计**：美国大型公立大学，30 位教师、**2,379 名学生**，教师层面随机；课程内嵌 GPT-4o 导师（RAG 读课程材料）。

**关键数字**
- **期末成绩 −0.27 ~ −0.37 SD**；
- 被设定的课程活动参与 **−0.90 SD**（同课程样本）；
- **第一代大学生损失更大**；
- **默认值决定一切**：只有 2 位教师整个学期把工具切到"导师模式"，其余留在"直接给答案"。

**边界**：单校、一学期；但它是"AI 越容易拿到答案，人越会退回到最省力路径"的最直接证据，且说明**产品默认值 = 事实上的教学法**。

---

## 7. 正面证据之一：哈佛物理 AI 导师 RCT（最强的正面结果）

**Kestin, G., Miller, K., Klales, A., Milbourne, T., & Ponti, G. (2025).** *AI tutoring outperforms in-class active learning: an RCT introducing a novel research-based design in an authentic educational setting.* **Scientific Reports** 15: 17458（2025-06-03）。
URL: https://doi.org/10.1038/s41598-025-97652-6 ｜PubMed https://pubmed.ncbi.nlm.nih.gov/40537565/ ｜哈佛报道 https://news.harvard.edu/gazette/story/2024/09/professor-tailored-ai-tutor-to-physics-course-engagement-doubled/

**设计**：哈佛最大的物理课 PS2（生命科学方向），2023 秋，**194 名有效学生**，**交叉设计**：两周两课（表面张力、流体），一周 A 组在家用 AI 导师、B 组上主动学习课，第二周互换。**内容与讲义完全相同**，差别在呈现方式（视频 vs 现场）与反馈来源（AI vs 同伴+教师）。AI 导师 "PS2 Pal" 基于 GPT-4，prompt 内嵌**分步解法**，平台**强制按问题子步骤推进**。

**关键数字**
- 前测中位数 2.75；后测中位数 **AI 组 4.5（N=142） vs 课堂组 3.5（N=174）**；秩和检验 z=−5.6，p<10⁻⁸；
- **中位学习增益超过 2 倍**；OLS 效应量 **0.63 SD**（作者认为受天花板效应低估），分位回归 **0.73–1.3 SD**；
- **用时更少**：AI 组中位 **49 分钟**，课堂按 60 分钟学习计；且**用时与后测成绩不相关**；
- 体验：投入感 4.1 vs 3.6（p<.0001）、动机 3.4 vs 3.1（p<.001）；兴趣与成长型思维无差异；
- 对 FCI 前后 40% 上下的学生、科学态度高低于 65% 的学生，优势都在（p<.001）。

**边界条件（作者自己列了，务必照抄）**
- 两节课、即时后测、**没有延迟保持测验**；
- 精英美国本科生、单一课程；
- 依赖：能遵循复杂 prompt 的模型、**教师逐题撰写的 prompt**、结构化平台、高质量教学视频、内容适合"首次接触"；
- **内容层级只到 Bloom 的 understand/apply/analyze**；作者明说**不假定在需要复杂综合与高阶批判性思维的场景也成立**；
- 比较的是"整包条件"（在家 vs 在课堂、视频 vs 现场、AI vs 同伴），无法拆分单一要素；
- 干预本质是**教学设计**，不是模型：任何人都能调同一个 API，但调不出这个 prompt 与流程。

---

## 8. 正面证据之二：中低收入与真实课堂的"中等效应"带

| 研究 | 设计 | 数字 | 关键设计要素 |
|---|---|---|---|
| **De Simone et al. 2025**（World Bank PRWP 11125） | 尼日利亚 Benin City 9 所公立学校，SS1（约 15 岁），12 次 90 分钟课后实验室，两人一机，用 Copilot，教师提供"让 AI 当导师而不是答案机"的起始 prompt | 1,328 人随机，759 人完成；**endline +0.31 SD**（SE .068）；英语 +0.24 SD；校内第三学期英语考试 **+0.21 SD**；出勤每多一天 +0.031 SD（平均出勤 72%） | 有人监督、脚本化 prompt、共享设备可行 |
| **Henkel et al. 2024**（Rori, arXiv:2402.09809） | 加纳 11 所学校，3–9 年级，每周 2 次 30 分钟，WhatsApp 上跑 8 个月；脚本化微课，卡住先给提示再给解法 | 477 人有前后测；成长分差 3.01/35 题，**d = 0.36** | 短、固定时间表、提示→解法阶梯 |
| **Harrison et al. 2026**（Medly, arXiv:2609.14789） | 英格兰多校微 RCT，GCSE 理化生，每周 30 分钟×4 周，LLM 按考纲批改开放题 vs 自主复习 | 929 → 644；**g = 0.33（0.18–0.48）** | 与考试标准对齐的练习 + AI 批改 |
| **LearnLM Team & Eedi 2025**（arXiv:2512.23633） | 英国 5 校 9–10 年级数学，165 名学生 17 位导师；每条 AI 消息由人类导师审核 | 导师 **76.4%** 的 AI 草稿零/极少修改即通过；迁移到下一主题 66.2% vs 60.7%（**+5.5pp，CI −1.4~+12.4**） | 模型拿到"题目 + 学生的错答 + 迷思说明" |
| **Wang et al. 2024/2026**（Tutor CoPilot, arXiv:2410.03017） | 700+ 人类导师、1,000+ 学生；AI 给**导师**实时建议 | 主题掌握 **+4pp**；对评分最低的导师 **+9pp**；约 20 美元/导师/年 | 增强人不替代人 |
| **Oreopoulos, Liut, Sungu & Low 2026**（NUMI, EdWorkingPaper 26-1552） | >6,000 名中学生，2×2：AI vs 无 AI × 掌握规则（连对 3 题）vs 自由推进；一周后延迟测验 | AI 使"更少尝试、更慢、更准"，**犯错后下一次正确率更高**；掌握规则单独无延迟收益；**AI×掌握规则**在练过的延迟题上约 **+3pp**（边际显著） | AI 的价值在"犯错之后"；掌握规则给"理解"一个理由 |

**共同结构（三份文件独立收敛）**：① 模型手里有**验证过的答案/迷思库**；② **先尝试后提示**，提示只到"下一步"；③ **给完解法立刻做一道无辅助同构题**；④ 有**时间表/剂量**，不是"想用就用"。

---

## 9. 元分析：效应量范围与调节变量（2025–2026 一批）

⚠️ 读元分析前必须记住一件事：**它们测的绝大多数是"带 AI 时的任务表现"，不是"撤掉 AI 后的能力"**。这正是 Bastani 里 +48%/+127% 与 −17% 能同时成立的原因。

| 元分析 | 范围 | 总效应 | 显著调节变量 |
|---|---|---|---|
| **Nature HSSC 2026**（35 项，4,193 人）https://www.nature.com/articles/s41599-026-07019-z | 2022–2024 | **g = 0.670**（CI .495–.844） | 学科、实验时长（>3 个月 g=1.033）、教学模式；**教育阶段与知识类型不显著** |
| **Frontiers Psychology 2026**（36 项，132 个效应，7,229 人）https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2026.1758670/full | 高等教育，三级模型 | **g = 0.499** | **唯一显著调节变量是教学法**：协作学习 **1.026**、混合式 0.633、传统 0.470、个性化 0.351、探究 0.371 |
| **Frontiers Education 2026**（58 项，68 个效应）https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2026.1971476/pdf | 认知/语言 | **g = 0.864**，但 I²≈88%，**预测区间 [−0.213, 1.942]**；PET-PEESE 校正后 **≈0.26–0.45** | 结果域、教育阶段（Holm 校正后不显著） |
| **Ma 2025, JCAL**（34 项）https://onlinelibrary.wiley.com/doi/10.1111/jcal.70117 | — | **0.68**；认知 0.795、能力 0.711、情感 0.507 | 学科；**时长、知识类型、先验知识、工具类型均不显著** |
| **Gu & Yan 2025, JECR**（19 项，24 个效应）https://journals.sagepub.com/doi/10.1177/07356331251349620 | K-12 + 高校 | **g = 0.683** | **教师支持：有 1.426 vs 无 0.077**（唯一显著） |
| **IRRODL 2026**（22 篇，86 个效应，6,992 人）https://doi.org/10.19173/irrodl.v27i1.8775 | — | **0.573**；中学 0.928 > 本科 0.538（不显著） | 教学法：自我调节学习 **1.115** > 案例 0.836 > 游戏化 0.092 |
| **Nature HSSC 2025**（51 项）https://www.nature.com/articles/s41599-025-04787-y | — | 学习成绩 **0.867**；学习感知 0.456；高阶思维 **0.457** | 课程类型、学习模式、时长（4–8 周更稳） |
| **CMU GAITAR 2026**（18 项校内实验）https://www.cmu.edu/teaching/gaitar/gaitaratscale/meta-analysis.html | 单校、跨学科 | **g = 0.36** | **"工具用途 × 是否有迁移任务"**：思考伙伴+迁移 **0.57**；代做+不迁移 **0.56**；**思考伙伴+不迁移 ns（p=.067）**；**"增补" 0.51 vs "替代" 不显著** |

**三条可操作的读法**
1. **g ≈ 0.4 是"诚实"的中心值**（CMU 0.36、Zhu 校正后 0.26–0.45、World Bank 0.31、Ghana 0.36、GCSE 0.33）；0.7–0.9 多来自小样本、自评、短时长、以及"带 AI 的即时表现"。
2. **最强的单一调节变量是"教学法/教学整合方式"，不是模型版本**：协作 1.03、教师支持 1.43、自我调节学习 1.12、增补 vs 替代 0.51 vs ns。
3. **元分析的平均值会把"伤害"稀释掉**：正负在同一分布里，Huntington-Klein 2026 的美国高中聚合估计只有 −0.0096 SD/SD（上界约 −0.04 SD），而 Strömberg 的校内月考是 −1.4 SD——**平均无害 ≠ 个体无害**。

---

## 10. 认知卸载与批判性思维

### 10.1 Gerlich 2025（最常被引用，也最需要打折扣）

**Gerlich, M. (2025).** *AI Tools in Society: Impacts on Cognitive Offloading and the Future of Critical Thinking.* **Societies** 15(1): 6.
URL: https://www.mdpi.com/2075-4698/15/1/6

- 英国 **666 人**混合方法（问卷 + 50 人深访）；HCTA 等量表 + 自评。
- **AI 使用 × 批判性思维 r = −0.68**；AI 使用 × 认知卸载 **r = +0.72**；卸载 × 批判性思维 **r = −0.75**；
- 中介：总效应 b=−0.42，经卸载的间接效应 b=−0.25（p<.001），直接效应 b=−0.17；
- 年龄：17–25 岁依赖最高、得分最低；教育程度正向预测批判性思维（与 AI 使用无关）。

**必须标注的边界（否则会误用）**
- **横断面相关，不能推因果**；"批判性思维"大部分是**自评**；
- 论文表格内部不一致：Table 5 与 Table 6 给同一对变量不同系数（−0.49 vs −0.68），作者另发了 OSF 更正说明（只更正 ANOVA 表，未解释相关系数差异）——https://doi.org/10.17605/osf.io/edb5y
- 结论方向与 Lee 2025、Liu 2026、Strömberg 2026 一致，但**它本身只应作为"假设来源"，不是"证据"**。

### 10.2 Lee et al. 2025（CHI，机制更可信）

**Lee, H.-P., Sarkar, A., Tankelevitch, L., Drosos, I., Rintel, S., Banks, R., & Wilson, N. (2025).** *The Impact of Generative AI on Critical Thinking: Self-Reported Reductions in Cognitive Effort and Confidence Effects.* **CHI '25**, Article 1121.
URL: https://www.microsoft.com/en-us/research/publication/the-impact-of-generative-ai-on-critical-thinking-self-reported-reductions-in-cognitive-effort-and-confidence-effects-from-a-survey-of-knowledge-workers/

- 319 名每周使用 GenAI 的知识工作者，**936 个真实任务案例**；59.29% 的案例中自报"动用了批判性思维"。
- **对 AI 的能力越有信心 → 批判性思维投入越少；对自己的能力越有信心 → 投入越多。**
- 批判性思维的性质发生位移：Knowledge/Comprehension 从"找信息"变成"验证信息"；Application 从"解题"变成"整合 AI 输出"；Analysis/Synthesis/Evaluation 从"执行"变成"监理（task stewardship）"。
- 设计含义：工具应针对三重障碍——**意识不到（awareness）、没动力（motivation）、不会做（ability）**。

### 10.3 概念框架（用于给产品命名与埋点）

| 概念 | 出处 | 一句话 |
|---|---|---|
| **Cognitive offloading** | Risko & Gilbert 2016, *Trends Cogn Sci* 20(9):676 | 把认知需求外包给环境，本身中性；关键在"是否替代了本该建立的内部通路" |
| **Cognitive debt** | Kosmyna et al. 2025 | 短期省下的认知劳动，长期以能力为利息偿还 |
| **Metacognitive laziness** | Fan et al. 2024, arXiv:2412.09315 | AI 让作品变好，但**元认知步骤（计划/监控/评估）减少**，知识获得与迁移无提升 |
| **Cognitive surrender** | Shaw & Nave 2026（Wharton 工作论文, doi:10.31234/osf.io/yk25n_v1） | 从"卸载"升级为"放弃判断"：接受高置信度的合成结果，不再形成自己的立场 |
| **Premature cognitive offloading** | Lee, R. T. 2026（Learning Scientists 客座, 2026-10-29） | 在内部通路尚未建立（K-12）时就外包，等于替脚手架浇混凝土之前拆掉模板 |
| **Performance vs Learning** | Soderstrom & Bjork 2015；Bjork & Bjork 2011 | **训练中表现好 ≠ 学得好**；"合意困难"降低即时表现、提升长期保持 |

### 10.4 关键类比：AI 的"易"和间隔/交错/检索的"难"是同一件事

**Kaminske, A. N. (2026).** *Unwanted Ease.* The Learning Scientists, 2026-08-21.
URL: https://www.learningscientists.org/blog/2026/8/21

作者把三组曲线叠在一起，形状完全一致（练习期占优 → 测试期反转）：
- 交错 vs 分块（Taylor & Rohrer 2010）；
- 间隔 vs 集中（massed 在即时测验更好，延迟测验更差）；
- 检索 vs 重读（即时测验重读更好，延迟后检索胜出）；
- **AI 辅助 vs 无辅助（Liu et al. 2026 的分数题曲线）**。

结论：**"AI 让当下的学习感觉更顺"这件事本身，就是一个预警信号，而不是成效证明**；但难度必须落在"刚好够难"的区间（Vygotsky ZPD / 合意困难），过难同样有害。

---

## 11. 反馈研究：经典结论 + AI 反馈 2024–2026 证据

### 11.1 经典（仍然是设计基准）

**Hattie, J., & Timperley, H. (2007).** *The Power of Feedback.* **Review of Educational Research** 77(1): 81–112.
URL: https://journals.sagepub.com/doi/10.3102/003465430298487

- 综合 12 项元分析、196 项研究：反馈平均 **ES ≈ 0.79**（Table 2 中 "Feedback" 一项覆盖 74 项元分析、4,157 项研究、5,755 个效应，ES=0.95）；高于先验能力 0.71、SES 0.44、作业 0.41。
- **三个问题**：Where am I going? How am I going? Where to next?
- **四个层级**：task / process / self-regulation / self。**层级决定效果**：
  - 任务级"关于上次尝试的变化" 0.55 vs 无 0.28；
  - **打击学生的任务反馈 −0.14**；
  - 关于任务的表扬 0.09 vs 无 0.34；
  - **praise（针对人）0.14，punishment 0.20**——最低。
- **时机**：task 级可延迟，**process 级应立即**；正/负反馈的效果取决于层级与自我效能。

**Wisniewski, B., Zierer, K., & Hattie, J. (2020).** *The Power of Feedback Revisited: A Meta-Analysis.* **Frontiers in Psychology** 10:3087.
URL: https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2019.03087/full

- 435 项研究、994 个效应、N>61,000：平均 **d ≈ 0.48**（另一模型报 0.55），**17% 的效应是负的**；
- **"信息量"是核心调节变量**：高信息反馈（任务+过程+自我调节）效应最大；单纯强化/惩罚最小；
- 结论句可直接引用："反馈不能被当作单一处理（treatment）"。

### 11.2 AI 反馈（2024–2026）

| 研究 | 设计 | 数字 | 要点 |
|---|---|---|---|
| **AI 反馈与人类反馈对比元分析 2025**（41 项，4,813 人）https://www.tandfonline.com/doi/full/10.1080/01443410.2025.2553639 | 元分析 | 差异 **g = 0.25，不显著**（CI −0.11~0.60）；感知 g=−0.20 ns | **AI 反馈"不比人差"，但也不更好**；I²=95%，预测区间 −2.21~2.93 |
| **AI 英语写作反馈元分析 2026**（43 项，234 个效应）https://www.tandfonline.com/doi/full/10.1080/2331186X.2026.2665494 | 三级元分析 | 总 **g = 0.58**；**混合人机 0.80** vs **纯 AI 0.26（不显著）**；AI+教师 **1.44** | 纯 AI 反馈单独用效果站不住 |
| **算法反馈元分析 2026**（33 项，5 种欧洲语言）https://doi.org/10.1016/j.asw.2026.101034 | 元分析 | 总 **g = 0.36**；表层后测 0.31，**保持期 −0.02**；深层后测 0.31、**保持期 0.54**；**ChatGPT 反馈不显著** | 表层（语法）改得快、忘得也快；深层（结构/内容）才有持续效应 |
| **AI 个性化反馈元分析 2025**（40 项，5,849 人）https://journals.sagepub.com/doi/10.1177/07356331251410020 | 元分析 | 学习结果 **g = 0.58**；**动机 g = 0.82** | 显著调节：学段、实验时长、反馈类型 |
| **GAI 形成性反馈实验 2025**（114 名师范生，4 条件）https://link.springer.com/article/10.1007/s10639-025-13778-0 | RCT | **多层级反馈 > 任务级**（作品与课程表现）；**"焦点"而非"复杂度"影响共享元认知** | 对应 Hattie 的层级结论 |
| **GenAI vs 混合反馈 L2 写作 2025**（60 名中国 EFL，12 周）https://www.tandfonline.com/doi/full/10.1080/17501229.2025.2503890 | 两组 | 纯 GenAI 改善语法/句式；**批判性思维与组织无显著提升**；混合组在组织与批判性思维上显著更好 | 高阶能力需要人 |
| **Pardos & Bhandari 2024**（274 名成人，PLOS ONE）https://doi.org/10.1371/journal.pone.0304013 | 在线 RCT | ChatGPT 编写的"完整解法"提示 ≈ 人工编写提示（无显著差异）；**32% 的 ChatGPT 提示未通过质量检查** | 生成内容必须校验 |

### 11.3 反馈设计的可执行结论

1. **层级 > 数量**：说"这一步为什么错（process）"比说"错了（task）"强；说"你这次比上次少跳了一步（task + 变化）"又比单纯判对错强。
2. **具体性 = 信息量**：AI 的独特优势是"能引用学生原话/原步骤"，而不是"能夸"。
3. **时机分工**：任务级可稍延迟（让学生先自己发现），过程级要即时。
4. **纯 AI 反馈会退化**：它倾向于改表层（语法、措辞），这与"保持期 −0.02"一致；**深层反馈需要人定的标准/评分细则**。
5. **自评是污染源**：Bastani 里学生自评学习感更高但实际更差；AI 反馈的"感知"与"效果"也不同向（g=−0.20 vs 0.25）。

---

## 12. Bloom 2σ 问题的再讨论（2024–2026）

**原始主张**：Bloom, B. S. (1984). *The 2 Sigma Problem: The Search for Methods of Group Instruction as Effective as One-to-One Tutoring.* Educational Researcher 13(6): 4–16。掌握学习 + 一对一辅导 ≈ +2 SD（中位数学生 → 98 百分位）。

**2024–2026 的共识：2σ 不可复现，且从来不是"辅导单独"的效果。**

| 来源 | 关键论点/数字 |
|---|---|
| **Education Next 2024-03**（Yeh 风格的长文）https://www.educationnext.org/two-sigma-tutoring-separating-science-fiction-from-science-fact/ | 严格评估的辅导效应"从 2 SD 到 0 甚至负值"都有；**典型值是 ~1/3 SD**；Anania/Burke 的 2σ 来自**窄域自定义测验 + 辅导+教师培训+额外时间+频繁测验反馈**的混合拳。明确警告：**不要向 AI 承诺 2σ** |
| **Nickow, Oreopoulos & Quan 2020**（96 项 RCT 元分析） | 平均 **0.37 SD**；无一项达到 2σ |
| **Ma, Adesope, Nesbit & Liu 2014**（107 个效应，14,321 人） | 智能导师系统 vs 大班教学 **g=0.42**、vs 教科书 0.35、**vs 个别人类辅导 g=−0.11（不显著）** |
| **Attridge 2026-03** https://eliotattridge.com/two-sigma-problem/ | 2σ 依赖少数小样本、小学数学、且掌握学习被混在里面；现代元分析把纯辅导拉到 **0.3–0.7σ**；AI 让"规模化个性化"的成本问题基本解决，**问题变成"学校到底为了什么"** |
| **Fikr Ventures 2026-03** https://www.fikrventures.com/blogs/retire-the-two-sigma | 逻辑闭合：**若 AI ≈ 人类导师，而人类导师 = 0.37，则完美的 AI 导师也只能落在 0.37**；两篇相隔 40 年的独立综合（Cohen 1982 = 0.33，Nickow 2020 = 0.37）互相印证 |
| **StudentBench 2026**（2,383 人，GRE）https://arxiv.org/abs/2609.28470 | AI 辅导与专家人类辅导**学习增益统计等价**（p=.015，±0.25 SD 边界；±0.20 更严边界 p=.023）；7 个 GRE 领域里 5 个 AI 更优；**成本低 918×**（每提升 1 个百分点 $0.0052 vs $4.81）；局限：只测即时增益，无月级保持 |
| **The Think Different 2026-08** https://www.thinkdifferent.blog/blog/the-tutor-problem/ | 把"AI 导师"拆成三类：worked-example 复现型、缺口诊断选讲型（有 40 年 ITS 证据，~0.5σ）、开放式对话型（钱都在这，证据最薄）。**动机/关系可能是 2σ 的一大块**——ITS 无关系仍有增益，但人类导师持续优于 ITS，且差距在落后学生身上最大 |

**对产品的含义（不是学术结论）**：
- 把目标定在 **0.3–0.5 SD** 是诚实的；承诺 2σ 会导向"看起来有效"的设计（更快、更顺、更像被辅导）。
- AI 真正改变的不是 σ 的大小，而是**边际成本**：把"个别化反馈"从稀缺变成免费。因此瓶颈从"能不能个性化"转移到**"学生会不会用、用多久、用来干什么"**（见 §13 SCALE 的剂量数据）。
- 若 2σ 里有相当部分是"有人在乎我"的动机成分，那么**纯 AI 的天花板低于人类导师**，这与 StudentBench 的"等价"并不矛盾——它测的是自愿参与的 GRE 备考者。

---

## 13. 权威机构与报告的结论（2025–2026）

### 13.1 EDUCAUSE Horizon Report 2026 | Teaching and Learning（2026-05-18）
URL: https://library.educause.edu/resources/2026/5/2026-educause-horizon-report-teaching-and-learning-edition ｜PDF https://ai.utah.edu/_resources/documents/horizon_report.pdf

- 方法：STEEP 框架 + 全球专家面板；**新增 "Signals of Change"**（早期信号，不是趋势）。
- 三条与学习直接相关的社会趋势：
  1. **AI 正在重塑"信任信息"的方式**：作者身份、来源、推理过程这些传统可信度线索被削弱；学生可能"跳过自己弄懂这一步"，从而限制批判性思维与新想法。
  2. **AI 正在重塑师生关系**：学生更愿意问 AI 而不是老师 → office hours 等非正式互动减少 → 教师加强审视 + AI 检测误判 → 互不信任。
  3. **AI 正在重新定义教学设计与评价**：传统评价失效 → 转向**过程性、真实性、口头解释、对 AI 输出的批判性评估**；有教师退回蓝皮书/机读卡/现场监考。
- 其它趋势：学术支持 AI 化（加州社区学院 116 校区全面铺开 AI 学习助手，属"信号"级）、网络安全与隐私、招生下滑与经费压力、AI 环境成本、无障碍新规。
- **报告的态度是"两难"而非"乐观/悲观"**：赋能 vs 监控、效率 vs 关系、普惠 vs 分层。

### 13.2 Stanford SCALE（2026-08-20）《AI Tutoring is Not a Monolith》
URL: https://scale.stanford.edu/research-in-action/ai-tutoring-not-monolith

- **高影响力辅导（high-impact tutoring）的定义仍以"真人主导"为准**；当前证据支持"用 AI 增强导师效能与教师产能"，**不支持用 AI 替代**。
- 两个学区 RCT 的剂量数据（关键）：
  - **AI-only：40%–47% 的学生从未使用过平台**；登录者累计只用 4–5 周、**平均每周 2–5 分钟**——远低于产生阅读增益所需剂量；
  - AI + 人类查岗/激励：参与度上升，**但仍未达到有效剂量，阅读成绩无改善**。
- AI 目前的可辩护定位：**补充性练习**；效果同时取决于"软件质量"与"课堂/家庭中的整合方式"。
- 安全前提：数据隐私、学生安全护栏、无监控交互的深度。

### 13.3 The Learning Scientists（2025–2026 三篇要点）
- **《Expert Thinking and AI》Part 1/2（2025-02/03）**：LLM 的"专长"与人类专长结构不同（频率共现 vs 层级概念网络）；工具在**有明确目的 + 专家监督**时最有用；复杂任务上错误率可达 28.6%–91.4%。
- **《What 130,000 Student Questions to AI Reveal About Critical Thinking》（2025-09-04，客座）**：8,600 名学生、约 13 万条提问；**约 1/3 达到较高认知层级，20% 在 Bloom "Analyze" 及以上**；据此设计了 "Go Deeper"——答完后追问一个"高 1–2 层"的问题。→ **提问本身就是生成动作，可以设计**。
- **《Unwanted Ease》（2026-08-21）**：见 §10.4。

### 13.4 跨来源的实践共识（把上面拼起来）
1. **先有人类/结构，再有 AI**（SCALE、Think Different、Horizon 的"关系"趋势）。
2. **评价必须回到"无 AI 条件下能做什么"**（Horizon 的过程性评价、Bastani 的闭卷考试、CMU 的迁移任务）。
3. **剂量与参与度是当前最大瓶颈**，而不是模型能力（Khanmigo、SCALE 的 2–5 分钟/周）。
4. **不要用自评、使用时长、产物质量当学习证据**（Bastani、Fan、Lee）。

---

## 14. 综合：正负证据的边界条件（本文件最重要的一张表）

| 条件 | 结果方向 | 证据 |
|---|---|---|
| AI **直接给答案/代做**，之后**无 AI 测验** | **负**（−0.17 ~ −1.4 SD；坚持性 ↓） | Bastani、Strömberg、Liu 2026 ×2 |
| AI **只给提示/澄清**，学生自己完成生成 | 中性到正（无显著损害） | Liu et al. 2026（hints 组）、Bastani Tutor |
| **模型持有验证过的答案/迷思库 + 强制步骤推进** | **正**（0.3–1.3 SD） | Kestin、De Simone、Henkel、LearnLM |
| **先尝试 → 提示阶梯 → 解法 → 立刻同构无辅助题** | **正**（且是唯一"既有练习增益又有学习增益"的结构） | NUMI、Rori、Avanti 设计规则 |
| 有**教师/人类监督** | **正**（1.43 vs 0.08） | Gu & Yan 2025、Tutor CoPilot、SCALE |
| **协作/混合式**教学法 | **正**（1.03 / 0.63） | Frontiers Psych 2026 |
| **替代**原有教学环节（而非增补） | **无显著效应** | CMU GAITAR（0.51 vs ns） |
| **无迁移测验**的"思考伙伴" | **无显著效应**（p=.067） | CMU GAITAR |
| **自愿、无时间表、无剂量** | **≈0**（0.06–0.08 SD/年） | Khanmigo 2026、SCALE |
| **弱先验知识者**自由使用 | **更可能受损** | Lehmann 2025、Liu 2026（第一代学生） |
| **高先验知识者**用作"解释器/补充" | 更可能受益 | Lehmann 2025 |
| **用时显著缩短 + 分数显著提高** | **强预警信号** | Strömberg 2026（81% 外包者）、Bastani |

---

## 15. 对 brainup 的启示（只列证据直接支持的，不含拍脑袋）

> 前提：brainup 的 LLM Wiki 模式天然是"高认知卸载"形态——LLM 负责总结、交叉引用、一致性维护。这在**簿记层**是纯收益（Karpathy 模式的核心洞察），但在**学习层**恰好命中 §2–§6 的全部风险机制。因此必须把"编译"与"学习"当成两件事。

**A. 结构性问题：谁做生成动作**
1. **把"不给答案"做成架构，而不是提示词。** Bastani 的 GPT Base 已经带了"当家教"的指令，仍然 −17%；Liu 2026 的默认值直接把整门课拖低 0.3 SD。→ 答案的可得性必须由**工具调用顺序/权限**决定（先交尝试 → 才解锁提示 → 二次失败才给解法），而不是 system prompt 里写"请不要直接回答"。
2. **区分"簿记动作"与"学习动作"。** 链接、去重、格式、一致性 → 交给 LLM；**用自己的话复述、预测、举例、找反例、引用原文** → 必须留给用户，且产品要能识别"这段是用户生成的还是 AI 生成的"（provenance 是一等字段）。
3. **每一条 wiki 主张都要能"被引用"。** MIT 的行为学探针（"你能不能引用自己刚写的那句"）可以直接产品化：对用户刚写的/刚确认的页面，隔一段时间问"这句话的原文/依据是什么"。**这比"你学会了吗"的自评有用一个数量级**。

**B. 度量问题：什么算学会了**
4. **学习证据只在 AI 关闭时采集**：闭卷自测、口述复述、写回 wiki 前先"凭记忆重建"一版再对照。**AI 开启时的准确率、停留时长、产物质量，都只能算使用指标**（Bastani +48%/+127% vs −17%；Strömberg +18% 作业分 vs −20% 月考）。
5. **"用时塌缩"作为 lint 项**：Strömberg 的判别器极其简单——**作业时间显著短于同类、分数异常高** = 外包。brainup 可以对标：某主题的"阅读→产出"时间比骤降、且引用密度下降 → 触发"认知债"提示。
6. **禁用自评作为成功指标**：学生自评学习感与实际负相关（Bastani）；AI 反馈的"感知"与"效果"不同向（g=−0.20 vs 0.25）。

**C. 教学设计问题：怎么让 AI 增强而不是替代**
7. **合意困难要显式设计**：先猜后看、间隔重现、交错主题、闭卷检索、生成性提问（"你会怎么反驳这一条"）。Learning Scientists 的四条同形曲线说明：**AI 带来的"顺"和 cramming 带来的"顺"是同一类假信号**。
8. **反馈按层级写，不按长度写**：process/self-regulation 级（"你这一步跳过了边界条件"）> task 级（"错了"）> self 级（"很棒"）。纯 AI 反馈会自然退化到表层（语法/措辞），这与保持期 −0.02 一致 → **深层反馈必须挂靠人定的评分细则或明确的学习目标**。
9. **在"犯错的那一刻"介入**：NUMI 的证据是 AI 的价值集中在"犯错后的下一次尝试"；Khanmigo 的失败在于"学生根本不问"。→ 产品应主动在错误点提问，而不是等用户开口。
10. **对新手更严格，而不是更宽松**：弱先验知识者在自由使用下受损最大（Lehmann、Liu）。"学习爱好者"进入新领域时就是新手 → 前期应**增加**脚手架与强制复述，而不是"让 AI 帮你快速建库"。

**D. 待验证（不要在 v0.2 当成事实写进设计）**
- LLM 自动生成的测验题/评分细则质量（Pardos：32% 提示不合格；Bastani：2023 年 GPT-4 只有 51% 正确率）→ 需要人审或答案库。
- "认知债"能否被可靠测量（目前只有间接代理：引用失败率、用时塌缩、迁移测验）。
- 长期（>6 个月）保持效应：现有 RCT 几乎全是即时后测；只有 Khanmigo（2 年，≈0）与 Strömberg（30 个月，负）够长。
- 中文语境/成人自学者：**没有任何一项 RCT 覆盖中国成人自主学习场景**——brainup 的目标用户群在证据上是空白，只能借方向，不能借数字。

---

## 16. 未解问题与后续检索线索

1. **Strömberg 的机制**：作业时间只降 5–6% 的总学习时间，却对应 20% 分数跌幅 → 课堂参与、注意、动机的渠道未被测量。
2. **"提示 vs 答案"的剂量曲线**：目前只有二分（hints / answers），不知道"第几次卡住给提示"最优。
3. **AI 辅助的"生成效应"能否被保留**：让学生先写、AI 只做对比反馈（而不是先看 AI 版本）——这是 brainup 最该自测的 A/B。
4. **社交/动机成分的占比**：2σ 里有多少是"有人在乎我"（Think Different 的假设），决定纯 AI 的天花板。
5. **检测工具不可用**：EDUCAUSE 2026 与 Bassett 2026 都指出 AI 检测器不可靠（"heads we win, tails you lose"），产品不应建立在检测上，而应建立在**过程证据**上。
6. 待补一手来源（本轮未打开全文）：Kumar et al. 2023（解释在尝试前/后的差异）、Barcaui 2025（45 天保持测验）、Sungu et al. 2026（AI 伤害教学）、Fütterer 2026 已读摘要级。

---

## 17. 参考清单（按主题）

**负面/机制**
- Kosmyna et al. 2025, arXiv:2506.08872 — https://arxiv.org/abs/2506.08872
- Bastani et al. 2025, PNAS 122(26):e2422633122 — https://www.pnas.org/doi/10.1073/pnas.2422633122
- Strömberg, Lei & Wu 2026, CEPR DP 21577 — https://cepr.org/publications/dp21577 ｜VoxEU https://cepr.org/voxeu/columns/generative-ai-learning-penalty-secondary-school
- Liu, Christian, Dumbalska, Bakker & Dubey 2026, arXiv:2604.04721 — https://ai-project-website.github.io/AI-assistance-reduces-persistence/
- Liu, J. et al. 2026, EdWorkingPaper 26-1598 — https://doi.org/10.26300/y3f8-vh05
- Gerlich 2025, Societies 15(1):6 — https://www.mdpi.com/2075-4698/15/1/6 ｜更正 https://doi.org/10.17605/osf.io/edb5y
- Lee et al. 2025, CHI '25 — https://www.microsoft.com/en-us/research/publication/the-impact-of-generative-ai-on-critical-thinking-self-reported-reductions-in-cognitive-effort-and-confidence-effects-from-a-survey-of-knowledge-workers/
- Fan et al. 2024, arXiv:2412.09315 — https://arxiv.org/abs/2412.09315
- Lehmann, Cornelius & Sting 2025, arXiv:2409.09047 — https://arxiv.org/abs/2409.09047
- Fütterer et al. 2026, Educ Psychol Rev 38 — https://doi.org/10.1007/s10648-026-10133-8

**正面/设计**
- Kestin et al. 2025, Sci Rep 15:17458 — https://doi.org/10.1038/s41598-025-97652-6
- StudentBench 2026, arXiv:2609.28470 — https://arxiv.org/abs/2609.28470
- De Simone et al. 2025, World Bank PRWP 11125 — https://openknowledge.worldbank.org/entities/publication/15e1ff08-15ae-4f7a-b2a8-d146e6c113ee
- Henkel et al. 2024, arXiv:2402.09809 — https://arxiv.org/abs/2402.09809
- Harrison et al. 2026, arXiv:2609.14789 — https://arxiv.org/abs/2609.14789
- LearnLM Team & Eedi 2025, arXiv:2512.23633 — https://arxiv.org/abs/2512.23633
- Wang et al. 2024/2026 (Tutor CoPilot), arXiv:2410.03017 — https://arxiv.org/abs/2410.03017
- Oreopoulos & Low 2026 (Khanmigo), EdWorkingPaper 26-1551 — https://doi.org/10.26300/kner-hv33
- Oreopoulos, Liut, Sungu & Low 2026 (NUMI), EdWorkingPaper 26-1552 — https://doi.org/10.26300/01qv-6c22
- Pardos & Bhandari 2024, PLOS ONE 19(5):e0304013 — https://doi.org/10.1371/journal.pone.0304013

**元分析**
- Nature HSSC 2026 (35 studies, g=0.670) — https://www.nature.com/articles/s41599-026-07019-z
- Frontiers Psychology 2026 (g=0.499, teaching method) — https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2026.1758670/full
- Frontiers Education 2026 (g=0.864, PET-PEESE 0.26–0.45) — https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2026.1971476/pdf
- Ma 2025, JCAL (0.68) — https://onlinelibrary.wiley.com/doi/10.1111/jcal.70117
- Gu & Yan 2025, JECR (teacher support 1.426 vs 0.077) — https://journals.sagepub.com/doi/10.1177/07356331251349620
- IRRODL 2026 (0.573; SRL 1.115) — https://doi.org/10.19173/irrodl.v27i1.8775
- Nature HSSC 2025 (51 studies; performance 0.867 / HOT 0.457) — https://www.nature.com/articles/s41599-025-04787-y
- CMU GAITAR 2026 (18 studies; tool use × transfer) — https://www.cmu.edu/teaching/gaitar/gaitaratscale/meta-analysis.html

**反馈**
- Hattie & Timperley 2007, RER 77(1):81–112 — https://journals.sagepub.com/doi/10.3102/003465430298487
- Wisniewski, Zierer & Hattie 2020, Front Psychol 10:3087 — https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2019.03087/full
- AI vs human feedback meta 2025 — https://www.tandfonline.com/doi/full/10.1080/01443410.2025.2553639
- AI writing feedback meta 2026 — https://www.tandfonline.com/doi/full/10.1080/2331186X.2026.2665494
- Algorithm-based feedback meta 2026 — https://doi.org/10.1016/j.asw.2026.101034
- AI personalized feedback meta 2025 — https://journals.sagepub.com/doi/10.1177/07356331251410020
- GAI formative feedback RCT 2025 — https://link.springer.com/article/10.1007/s10639-025-13778-0
- GenAI vs hybrid L2 feedback 2025 — https://www.tandfonline.com/doi/full/10.1080/17501229.2025.2503890

**2σ 与政策/共识**
- Education Next 2024-03 — https://www.educationnext.org/two-sigma-tutoring-separating-science-fiction-from-science-fact/
- Attridge 2026-03 — https://eliotattridge.com/two-sigma-problem/
- Fikr Ventures 2026-03 — https://www.fikrventures.com/blogs/retire-the-two-sigma
- EDUCAUSE Horizon 2026 — https://library.educause.edu/resources/2026/5/2026-educause-horizon-report-teaching-and-learning-edition
- Stanford SCALE 2026-08 — https://scale.stanford.edu/research-in-action/ai-tutoring-not-monolith
- Learning Scientists《Unwanted Ease》2026-08-21 — https://www.learningscientists.org/blog/2026/8/21
- Learning Scientists《130,000 Student Questions》2025-09-04 — https://www.learningscientists.org/blog/2025/9/4-1
- Learning Scientists《Premature Cognitive Offloading》2026-10-29 — https://www.learningscientists.org/blog/2026/10/29-1
- Nature 新闻（对 MIT 研究的批评）2025-06-25 — https://www.nature.com/articles/d41586-025-02005-y
