# brainup · 升级大脑 🧠⬆️

> **读书人的复利知识库引擎** — 读过的每一本书，都变成往后可用的知识资产。

[English](#english) | 中文

## 这是什么

基于 [Karpathy 的 LLM Wiki 模式](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)构建的个人知识库工具：不做 RAG 式的"每次查询重新拼装"，而是让 LLM 把你读过的书、论文、文章**增量编译**成一个持久的、互相链接的 markdown wiki——知识编译一次、持续保鲜、随取随用。

```
你的书（PDF/EPUB/文章）→  brainup 编译  →  知识资产（概念卡/人物卡/主题页/分歧页）
        raw 不可变层      受约束的写路径     wiki append-only 声明层（人审队列把关）
```

**核心信念**（来自 30+ 一手来源的调研，见 [`research/`](research/README.md)）：
- 跨书连接是检索做不到的——"这本书和那本书在 X 上的分歧"编译时就已经存在于页面里
- 信任靠工程不靠自觉：封闭动作词表 + 逐字引用核验 + 人审队列
- 维护靠决策队列而非自动修复：每条死链/重复/矛盾都是一个可批量裁决的分诊决定
- 知识资产用 [OKF v0.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) 兼容格式存储——可携带，不锁死

## 快速开始

```bash
uv tool install brainup   # 或 uvx brainup
brainup status
```

> 当前为 v0.1 骨架阶段。设计已定稿（[design/design-proposal-v0.1.md](design/design-proposal-v0.1.md)），命令面逐步落地中。

## 命令面（v0.1 规划）

| 命令 | 行为 |
|---|---|
| `brainup init` | 脚手架 vault（中文默认，OKF v0.2 兼容） |
| `brainup ingest <src>` | 解析 → 入 raw → 编译计划 → **人审队列** → 原子应用 |
| `brainup query <q>` | 三级渐进披露 → FTS 兜底 → 引用作答 |
| `brainup lint` | 健康扫描 → **决策队列** |
| `brainup review` | 审批待定动作（action 粒度） |
| `brainup metrics` | 每查询 token / 命中率 / 决策吞吐 / 源页比 |

同时以 **MCP server** 形式把同一引擎暴露给 Claude Code / Codex / Cursor / OpenCode 等任意 agent 客户端。

## 模型接入（BYOK，全兼容）

OpenAI 兼容接口统一接入：DeepSeek / GLM / Qwen / Moonshot / OpenRouter / **Ollama 本地** / vLLM；另支持 Anthropic 原生。不绑定任何厂商，你的 key 你做主。小模型做路由决策，大模型做综合——省 token 且更准。

## 路线图

- **v0.1** 引擎 + CLI/MCP + 中文读书 schema（进行中）
- **v0.2** FSRS 复习卡、播客/视频源、行业研究模板
- **v0.3** GUI 桌面壳（引擎不动，服务普通用户）

## 许可证

[Apache-2.0](LICENSE)

## 致谢

- [Andrej Karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — LLM Wiki 模式
- [Vannevar Bush](https://en.wikipedia.org/wiki/Memex) — Memex (1945)

---

## English

**brainup** is a compounding knowledge-base engine for readers, built on [Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f): instead of re-deriving answers from raw documents at query time (RAG), an LLM incrementally compiles what you read into a persistent, interlinked markdown wiki. CLI + MCP; BYOK model access (any OpenAI-compatible endpoint or Anthropic); OKF v0.2-compatible vaults you own in git. Chinese-first, English-friendly. Pre-alpha — see the [design doc](design/design-proposal-v0.1.md).
