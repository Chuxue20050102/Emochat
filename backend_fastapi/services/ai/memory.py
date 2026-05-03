import json
import threading
from datetime import datetime, timezone
from typing import Dict, List, Optional

import redis
from langchain_classic.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import RedisChatMessageHistory

from services.ai.client import get_client
from services.ai.config import (
    DASHSCOPE_MODEL,
    MEMORY_EXPIRY,
    MEMORY_PREFIX,
    MEMORY_SUMMARY_TRIGGER,
    PROFILE_PREFIX,
    PROFILE_REFRESH_TRIGGER,
    REDIS_DB,
    REDIS_HOST,
    REDIS_PORT,
    REDIS_URL,
    SUMMARY_PREFIX,
)
from services.ai.prompts import MEMORY_PROFILE_PROMPT
from services.ai.safety import detect_crisis
from services.ai.utils import llm_json_parse, safe_print

_redis_client: Optional[redis.Redis] = None
_memories: Dict[int, ConversationBufferMemory] = {}
_memories_lock = threading.Lock()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def get_redis_client() -> redis.Redis:
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            decode_responses=True,
        )
    return _redis_client


def get_chat_message_history(user_id: int) -> RedisChatMessageHistory:
    session_id = f"{MEMORY_PREFIX}{user_id}"
    try:
        return RedisChatMessageHistory(
            session_id=session_id,
            redis_client=get_redis_client(),
            ttl=MEMORY_EXPIRY,
        )
    except TypeError:
        return RedisChatMessageHistory(
            session_id=session_id,
            url=REDIS_URL,
            ttl=MEMORY_EXPIRY,
        )


def get_memory(user_id: int) -> ConversationBufferMemory:
    with _memories_lock:
        if user_id in _memories:
            return _memories[user_id]

        try:
            memory = ConversationBufferMemory(
                chat_memory=get_chat_message_history(user_id),
                return_messages=True,
                output_key="output",
                input_key="input",
            )
        except Exception as exc:
            safe_print(f"[Memory Init Warning] user_id={user_id}, fallback=in-memory, err={exc}")
            memory = ConversationBufferMemory(
                return_messages=True,
                output_key="output",
                input_key="input",
            )

        _memories[user_id] = memory
        return memory


def get_history_messages(user_id: int, limit: int = 50) -> List[dict]:
    memory = get_memory(user_id)
    raw_messages = list(getattr(memory.chat_memory, "messages", []) or [])
    if limit > 0:
        raw_messages = raw_messages[-limit:]

    messages: List[dict] = []
    for msg in raw_messages:
        msg_type = getattr(msg, "type", "")
        if msg_type == "human":
            messages.append({"role": "user", "content": msg.content})
        elif msg_type == "ai":
            messages.append({"role": "assistant", "content": msg.content})
    return messages


def empty_profile() -> dict:
    return {
        "core_concerns": [],
        "triggers": [],
        "soothing_preferences": [],
        "communication_preferences": [],
        "support_network": [],
        "risk_signals": [],
        "goals": [],
        "summary": "",
        "updated_at": utc_now(),
        "version": 1,
    }


def normalize_profile(profile: dict) -> dict:
    base = empty_profile()
    base.update(profile or {})
    for key in (
        "core_concerns",
        "triggers",
        "soothing_preferences",
        "communication_preferences",
        "support_network",
        "risk_signals",
        "goals",
    ):
        values = base.get(key) or []
        if not isinstance(values, list):
            values = [str(values)]
        cleaned: List[str] = []
        for x in values:
            item = str(x).strip()
            if item and item not in cleaned:
                cleaned.append(item)
        base[key] = cleaned[:6]

    base["summary"] = str(base.get("summary") or "").strip()[:120]
    base["updated_at"] = utc_now()
    base["version"] = 1
    return base


def get_structured_memory(user_id: int) -> dict:
    try:
        raw = get_redis_client().get(f"{PROFILE_PREFIX}{user_id}")
        if not raw:
            return empty_profile()
        parsed = json.loads(raw)
        if isinstance(parsed, dict):
            return normalize_profile(parsed)
    except Exception as exc:
        safe_print(f"[Load Profile Warning] user_id={user_id}, err={exc}")
    return empty_profile()


def save_structured_memory(user_id: int, profile: dict) -> None:
    try:
        normalized = normalize_profile(profile)
        get_redis_client().setex(
            f"{PROFILE_PREFIX}{user_id}",
            MEMORY_EXPIRY,
            json.dumps(normalized, ensure_ascii=False),
        )
        summary = normalized.get("summary") or ""
        if summary:
            get_redis_client().setex(f"{SUMMARY_PREFIX}{user_id}", MEMORY_EXPIRY, summary[:400])
    except Exception as exc:
        safe_print(f"[Save Profile Warning] user_id={user_id}, err={exc}")


def clear_memory(user_id: int) -> None:
    try:
        get_chat_message_history(user_id).clear()
    except Exception as exc:
        safe_print(f"[Clear Redis Memory Warning] user_id={user_id}, err={exc}")

    try:
        get_redis_client().delete(f"{SUMMARY_PREFIX}{user_id}")
        get_redis_client().delete(f"{PROFILE_PREFIX}{user_id}")
    except Exception as exc:
        safe_print(f"[Clear Profile Warning] user_id={user_id}, err={exc}")

    with _memories_lock:
        memory = _memories.pop(user_id, None)
    if memory:
        try:
            memory.clear()
        except Exception:
            pass


def get_memory_summary(user_id: int) -> str:
    profile = get_structured_memory(user_id)
    summary = str(profile.get("summary") or "").strip()
    if summary:
        return summary

    try:
        return (get_redis_client().get(f"{SUMMARY_PREFIX}{user_id}") or "").strip()
    except Exception as exc:
        safe_print(f"[Load Summary Warning] user_id={user_id}, err={exc}")
        return ""


def fallback_profile(previous_profile: dict, recent_messages: List[dict]) -> dict:
    profile = normalize_profile(previous_profile)
    user_text = "\n".join(
        [str(m.get("content") or "") for m in recent_messages if m.get("role") == "user"]
    )[-1800:]

    if not user_text:
        return profile

    if any(k in user_text for k in ["建议", "别讲道理", "别分析", "听我说"]):
        profile["communication_preferences"] = list(
            dict.fromkeys(profile["communication_preferences"] + ["更希望被倾听，少建议"])
        )[:6]
    if any(k in user_text for k in ["工作", "加班", "绩效", "同事", "领导"]):
        profile["core_concerns"] = list(dict.fromkeys(profile["core_concerns"] + ["工作压力"]))[:6]
    if any(k in user_text for k in ["家庭", "父母", "伴侣", "关系"]):
        profile["core_concerns"] = list(dict.fromkeys(profile["core_concerns"] + ["关系压力"]))[:6]
    if any(k in user_text for k in ["睡不着", "失眠", "焦虑", "心慌"]):
        profile["triggers"] = list(dict.fromkeys(profile["triggers"] + ["焦虑与睡眠问题"]))[:6]
    if detect_crisis(user_text):
        profile["risk_signals"] = list(dict.fromkeys(profile["risk_signals"] + ["出现自伤或绝望表达"]))[:6]
    if not profile.get("summary"):
        profile["summary"] = "用户在情绪波动时更需要被倾听和稳定支持。"

    return normalize_profile(profile)


def update_structured_memory(previous_profile: dict, recent_messages: List[dict]) -> dict:
    compact_text = "\n".join(
        [f"{m.get('role', 'user')}: {m.get('content', '')}" for m in recent_messages if m.get("content")]
    )[-2200:]

    if not compact_text:
        return normalize_profile(previous_profile)

    client = get_client()
    if client is None:
        return fallback_profile(previous_profile, recent_messages)

    try:
        response = client.chat.completions.create(
            model=DASHSCOPE_MODEL,
            temperature=0.2,
            max_tokens=420,
            messages=[
                {"role": "system", "content": MEMORY_PROFILE_PROMPT},
                {
                    "role": "user",
                    "content": (
                        f"已有记忆:\n{json.dumps(previous_profile, ensure_ascii=False)}\n\n"
                        f"最近对话:\n{compact_text}"
                    ),
                },
            ],
        )
        raw = response.choices[0].message.content or ""
        parsed = llm_json_parse(raw)
        if parsed:
            return normalize_profile(parsed)
    except Exception as exc:
        safe_print(f"[Profile Update Warning] err={exc}")

    return fallback_profile(previous_profile, recent_messages)


def refresh_structured_memory(user_id: int) -> None:
    try:
        history_messages = get_history_messages(user_id, limit=max(MEMORY_SUMMARY_TRIGGER, 1))
        if len(history_messages) < PROFILE_REFRESH_TRIGGER:
            return
        previous_profile = get_structured_memory(user_id)
        new_profile = update_structured_memory(previous_profile, history_messages)
        save_structured_memory(user_id, new_profile)
    except Exception as exc:
        safe_print(f"[Refresh Profile Warning] user_id={user_id}, err={exc}")


def schedule_memory_summary_update(user_id: Optional[int]) -> None:
    if user_id is None:
        return
    threading.Thread(target=refresh_structured_memory, args=(user_id,), daemon=True).start()


def save_turn_to_memory(user_id: Optional[int], user_message: str, ai_reply: str) -> None:
    if user_id is None:
        return

    try:
        memory = get_memory(user_id)
        memory.save_context({"input": user_message}, {"output": ai_reply})
    except Exception as exc:
        safe_print(f"[Memory Save Warning] user_id={user_id}, err={exc}")
        return

    schedule_memory_summary_update(user_id)


# Backward-compatible private aliases.
_get_redis_client = get_redis_client
_empty_profile = empty_profile
_normalize_profile = normalize_profile
_save_structured_memory = save_structured_memory
_fallback_profile = fallback_profile
_update_structured_memory = update_structured_memory
_refresh_structured_memory = refresh_structured_memory
_save_turn_to_memory = save_turn_to_memory
