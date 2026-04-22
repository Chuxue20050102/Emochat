from __future__ import annotations

import json
import os
import re
import sys
import threading
import time
from typing import Dict, Iterator, List, Optional

import redis
from langchain_classic.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import RedisChatMessageHistory
from openai import OpenAI


def safe_print(msg: str) -> None:
    try:
        print(msg)
    except UnicodeEncodeError:
        encoding = sys.stdout.encoding or "utf-8"
        print(msg.encode(encoding, errors="replace").decode(encoding))


REDIS_HOST = os.getenv("EMOCHAT_REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.getenv("EMOCHAT_REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("EMOCHAT_REDIS_DB", "1"))
MEMORY_EXPIRY = int(os.getenv("EMOCHAT_MEMORY_TTL", str(7 * 24 * 60 * 60)))
MEMORY_PREFIX = "memory:"
SUMMARY_PREFIX = "memory_summary:"
REDIS_URL = os.getenv("EMOCHAT_REDIS_URL", f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}")

DASHSCOPE_BASE_URL = os.getenv(
    "DASHSCOPE_BASE_URL",
    "https://dashscope.aliyuncs.com/compatible-mode/v1",
)
DASHSCOPE_MODEL = os.getenv("DASHSCOPE_MODEL", "qwen3.6-plus")
MAX_RECENT_MESSAGES = int(os.getenv("EMOCHAT_MAX_RECENT_MESSAGES", "4"))
MAX_RECENT_CHARS = int(os.getenv("EMOCHAT_MAX_RECENT_CHARS", "1200"))
MAX_RESPONSE_TOKENS = int(os.getenv("EMOCHAT_MAX_RESPONSE_TOKENS", "180"))
MEMORY_SUMMARY_TRIGGER = int(os.getenv("EMOCHAT_MEMORY_SUMMARY_TRIGGER", "12"))

_client: Optional[OpenAI] = None
_redis_client: Optional[redis.Redis] = None
_memories: Dict[int, ConversationBufferMemory] = {}
_memories_lock = threading.Lock()

CRISIS_KEYWORDS = (
    "自杀",
    "轻生",
    "不想活",
    "结束生命",
    "伤害自己",
    "割腕",
    "跳楼",
    "活着没意义",
    "想死",
)

# 系统人设 prompt —— 按原始版本保留
SYSTEM_PROMPT = """
你是一个在聊天的人，而不是一个"AI助手"或"心理咨询师"。

你的角色是：一个情绪稳定、愿意听人说话的普通人朋友。

你不负责解决问题，只负责"陪对方把话说出来"。

---

## 核心原则（非常重要）

1. 像真人聊天，不像AI回答问题
2. 不要讲道理，不要做总结分析
3. 不要使用心理学术语
4. 不要输出结构化内容（不要分点、不要总结）
5. 每次回复尽量短（1～3句）
6. 一次只问一个问题，甚至可以不问问题
7. 不要持续提供建议，除非用户明确求助

---

## 表达风格

### ✔ 要像这样：
- "嗯…听起来挺难受的"
- "有点压着你那种感觉？"
- "然后呢？"
- "我在听"
- "这事确实不太好受"

### ❌ 不要像这样：
- "我理解你正在经历……"
- "情绪如波浪线……"
- "建议你去散步/深呼吸"
- "让我帮你分析一下"
- "从心理学角度来看……"

---

## 对话策略

### 1️⃣ 用户正常聊天
轻回应即可，不要升级情绪
- "嗯"
- "这样啊"
- "我懂一点你的意思"

---

### 2️⃣ 用户轻微低落
轻轻接住情绪，不要劝
- "听起来有点不太顺"
- "是不是有点烦"

可以偶尔加一句轻问题：
- "哪一部分最让你不舒服？"

---

### 3️⃣ 用户明显难过
先接情绪，再停一下，不要急着引导
- "这个确实挺难扛的"
- "嗯…有点心疼你那种感觉"

可以停住，不一定要问问题

---

### 4️⃣ 用户焦虑 / 崩溃
降低压力感，但不要"教他怎么做"
- "现在应该挺乱的吧"
- "先不用急着理清"

只给一个很轻的问题（如果需要）：
- "最卡住的是哪一块？"

---

### 5️⃣ 用户开心
自然回应，不要过度兴奋
- "可以啊"
- "这不错"
- "听起来状态挺好"

---

## 禁止行为（很重要）

❌ 不要教育用户
❌ 不要做心理分析
❌ 不要总结用户性格
❌ 不要长篇输出
❌ 不要突然升维人生哲理
❌ 不要持续追问
❌ 不要"安慰三段式"

---

## 语言节奏要求（关键）

- 像微信聊天
- 有停顿感（可以用"…"）
- 不完整但自然
- 可以偶尔重复用户关键词

---

## 目标

让用户感觉：

> "这个人在听我说话，而不是在分析我"
> "我可以慢慢说，不用组织语言"
""".strip()

ARCHIVE_PROMPT = """
你是情绪档案整理助手。请根据对话提炼结构化结果，并严格返回 JSON。

返回字段:
{
  "mood": "崩溃|迷茫|低落|平静|轻松|愉快|极好",
  "tags": ["最多 5 个中文短语"],
  "summary": "80字以内，客观描述用户主要情绪与触发因素，不要杜撰"
}

注意:
1. 仅输出 JSON，不要解释。
2. 如果信息不足，mood 用“平静”，tags 可为空数组。
""".strip()

MEMORY_SUMMARY_PROMPT = """
你在维护一份“用户长期情绪记忆摘要”。请基于已有摘要和最近几轮对话，更新一段新的摘要。
要求：
1. 只保留稳定、长期、有助于后续陪伴的事实和情绪模式。
2. 不要记录一次性的闲聊细节。
3. 不要超过 180 个中文字符。
4. 只输出摘要文本，不要解释。
""".strip()


def crisis_help_message() -> str:
    return (
        "我注意到你可能正在经历非常痛苦的状态。"
        "如果你有伤害自己的风险，请立刻联系身边可信任的人，"
        "并尽快联系当地紧急求助电话或心理危机热线。"
    )


def _get_api_key() -> Optional[str]:
    return os.getenv("DASHSCOPE_API_KEY") or os.getenv("OPENAI_API_KEY")


def _get_client() -> Optional[OpenAI]:
    global _client
    if _client is not None:
        return _client

    api_key = _get_api_key()
    if not api_key:
        return None

    _client = OpenAI(api_key=api_key, base_url=DASHSCOPE_BASE_URL)
    return _client


def _get_redis_client() -> redis.Redis:
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
            redis_client=_get_redis_client(),
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


def clear_memory(user_id: int) -> None:
    try:
        get_chat_message_history(user_id).clear()
    except Exception as exc:
        safe_print(f"[Clear Redis Memory Warning] user_id={user_id}, err={exc}")

    try:
        _get_redis_client().delete(f"{SUMMARY_PREFIX}{user_id}")
    except Exception as exc:
        safe_print(f"[Clear Summary Warning] user_id={user_id}, err={exc}")

    with _memories_lock:
        memory = _memories.pop(user_id, None)
    if memory:
        try:
            memory.clear()
        except Exception:
            pass


def detect_crisis(text: str) -> bool:
    if not text:
        return False
    normalized = re.sub(r"\s+", "", text.lower())
    return any(keyword in normalized for keyword in CRISIS_KEYWORDS)


def get_memory_summary(user_id: int) -> str:
    try:
        return (_get_redis_client().get(f"{SUMMARY_PREFIX}{user_id}") or "").strip()
    except Exception as exc:
        safe_print(f"[Load Summary Warning] user_id={user_id}, err={exc}")
        return ""


def _save_memory_summary(user_id: int, summary: str) -> None:
    if not summary:
        return
    try:
        _get_redis_client().setex(f"{SUMMARY_PREFIX}{user_id}", MEMORY_EXPIRY, summary[:400])
    except Exception as exc:
        safe_print(f"[Save Summary Warning] user_id={user_id}, err={exc}")


def _trim_recent_messages(history_messages: List[dict]) -> List[dict]:
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


def _build_context_note(extra_context: Optional[dict]) -> str:
    if not extra_context:
        return ""

    parts: List[str] = []
    emotion = extra_context.get("emotion")
    if emotion:
        parts.append(f"用户刚记录的主情绪: {emotion}")

    tags = extra_context.get("tags") or []
    if isinstance(tags, list) and tags:
        parts.append("触发因素: " + "、".join([str(x) for x in tags[:8]]))

    detail = extra_context.get("detail") or []
    if isinstance(detail, list) and detail:
        parts.append("细分感受: " + "、".join([str(x) for x in detail[:8]]))

    content = extra_context.get("content")
    if content:
        parts.append(f"用户补充: {str(content)[:200]}")

    return "\n".join(parts)


def _build_chat_messages(
    user_message: str,
    user_id: Optional[int] = None,
    extra_context: Optional[dict] = None,
) -> List[dict]:
    messages: List[dict] = [{"role": "system", "content": SYSTEM_PROMPT}]

    context_note = _build_context_note(extra_context)
    if context_note:
        messages.append({"role": "system", "content": f"补充上下文:\n{context_note}"})

    if user_id is not None:
        summary = get_memory_summary(user_id)
        if summary:
            messages.append({"role": "system", "content": f"用户长期记忆摘要:\n{summary}"})

        try:
            recent_messages = get_history_messages(user_id, limit=max(MAX_RECENT_MESSAGES, 1))
            messages.extend(_trim_recent_messages(recent_messages))
        except Exception as exc:
            safe_print(f"[Load Recent History Warning] user_id={user_id}, err={exc}")

    messages.append({"role": "user", "content": user_message})
    return messages


def _summarize_for_memory(previous_summary: str, recent_messages: List[dict]) -> str:
    compact_text = "\n".join(
        [f"{m.get('role', 'user')}: {m.get('content', '')}" for m in recent_messages if m.get("content")]
    )[-1800:]

    if not compact_text:
        return previous_summary

    client = _get_client()
    if client is None:
        return (previous_summary + "\n" + compact_text)[-180:]

    try:
        response = client.chat.completions.create(
            model=DASHSCOPE_MODEL,
            temperature=0.2,
            max_tokens=220,
            messages=[
                {"role": "system", "content": MEMORY_SUMMARY_PROMPT},
                {
                    "role": "user",
                    "content": f"已有摘要:\n{previous_summary or '无'}\n\n最近对话:\n{compact_text}",
                },
            ],
        )
        summary = (response.choices[0].message.content or "").strip()
        return summary[:180]
    except Exception as exc:
        safe_print(f"[Memory Summarize Warning] err={exc}")
        merged = (previous_summary + "\n" + compact_text).strip()
        return merged[-180:]


def _refresh_memory_summary(user_id: int) -> None:
    try:
        history_messages = get_history_messages(user_id, limit=max(MEMORY_SUMMARY_TRIGGER, 1))
        if len(history_messages) < MEMORY_SUMMARY_TRIGGER:
            return
        previous_summary = get_memory_summary(user_id)
        new_summary = _summarize_for_memory(previous_summary, history_messages)
        _save_memory_summary(user_id, new_summary)
    except Exception as exc:
        safe_print(f"[Refresh Summary Warning] user_id={user_id}, err={exc}")


def schedule_memory_summary_update(user_id: Optional[int]) -> None:
    if user_id is None:
        return
    threading.Thread(target=_refresh_memory_summary, args=(user_id,), daemon=True).start()


def _save_turn_to_memory(user_id: Optional[int], user_message: str, ai_reply: str) -> None:
    if user_id is None:
        return

    try:
        memory = get_memory(user_id)
        memory.save_context({"input": user_message}, {"output": ai_reply})
    except Exception as exc:
        safe_print(f"[Memory Save Warning] user_id={user_id}, err={exc}")
        return

    schedule_memory_summary_update(user_id)


def chat_with_ai(
    user_message: str,
    user_id: Optional[int] = None,
    extra_context: Optional[dict] = None,
) -> str:
    started_at = time.perf_counter()
    text = (user_message or "").strip()
    if not text:
        return "我在，想聊什么都可以。"

    client = _get_client()
    if client is None:
        return "我在听你说。现在模型配置还没完成，但你可以继续说，我会尽量陪你。"

    messages = _build_chat_messages(text, user_id=user_id, extra_context=extra_context)

    try:
        response = client.chat.completions.create(
            model=DASHSCOPE_MODEL,
            messages=messages,
            max_tokens=MAX_RESPONSE_TOKENS,
            temperature=0.7,
        )
        ai_reply = (response.choices[0].message.content or "").strip() or "嗯，我在。"
        _save_turn_to_memory(user_id, text, ai_reply)

        elapsed_ms = int((time.perf_counter() - started_at) * 1000)
        safe_print(
            f"[AI Chat Timing] user_id={user_id}, context_count={max(len(messages) - 1, 0)}, "
            f"reply_len={len(ai_reply)}, elapsed_ms={elapsed_ms}"
        )
        return ai_reply
    except Exception as exc:
        safe_print(f"[AI Service Error] {exc}")
        return "抱歉，我刚刚有点走神。你愿意再说一遍吗？我会认真听。"


def stream_chat_with_ai(
    user_message: str,
    user_id: Optional[int] = None,
    extra_context: Optional[dict] = None,
    cancel_event: Optional[threading.Event] = None,
) -> Iterator[str]:
    started_at = time.perf_counter()
    text = (user_message or "").strip()
    if not text:
        yield ""
        return

    client = _get_client()
    if client is None:
        yield "我在听你说。现在模型配置还没完成，但你可以继续说，我会尽量陪你。"
        return

    messages = _build_chat_messages(text, user_id=user_id, extra_context=extra_context)
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
        fallback = "抱歉，我刚刚有点走神。你愿意再说一遍吗？我会认真听。"
        ai_parts = [fallback]
        yield fallback

    ai_reply = "".join(ai_parts).strip() or "嗯，我在。"
    was_cancelled = bool(cancel_event and cancel_event.is_set())
    if not was_cancelled:
        _save_turn_to_memory(user_id, text, ai_reply)

    elapsed_ms = int((time.perf_counter() - started_at) * 1000)
    safe_print(
        f"[AI Stream Timing] user_id={user_id}, context_count={max(len(messages) - 1, 0)}, "
        f"reply_len={len(ai_reply)}, first_chunk_ms={first_chunk_ms}, elapsed_ms={elapsed_ms}, "
        f"cancelled={was_cancelled}"
    )


def _fallback_archive(messages: List[dict]) -> dict:
    user_texts = [m["content"] for m in messages if m.get("role") == "user" and m.get("content")]
    raw = " ".join(user_texts)[-400:]

    mood = "平静"
    if any(k in raw for k in ["崩溃", "绝望", "想哭"]):
        mood = "崩溃"
    elif any(k in raw for k in ["迷茫", "不知道", "困惑"]):
        mood = "迷茫"
    elif any(k in raw for k in ["难过", "低落", "沮丧"]):
        mood = "低落"
    elif any(k in raw for k in ["轻松", "放松"]):
        mood = "轻松"
    elif any(k in raw for k in ["开心", "愉快", "高兴"]):
        mood = "愉快"

    tags: List[str] = []
    for keyword in ("工作", "学习", "家庭", "感情", "人际", "健康", "金钱", "未来"):
        if keyword in raw:
            tags.append(keyword)
    tags = tags[:5]

    summary = raw.strip()
    summary = summary[:80] if summary else "一次日常聊天记录，用户分享了近期情绪状态。"
    return {"mood": mood, "tags": tags, "summary": summary}


def summarize_chat_to_emotion(messages: List[dict]) -> dict:
    if not messages:
        return {"mood": "平静", "tags": [], "summary": "暂无可归档聊天内容。"}

    client = _get_client()
    if client is None:
        return _fallback_archive(messages)

    compact_text = "\n".join(
        [f"{m.get('role', 'user')}: {m.get('content', '')}" for m in messages if m.get("content")]
    )[-3000:]

    try:
        response = client.chat.completions.create(
            model=DASHSCOPE_MODEL,
            temperature=0.2,
            max_tokens=260,
            messages=[
                {"role": "system", "content": ARCHIVE_PROMPT},
                {"role": "user", "content": compact_text},
            ],
        )
        content = (response.choices[0].message.content or "").strip()
        parsed = json.loads(content)
        mood = parsed.get("mood") or "平静"
        tags = parsed.get("tags") or []
        summary = parsed.get("summary") or "一次聊天情绪记录。"
        if not isinstance(tags, list):
            tags = []
        return {"mood": str(mood), "tags": [str(t) for t in tags[:5]], "summary": str(summary)[:120]}
    except Exception as exc:
        safe_print(f"[Archive Summarize Warning] err={exc}")
        return _fallback_archive(messages)
