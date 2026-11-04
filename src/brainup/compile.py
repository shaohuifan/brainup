"""compile：用 LLM 从来源生成编译计划（ingest --auto 路径）。

职责边界：
- 小模型路由（分类决策）在 llm.LLMClient.chat_json 中体现
- 本模块只负责：extract 全文 + 页面目录 + 动作词表 schema → 计划 JSON → Plan 校验
- 计划永远进入人审队列（review.submit_plan），绝不直接落盘
"""

from __future__ import annotations

from . import review
from .actions import ActionError, Plan
from .llm import LLMClient, LLMError
from .vault import Vault

_ACTION_SCHEMA = """\
可用动作（封闭词表，只允许以下五种 type，字段必须精确匹配）：

1. create_page — 新建页面。
   字段：type, page_type(concept|person|work|chapter|topic|disagreement|review),
   slug(文件名，中文可用，不含路径分隔符), title, summary(4-200字一句话)
   ⚠️ 页面已存在时禁止使用（扩展而非新建）。
2. add_claim — 向页面添加一条声明。字段：type, page_slug, text(4-600字),
   citation{source_id, quote(从来源逐字摘录 8-300 字符，一字不差), start_line, end_line}
   ⚠️ quote 必须是 extract 文本 L{start_line}-L{end_line} 区间内的连续原文，工具会逐字核验。
3. revise_claim — 修订声明。字段：type, page_slug, claim_id(如 C1), new_text, citation(可选)
4. deprecate_claim — 弃用声明（不删除）。字段：type, page_slug, claim_id, reason
5. link_pages — 建立关联。字段：type, from_slug, to_slug, note(可选)

规则：
- 只输出 JSON 对象：{"actions": [ ... ]}
- 每条声明必须携带引用；来源没有的内容不要写
- 与已有页面冲突的观点 → revise_claim/deprecate_claim 或写分歧，禁止静默覆盖
- 页面目录中已有相关页 → 优先 add_claim 到既有页面"""

_COMPLE_SYSTEM = (
    "你是知识库的编译器。你把来源文本编译为结构化声明：忠实、逐字引用、不做发明。"
    "你没有直接写文件的权力——你只产出计划，人审后由执行器落盘。"
)


def build_plan_for_source(
    vault: Vault, source_id: str, llm: LLMClient, max_chars: int = 24000
) -> Plan:
    """为一个已 ingest 的来源生成编译计划（入人审队列）。"""
    extract_path = vault.extract_dir / f"{source_id}.md"
    if not extract_path.is_file():
        raise ActionError(f"来源未 ingest：{source_id}")
    extract = extract_path.read_text(encoding="utf-8")
    if len(extract) > max_chars:
        extract = extract[:max_chars] + "\n…（超长截断，请只编译前文）"

    registry: dict[str, dict] = vault.load_json("sources.json", {})
    title = str(registry.get(source_id, {}).get("title", source_id))
    cat = vault.list_pages()
    catalog_text = (
        "\n".join(f"- {p['slug']}（{p['type']}）：{p['summary']}" for p in cat) or "（暂无页面）"
    )

    plan_obj, _tokens = llm.chat_json(
        [
            {"role": "system", "content": _COMPLE_SYSTEM + "\n\n" + _ACTION_SCHEMA},
            {
                "role": "user",
                "content": (
                    f"来源 ID：{source_id}\n来源标题：{title}\n\n"
                    f"## 已有页面目录\n{catalog_text}\n\n"
                    f"## 来源全文（行号即引用锚点）\n{extract}\n\n"
                    "编译这个来源。输出 JSON。"
                ),
            },
        ],
        model=llm.model,  # 综合用大模型
    )
    if not isinstance(plan_obj, dict) or not isinstance(plan_obj.get("actions"), list):
        raise LLMError(f"模型输出不是计划结构：{str(plan_obj)[:300]}")

    plan = review.plan_from_actions_json(
        vault, plan_obj["actions"], origin="ingest", source_id=source_id
    )
    return plan
