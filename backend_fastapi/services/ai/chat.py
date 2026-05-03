import time
from typing import Iterator, List, Optional

from services.ai.client import get_client
from services.ai.config import (
    DASHSCOPE_MODEL,
    MAX_RECENT_CHARS,
    MAX_RECENT_MESSAGES,
    MAX_RESPONSE_TOKENS,
)
from services.ai.memory import (
    get_history_messages,
    get_structured_memory,
    save_turn_to_memory,
)
from services.ai.prompts import RESPONSE_MODE_PROMPTS, SYSTEM_PROMPT
from services.ai.safety import (
    classify_user_state,
    detect_crisis_level,
    select_response_mode,
)
from services.ai.utils import safe_print


def trim_recent_messages(history_messages: List[dict]) -> List[dict]:
    trimmed = history_messages[-MAX_RECENT_MESSAGES:] if MAX_RECENT_MESSAGES > 0 else history_messages
    if MAX_RECENT_CHARS <= 0:
        return trimmed

    total_chars = 0
    kept: List[dict] = []
    for msg in reversed(trimmed):
        content = str(msg.get("content") or "")
        total_chars += len(content)
        if kept and total_chars > MAX_RECENT_CHARS:
            break
        kept.append(msg)
    kept.reverse()
    return kept


def build_context_note(extra_context: Optional[dict]) -> str:
    if not extra_context:
        return ""

    parts: List[str] = []
    emotion = extra_context.get("emotion")
    if emotion:
        parts.append(f"用户主情绪: {emotion}")

    tags = extra_context.get("tags") or []
    if isinstance(tags, list) and tags:
        parts.append("可能触发因素: " + " / ".join([str(x) for x in tags[:8]]))

    detail = extra_context.get("detail") or []
    if isinstance(detail, list) and detail:
        parts.append("细分感受: " + " / ".join([str(x) for x in detail[:8]]))

    content = extra_context.get("content")
    if content:
        parts.append(f"用户补充: {str(content)[:200]}")

    return "\n".join(parts)


def format_profile_for_prompt(profile: dict) -> str:
    sections = []
    mapping = {
        "core_concerns": "长期困扰",
        "triggers": "触发因素",
        "soothing_preferences": "有效安抚",
        "communication_preferences": "沟通偏好",
        "support_network": "支持网络",
        "risk_signals": "风险信号",
        "goals": "长期目标",
    }

    for key, title in mapping.items():
        values = profile.get(key) or []
        if values:
            sections.append(f"{title}: " + "，".join(values[:4]))

    summary = str(profile.get("summary") or "").strip()
    if summary:
        sections.append(f"长期画像: {summary}")

    return "\n".join(sections)


def build_chat_messages(
    user_message: str,
    user_id: Optional[int] = None,
    extra_context: Optional[dict] = None,
) -> List[dict]:
    user_state = classify_user_state(user_message)
    response_mode = select_response_mode(user_state)
    risk_level = detect_crisis_level(user_message)

    messages: List[dict] = [{"role": "system", "content": SYSTEM_PROMPT}]
    mode_prompt = RESPONSE_MODE_PROMPTS.get(response_mode)
    if mode_prompt:
        messages.append({"role": "system", "content": mode_prompt})

    messages.append(
        {
            "role": "system",
            "content": f"用户状态: {user_state}\n回复策略: {response_mode}\n风险等级: {risk_level}",
        }
    )

    if risk_level == "crisis":
        messages.append(
            {
                "role": "system",
                "content": "高风险场景：优先简短安全回应，建议立即联系现实支持和紧急援助。",
            }
        )

    context_note = build_context_note(extra_context)
    if context_note:
        messages.append({"role": "system", "content": f"补充上下文:\n{context_note}"})

    if user_id is not None:
        profile = get_structured_memory(user_id)
        profile_note = format_profile_for_prompt(profile)
        if profile_note:
            messages.append({"role": "system", "content": f"用户长期记忆:\n{profile_note}"})

        try:
            recent_messages = get_history_messages(user_id, limit=max(MAX_RECENT_MESSAGES, 1))
            messages.extend(trim_recent_messages(recent_messages))
        except Exception as exc:
            safe_print(f"[Load Recent History Warning] user_id={user_id}, err={exc}")

    messages.append({"role": "user", "content": user_message})
    return messages


def fallback_reply_for_empty_text() -> str:
    return "我在，想聊什么都可以。"


def fallback_reply_for_no_model() -> str:
    return "我在听你说。现在模型服务还没连上，但你可以继续说，我会尽量陪你。"


def fallback_reply_for_error() -> str:
    return "抱歉，我刚才有点卡住了。你愿意再说一遍吗？我会认真听。"


def chat_with_ai(
    user_message: str,
    user_id: Optional[int] = None,
    extra_context: Optional[dict] = None,
) -> str:
    started_at = time.perf_counter()
    text = (user_message or "").strip()
    if not text:
        return fallback_reply_for_empty_text()

    client = get_client()
    if client is None:
        return fallback_reply_for_no_model()

    messages = build_chat_messages(text, user_id=user_id, extra_context=extra_context)

    try:
        response = client.chat.completions.create(
            model=DASHSCOPE_MODEL,
            messages=messages,
            max_tokens=MAX_RESPONSE_TOKENS,
            temperature=0.7,
        )
        ai_reply = (response.choices[0].message.content or "").strip() or "嗯，我在。"
        save_turn_to_memory(user_id, text, ai_reply)

        elapsed_ms = int((time.perf_counter() - started_at) * 1000)
        safe_print(
            f"[AI Chat Timing] user_id={user_id}, context_count={max(len(messages) - 1, 0)}, "
            f"reply_len={len(ai_reply)}, elapsed_ms={elapsed_ms}"
        )
        return ai_reply
    except Exception as exc:
        safe_print(f"[AI Service Error] {exc}")
        return fallback_reply_for_error()


def stream_chat_with_ai(
    user_message: str,
    user_id: Optional[int] = None,
    extra_context: Optional[dict] = None,
    cancel_event=None,
) -> Iterator[str]:
    started_at = time.perf_counter()
    text = (user_message or "").strip()
    if not text:
        yield ""
        return

    client = get_client()
    if client is None:
        yield fallback_reply_for_no_model()
        return

    messages = build_chat_messages(text, user_id=user_id, extra_context=extra_context)
    ai_parts: List[str] = []
    first_chunk_ms: Optional[int] = None

    try:
        stream = client.chat.completions.create(
            model=DASHSCOPE_MODEL,
            messages=messages,
            max_tokens=MAX_RESPONSE_TOKENS,
            temperature=0.7,
            stream=True,
        )

        for chunk in stream:
            if cancel_event and cancel_event.is_set():
                safe_print(f"[AI Stream Cancelled] user_id={user_id}")
                break

            try:
                delta = chunk.choices[0].delta.content or ""
            except Exception:
                delta = ""

            if not delta:
                continue

            if first_chunk_ms is None:
                first_chunk_ms = int((time.perf_counter() - started_at) * 1000)
                safe_print(
                    f"[AI Stream First Chunk] user_id={user_id}, context_count={max(len(messages) - 1, 0)}, "
                    f"first_chunk_ms={first_chunk_ms}"
                )

            ai_parts.append(delta)
            yield delta
    except Exception as exc:
        safe_print(f"[AI Stream Error] {exc}")
        fallback = fallback_reply_for_error()
        ai_parts = [fallback]
        yield fallback

    ai_reply = "".join(ai_parts).strip() or "嗯，我在。"
    was_cancelled = bool(cancel_event and cancel_event.is_set())
    if not was_cancelled:
        save_turn_to_memory(user_id, text, ai_reply)

    elapsed_ms = int((time.perf_counter() - started_at) * 1000)
    safe_print(
        f"[AI Stream Timing] user_id={user_id}, context_count={max(len(messages) - 1, 0)}, "
        f"reply_len={len(ai_reply)}, first_chunk_ms={first_chunk_ms}, elapsed_ms={elapsed_ms}, "
        f"cancelled={was_cancelled}"
    )


_trim_recent_messages = trim_recent_messages
_build_context_note = build_context_note
_format_profile_for_prompt = format_profile_for_prompt
_build_chat_messages = build_chat_messages
_fallback_reply_for_empty_text = fallback_reply_for_empty_text
_fallback_reply_for_no_model = fallback_reply_for_no_model
_fallback_reply_for_error = fallback_reply_for_error
