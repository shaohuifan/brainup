"""review：人审队列——编译计划审批与决策裁决的统一入口（P0/P1）。

原则：
- 计划在 .kb/plans/<id>.json 排队，人审批准才落盘（approve 即原子应用 + git commit）
- 审批以整个计划为单位呈现，但校验以动作为粒度逐条报错
- rejected 计划保留（append-only 精神：负面结果也是资产）
"""

from __future__ import annotations

import secrets
from datetime import UTC, datetime

from . import lint as lint_mod
from .actions import ActionError, Plan, PlanExecutor, parse_action, summarize_plan
from .vault import Vault, utcnow


def new_plan_id() -> str:
    stamp = datetime.now(UTC).strftime("%Y%m%d-%H%M%S")
    return f"P-{stamp}-{secrets.token_hex(2)}"


def submit_plan(vault: Vault, plan: Plan, validate: bool = True) -> Plan:
    """接收计划入队。validate=True 时先做封闭词表与引用核验（拒绝即不入队）。"""
    if validate:
        executor = PlanExecutor(vault)
        errors = executor.validate(plan)
        if errors:
            raise ActionError(f"计划被拒绝（{len(errors)} 项）：\n- " + "\n- ".join(errors))
    path = vault.plans_dir / f"{plan.plan_id}.json"
    if path.exists():
        raise ActionError(f"计划已存在：{plan.plan_id}")
    path.write_text(plan.model_dump_json(indent=2), encoding="utf-8")
    vault.git_commit(f"plan: 提交待审计划 {plan.plan_id}（{len(plan.actions)} 个动作）")
    return plan


def plan_from_actions_json(
    vault: Vault, actions: list[object], origin: str = "agent", source_id: str | None = None
) -> Plan:
    """从动作列表构造计划（MCP 提交路径）：逐条封闭词表解析。"""
    parsed = [parse_action(a) for a in actions]
    return Plan(
        plan_id=new_plan_id(),
        origin=origin,  # type: ignore[arg-type]
        source_id=source_id,
        created_at=utcnow(),
        actions=parsed,
    )


def list_plans(vault: Vault, status: str | None = None) -> list[Plan]:
    out: list[Plan] = []
    for path in sorted(vault.plans_dir.glob("*.json")):
        try:
            plan = Plan.model_validate_json(path.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001 - 损坏计划不阻塞队列
            continue
        if status is None or plan.status == status:
            out.append(plan)
    return out


def get_plan(vault: Vault, plan_id: str) -> Plan:
    path = vault.plans_dir / f"{plan_id}.json"
    if not path.is_file():
        raise ActionError(f"计划不存在：{plan_id}")
    return Plan.model_validate_json(path.read_text(encoding="utf-8"))


def save_plan(vault: Vault, plan: Plan) -> None:
    (vault.plans_dir / f"{plan.plan_id}.json").write_text(
        plan.model_dump_json(indent=2), encoding="utf-8"
    )


def approve_plan(vault: Vault, plan_id: str) -> Plan:
    """批准并原子应用。应用失败 → 状态 failed + 错误留档，不产生部分写入。"""
    plan = get_plan(vault, plan_id)
    if plan.status != "pending":
        raise ActionError(f"计划状态为 {plan.status}，不能批准")
    executor = PlanExecutor(vault)
    try:
        touched = executor.apply(plan)
    except ActionError as e:
        plan.status = "failed"
        plan.error = str(e)
        save_plan(vault, plan)
        raise
    plan.status = "applied"
    save_plan(vault, plan)
    vault.git_commit(f"review: 批准 {plan_id} → 写入 {len(touched)} 页")
    return plan


def reject_plan(vault: Vault, plan_id: str, reason: str) -> Plan:
    plan = get_plan(vault, plan_id)
    if plan.status != "pending":
        raise ActionError(f"计划状态为 {plan.status}，不能拒绝")
    plan.status = "rejected"
    plan.note = reason
    save_plan(vault, plan)
    vault.git_commit(f"review: 拒绝 {plan_id}（{reason}）")
    return plan


def review_summary(vault: Vault) -> dict[str, object]:
    plans = list_plans(vault)
    return {
        "pending_plans": [summarize_plan(p) for p in plans if p.status == "pending"],
        "open_decisions": [d.model_dump() for d in lint_mod.open_decisions(vault)],
        "recent_failed": [summarize_plan(p) for p in plans if p.status == "failed"][:5],
    }
