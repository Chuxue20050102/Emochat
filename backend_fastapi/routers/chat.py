import json
import threading
import time
from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import StreamingResponse
from sqlalchemy import desc
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from services.ai_service import (
    chat_with_ai,
    clear_memory,
    crisis_help_message,
    detect_crisis,
    get_history_messages,
    safe_print,
    stream_chat_with_ai,
    summarize_chat_to_emotion,
)
from utils import success_resp

router = APIRouter(prefix="/api/chat", tags=["4. AI 聊天"])


def _build_context_from_record(record: Optional[models.EmotionRecord]) -> Optional[dict]:
    if record is None:
        return None
    return {
        "emotion": record.mood,
        "tags": [x for x in (record.tags or "").split(",") if x],
        "detail": [],
        "content": record.description or "",
    }


def _resolve_extra_context(
    req: schemas.ChatSendRequest,
    db: Session,
) -> Optional[dict]:
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
        return _build_context_from_record(record)
    return extra_context


@router.post("/send")
def send_chat(req: schemas.ChatSendRequest, db: Session = Depends(get_db)):
    started_at = time.perf_counter()
    user_message = (req.message or "").strip()
    if not user_message:
        return success_resp(
            data={
                "reply_msg": "我在，想聊什么都可以。",
                "is_crisis": False,
                "crisis_help_message": "",
            }
        )

    safe_print(f"\n[Chat] user_id={req.user_id}, message={user_message}")
    extra_context = _resolve_extra_context(req, db)
    memory_user_id = req.user_id if req.use_memory else None

    ai_reply = chat_with_ai(
        user_message,
        user_id=memory_user_id,
        extra_context=extra_context,
    )
    is_crisis = detect_crisis(user_message) or detect_crisis(ai_reply)
    elapsed_ms = int((time.perf_counter() - started_at) * 1000)
    safe_print(
        f"[Chat API Timing] user_id={req.user_id}, use_memory={req.use_memory}, elapsed_ms={elapsed_ms}"
    )

    return success_resp(
        data={
            "reply_msg": ai_reply,
            "is_crisis": is_crisis,
            "crisis_help_message": crisis_help_message() if is_crisis else "",
        }
    )


@router.post("/stream")
async def stream_chat(
    req: schemas.ChatSendRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    started_at = time.perf_counter()
    user_message = (req.message or "").strip()
    if not user_message:
        payload = {"type": "end", "reply_msg": "", "is_crisis": False, "crisis_help_message": ""}
        return StreamingResponse(
            iter([json.dumps(payload, ensure_ascii=False) + "\n"]),
            media_type="application/x-ndjson",
        )

    safe_print(f"\n[Chat Stream] user_id={req.user_id}, message={user_message}")
    extra_context = _resolve_extra_context(req, db)
    memory_user_id = req.user_id if req.use_memory else None
    cancel_event = threading.Event()

    async def event_generator():
        parts = []
        first_delta_ms = None
        completed = False

        try:
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
                if first_delta_ms is None:
                    first_delta_ms = int((time.perf_counter() - started_at) * 1000)
                    safe_print(
                        f"[Chat Stream API First Delta] user_id={req.user_id}, first_delta_ms={first_delta_ms}"
                    )

                yield json.dumps({"type": "delta", "content": chunk}, ensure_ascii=False) + "\n"

            if cancel_event.is_set():
                return

            ai_reply = "".join(parts).strip()
            is_crisis = detect_crisis(user_message) or detect_crisis(ai_reply)
            completed = True
            yield json.dumps(
                {
                    "type": "end",
                    "reply_msg": ai_reply,
                    "is_crisis": is_crisis,
                    "crisis_help_message": crisis_help_message() if is_crisis else "",
                },
                ensure_ascii=False,
            ) + "\n"
        finally:
            elapsed_ms = int((time.perf_counter() - started_at) * 1000)
            safe_print(
                f"[Chat Stream API Timing] user_id={req.user_id}, use_memory={req.use_memory}, "
                f"first_delta_ms={first_delta_ms}, elapsed_ms={elapsed_ms}, "
                f"completed={completed}, cancelled={cancel_event.is_set()}"
            )

    return StreamingResponse(event_generator(), media_type="application/x-ndjson")


@router.get("/history")
def get_history(
    user_id: int = Query(..., description="用户ID"),
    limit: int = Query(100, ge=1, le=300, description="返回消息数量上限"),
):
    try:
        messages = get_history_messages(user_id, limit=limit)
        return success_resp(data={"messages": messages})
    except Exception as exc:
        safe_print(f"[Get History Error] user_id={user_id}, err={exc}")
        return success_resp(data={"messages": []})


@router.delete("/history")
def delete_history(user_id: int = Query(..., description="用户ID")):
    try:
        clear_memory(user_id)
        return success_resp(msg="已清空与 AI 的聊天记忆")
    except Exception as exc:
        safe_print(f"[Delete History Error] user_id={user_id}, err={exc}")
        return success_resp(msg="清空失败，请稍后再试")


@router.post("/archive")
def archive_chat_to_emotion(req: schemas.ChatArchiveRequest, db: Session = Depends(get_db)):
    messages = get_history_messages(req.user_id, limit=req.max_messages)
    if not messages:
        return success_resp(msg="暂无可归档聊天内容", data=None)

    archive = summarize_chat_to_emotion(messages)
    mood = archive.get("mood") or "平静"
    tags = archive.get("tags") or []
    summary = archive.get("summary") or "一次聊天情绪记录。"

    record = models.EmotionRecord(
        user_id=req.user_id,
        mood=mood,
        tags=",".join(tags),
        description=summary,
        record_date=date.today(),
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return success_resp(
        data={
            "record_id": record.id,
            "mood": mood,
            "tags": tags,
            "summary": summary,
        },
        msg="已归档聊天内容到情绪档案",
    )


@router.get("/emotion-history")
def get_emotion_history_from_chat(
    user_id: int = Query(..., description="用户ID"),
    limit: int = Query(20, ge=1, le=100, description="返回条数"),
    db: Session = Depends(get_db),
):
    records = (
        db.query(models.EmotionRecord)
        .filter(models.EmotionRecord.user_id == user_id)
        .order_by(desc(models.EmotionRecord.record_date), desc(models.EmotionRecord.id))
        .limit(limit)
        .all()
    )
    return success_resp(
        data={
            "records": [
                {
                    "id": r.id,
                    "mood": r.mood,
                    "tags": r.tags or "",
                    "description": r.description or "",
                    "record_date": str(r.record_date),
                }
                for r in records
            ]
        }
    )
