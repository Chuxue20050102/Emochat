import json
from typing import List

from services.ai.client import get_client
from services.ai.config import DASHSCOPE_MODEL
from services.ai.prompts import ARCHIVE_PROMPT
from services.ai.safety import detect_crisis
from services.ai.utils import llm_json_parse, safe_print


def fallback_archive(messages: List[dict]) -> dict:
    user_texts = [m["content"] for m in messages if m.get("role") == "user" and m.get("content")]
    raw = " ".join(user_texts)[-500:]

    mood = "中性"
    if detect_crisis(raw):
        mood = "非常不愉快"
    elif any(k in raw for k in ["难过", "低落", "沮丧", "崩溃", "绝望", "想哭"]):
        mood = "不愉快"
    elif any(k in raw for k in ["迷茫", "不知道", "困惑", "有点闷", "担心"]):
        mood = "有点不愉快"
    elif any(k in raw for k in ["放松", "轻松", "舒服", "安心"]):
        mood = "有点愉快"
    elif any(k in raw for k in ["开心", "愉快", "高兴", "满足", "顺利"]):
        mood = "愉快"
    elif any(k in raw for k in ["兴奋", "特别开心", "超满足", "幸福"]):
        mood = "很愉快"

    tags = []
    for tag in ["工作", "人际", "家庭", "学习", "睡眠", "健康", "情感", "金钱", "未来"]:
        if tag in raw and tag not in tags:
            tags.append(tag)

    user_last = user_texts[-1] if user_texts else ""
    summary = user_last[:60] if user_last else "一段日常聊天，记录了当时的感受。"
    return {"mood": mood, "tags": tags[:5], "summary": summary}


def summarize_chat_to_emotion(messages: List[dict]) -> dict:
    if not messages:
        return {"mood": "calm", "tags": [], "summary": "暂无可归档聊天内容。"}

    client = get_client()
    if client is None:
        return fallback_archive(messages)

    compact_text = "\n".join(
        [f"{m.get('role', 'user')}: {m.get('content', '')}" for m in messages if m.get("content")]
    )[-2600:]

    try:
        response = client.chat.completions.create(
            model=DASHSCOPE_MODEL,
            temperature=0.2,
            max_tokens=220,
            messages=[
                {"role": "system", "content": ARCHIVE_PROMPT},
                {"role": "user", "content": compact_text},
            ],
        )
        raw = response.choices[0].message.content or ""
        parsed = llm_json_parse(raw)
        if not parsed:
            return fallback_archive(messages)

        mood = str(parsed.get("mood") or "calm").strip()
        tags = parsed.get("tags") or []
        if not isinstance(tags, list):
            tags = []
        tags = [str(t).strip() for t in tags if str(t).strip()][:5]
        summary = str(parsed.get("summary") or "一次聊天情绪记录。").strip()[:120]
        return {"mood": mood, "tags": tags, "summary": summary}
    except Exception as exc:
        safe_print(f"[Archive Summarize Error] err={exc}")
        return fallback_archive(messages)


_fallback_archive = fallback_archive
