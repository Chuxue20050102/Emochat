import json
import threading
from datetime import date
from typing import Optional

from fastapi import Request
from sqlalchemy import desc
from sqlalchemy.orm import Session

import models
import schemas
from services.ai.archive import summarize_chat_to_emotion
from services.ai.chat import chat_with_ai, stream_chat_with_ai
from services.ai.memory import clear_memory, get_history_messages, get_structured_memory
from services.ai.safety import crisis_help_message, detect_crisis
from services.ai.utils import safe_print


def build_context_from_record(record: Optional[models.EmotionRecord]) -> Optional[dict]:
    if record is None:
        return None
    return {
        "emotion": record.mood,
        "tags": [x for x in (record.tags or "").split(",") if x],
        "detail": [],
        "content": record.description or "",
    }


def resolve_extra_context(req: schemas.ChatSendRequest, db: Session) -> Optional[dict]:
    extra_context = req.emotion_context or None
    if req.card_record_id is None:
        return extra_context

    record = (
        db.query(models.EmotionRecord)
        .filter(
            models.EmotionRecord.id == req.card_record_id,
            models.EmotionRecord.user_id == req.user_id,
        )
        .first()
    )
    if record is not None:
        return build_context_from_record(record)
    return extra_context


def send_chat(req: schemas.ChatSendRequest, db: Session):
    user_message = (req.message or "").strip()
    if not user_message:
        return {
            "reply_msg": "我在，想聊什么都可以。",
            "is_crisis": False,
            "crisis_help_message": "",
        }

    safe_print(f"\n[Chat] user_id={req.user_id}, message={user_message}")
    extra_context = resolve_extra_context(req, db)
    memory_user_id = req.user_id if req.use_memory else None

    ai_reply = chat_with_ai(
        user_message,
        user_id=memory_user_id,
        extra_context=extra_context,
    )
    is_crisis = detect_crisis(user_message) or detect_crisis(ai_reply)
    return {
        "reply_msg": ai_reply,
        "is_crisis": is_crisis,
        "crisis_help_message": crisis_help_message() if is_crisis else "",
    }


def stream_chat(req: schemas.ChatSendRequest, request: Request, db: Session):
    user_message = (req.message or "").strip()
    if not user_message:
        payload = {"type": "end", "reply_msg": "", "is_crisis": False, "crisis_help_message": ""}
        return iter([json.dumps(payload, ensure_ascii=False) + "\n"])

    safe_print(f"\n[Chat Stream] user_id={req.user_id}, message={user_message}")
    extra_context = resolve_extra_context(req, db)
    memory_user_id = req.user_id if req.use_memory else None
    cancel_event = threading.Event()

    async def event_generator():
        parts = []
        yield json.dumps({"type": "start"}, ensure_ascii=False) + "\n"
        for chunk in stream_chat_with_ai(
            user_message,
            user_id=memory_user_id,
            extra_context=extra_context,
            cancel_event=cancel_event,
        ):
            if await request.is_disconnected():
                cancel_event.set()
                safe_print(f"[Chat Stream Disconnected] user_id={req.user_id}")
                break

            if not chunk:
                continue
            parts.append(chunk)
            yield json.dumps({"type": "delta", "content": chunk}, ensure_ascii=False) + "\n"

        if cancel_event.is_set():
            return

        ai_reply = "".join(parts).strip()
        is_crisis = detect_crisis(user_message) or detect_crisis(ai_reply)
        yield json.dumps(
            {
                "type": "end",
                "reply_msg": ai_reply,
                "is_crisis": is_crisis,
                "crisis_help_message": crisis_help_message() if is_crisis else "",
            },
            ensure_ascii=False,
        ) + "\n"

    return event_generator()


def get_history(user_id: int, limit: int = 100):
    return {"messages": get_history_messages(user_id, limit=limit)}


def delete_history(user_id: int):
    clear_memory(user_id)
    return {"msg": "已清空与陪聊相关的聊天记录"}


def get_memory_profile(user_id: int):
    return {"profile": get_structured_memory(user_id)}


def format_created_at(record) -> str:
    if not getattr(record, "created_at", None):
        return ""
    return record.created_at.strftime("%Y-%m-%d %H:%M")


def archive_chat_to_emotion(req: schemas.ChatArchiveRequest, db: Session):
    messages = get_history_messages(req.user_id, limit=req.max_messages)
    if not messages:
        return False, {"msg": "暂无可保存的聊天内容", "data": None}

    archive = summarize_chat_to_emotion(messages)
    mood = archive.get("mood") or "calm"
    tags = archive.get("tags") or []
    summary = archive.get("summary") or "一次聊天情绪记录。"

    record = models.EmotionRecord(
        user_id=req.user_id,
        mood=mood,
        source="chat",
        tags=",".join(tags),
        description=summary,
        record_date=date.today(),
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return True, {
        "record_id": record.id,
        "mood": mood,
        "tags": tags,
        "summary": summary,
        "created_at": format_created_at(record),
    }


def get_emotion_history(user_id: int, limit: int, db: Session):
    records = (
        db.query(models.EmotionRecord)
        .filter(models.EmotionRecord.user_id == user_id)
        .order_by(desc(models.EmotionRecord.record_date), desc(models.EmotionRecord.created_at), desc(models.EmotionRecord.id))
        .limit(limit)
        .all()
    )
    return {
        "records": [
            {
                "id": r.id,
                "mood": r.mood,
                "source": r.source or "manual",
                "tags": r.tags or "",
                "description": r.description or "",
                "record_date": str(r.record_date),
                "created_at": format_created_at(r),
            }
            for r in records
        ]
    }
