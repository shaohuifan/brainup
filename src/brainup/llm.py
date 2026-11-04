"""llm：BYOK 模型接入（全兼容，不绑厂商）。

- OpenAI-compat 统一接口：DeepSeek / GLM / Qwen / Moonshot / OpenRouter / Ollama 本地 / vLLM
- Anthropic 原生消息接口
- API key 只从环境变量读取（配置文件永不存储密钥）
- 小模型路由（decision）+ 大模型（synthesis）：省 token 且更准（crow-hq 实证）
"""

from __future__ import annotations

import json
import os
import tomllib
from dataclasses import dataclass

import httpx

from .vault import Vault


class LLMError(Exception):
    """模型调用失败。"""


@dataclass
class LLMResult:
    text: str
    tokens: int


class LLMClient:
    """极薄客户端：chat_text / chat_json 两个方法，便于测试打桩。"""

    def __init__(self, config: dict[str, str]) -> None:
        self.provider = config.get("provider", "openai-compat")
        self.base_url = (config.get("base_url") or "").rstrip("/")
        self.model = config.get("model") or ""
        self.small_model = config.get("small_model") or self.model
        self.api_key_env = config.get("api_key_env", "BRAINUP_API_KEY")
        if self.provider not in ("openai-compat", "anthropic"):
            raise LLMError(f"不支持的 provider：{self.provider}")
        if self.provider == "openai-compat" and not self.base_url:
            raise LLMError("openai-compat 需要 base_url（如 https://api.deepseek.com/v1）")
        if not self.model:
            raise LLMError("config.toml 缺少 model")

    @property
    def api_key(self) -> str:
        return os.environ.get(self.api_key_env, "")

    # ---------- 对外接口 ----------
    def chat_text(
        self, messages: list[dict[str, str]], model: str | None = None
    ) -> LLMResult:
        return self._chat(messages, model or self.model)

    def chat_json(
        self, messages: list[dict[str, str]], model: str | None = None
    ) -> tuple[object, int]:
        result = self._chat(messages, model or self.small_model)
        try:
            return _parse_json(result.text), result.tokens
        except json.JSONDecodeError as e:
            raise LLMError(f"模型输出不是合法 JSON：{e}\n{result.text[:500]}") from e

    # ---------- 内部 ----------
    def _chat(self, messages: list[dict[str, str]], model: str) -> LLMResult:
        if self.provider == "anthropic":
            return self._chat_anthropic(messages, model)
        return self._chat_openai_compat(messages, model)

    def _chat_openai_compat(self, messages: list[dict[str, str]], model: str) -> LLMResult:
        if not self.api_key:
            raise LLMError(f"缺少 API key：请设置环境变量 {self.api_key_env}")
        resp = httpx.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"model": model, "messages": messages},
            timeout=120.0,
        )
        if resp.status_code != 200:
            raise LLMError(f"API {resp.status_code}：{resp.text[:300]}")
        data = resp.json()
        text = data["choices"][0]["message"]["content"] or ""
        tokens = int(data.get("usage", {}).get("total_tokens", 0))
        return LLMResult(text, tokens)

    def _chat_anthropic(self, messages: list[dict[str, str]], model: str) -> LLMResult:
        if not self.api_key:
            raise LLMError(f"缺少 API key：请设置环境变量 {self.api_key_env}")
        system = "\n".join(m["content"] for m in messages if m["role"] == "system")
        msgs = [m for m in messages if m["role"] != "system"]
        resp = httpx.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
            },
            json={
                "model": model,
                "max_tokens": 4096,
                "system": system or None,
                "messages": msgs,
            },
            timeout=120.0,
        )
        if resp.status_code != 200:
            raise LLMError(f"API {resp.status_code}：{resp.text[:300]}")
        data = resp.json()
        text = "".join(b.get("text", "") for b in data.get("content", []))
        tokens = int(data.get("usage", {}).get("input_tokens", 0)) + int(
            data.get("usage", {}).get("output_tokens", 0)
        )
        return LLMResult(text, tokens)


def load_llm_config(vault: Vault) -> dict[str, str]:
    path = vault.kb / "config.toml"
    if not path.is_file():
        return {}
    with path.open("rb") as f:
        data = tomllib.load(f)
    return {k: str(v) for k, v in data.get("llm", {}).items()}


def load_llm(vault: Vault) -> LLMClient | None:
    """返回配置好的客户端；provider=none 或配置不全时返回 None（纯检索模式）。"""
    config = load_llm_config(vault)
    if config.get("provider", "none") == "none":
        return None
    try:
        return LLMClient(config)
    except LLMError:
        return None


def _parse_json(text: str) -> object:
    """容错解析：剥掉 markdown 代码围栏。"""
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = stripped.split("\n", 1)[1] if "\n" in stripped else stripped
        if stripped.endswith("```"):
            stripped = stripped[: -3]
    return json.loads(stripped)
