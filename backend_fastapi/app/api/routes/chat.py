import json
import time

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

import schemas
from app.core.database import get_db
from app.core.response import success_resp
from app.services import chat_service
from services.ai.utils import safe_print

router = APIRouter(prefix="/api/chat", tags=["4. AI Chat"])
STREAM_HEADERS = {
    "Cache-Control": "no-cache, no-transform",
    "Connection": "keep-alive",
    "X-Accel-Buffering": "no",
}


@router.post("/send")
def send_chat(req: schemas.ChatSendRequest, db: Session = Depends(get_db)):
    started_at = time.perf_counter()
    payload = chat_service.send_chat(req, db)
    elapsed_ms = int((time.perf_counter() - started_at) * 1000)
    safe_print(
        f"[Chat API Timing] user_id={req.user_id}, use_memory={req.use_memory}, elapsed_ms={elapsed_ms}"
    )
    return success_resp(data=payload)


@router.post("/stream")
async def stream_chat(
    req: schemas.ChatSendRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    started_at = time.perf_counter()
    if not (req.message or "").strip():
        payload = {"type": "end", "reply_msg": "", "is_crisis": False, "crisis_help_message": ""}
        return StreamingResponse(
            iter([json.dumps(payload, ensure_ascii=False) + "\n"]),
            media_type="application/x-ndjson",
            headers=STREAM_HEADERS,
        )

    stream = chat_service.stream_chat(req, request, db)

    async def wrapped_generator():
        try:
            async for chunk in stream:
                yield chunk
        finally:
            elapsed_ms = int((time.perf_counter() - started_at) * 1000)
            safe_print(
                f"[Chat Stream API Timing] user_id={req.user_id}, "
                f"use_memory={req.use_memory}, elapsed_ms={elapsed_ms}"
            )

    return StreamingResponse(
        wrapped_generator(),
        media_type="application/x-ndjson",
        headers=STREAM_HEADERS,
    )


@router.get("/history")
def get_history(
    user_id: int = Query(..., description="User ID"),
    limit: int = Query(100, ge=1, le=300, description="Message limit"),
):
    payload = chat_service.get_history(user_id, limit=limit)
    return success_resp(data=payload)


@router.delete("/history")
def delete_history(user_id: int = Query(..., description="User ID")):
    payload = chat_service.delete_history(user_id)
    return success_resp(msg=payload["msg"])


@router.get("/memory-profile")
def get_memory_profile(user_id: int = Query(..., description="User ID")):
    payload = chat_service.get_memory_profile(user_id)
    return success_resp(data=payload)


@router.post("/archive")
def archive_chat_to_emotion(req: schemas.ChatArchiveRequest, db: Session = Depends(get_db)):
    ok, payload = chat_service.archive_chat_to_emotion(req, db)
    if not ok:
        return success_resp(msg=payload["msg"], data=payload["data"])
    return success_resp(data=payload, msg="Archived chat content into emotion records")


@router.get("/emotion-history")
def get_emotion_history_from_chat(
    user_id: int = Query(..., description="User ID"),
    limit: int = Query(20, ge=1, le=100, description="Record limit"),
    db: Session = Depends(get_db),
):
    payload = chat_service.get_emotion_history(user_id, limit, db)
    return success_resp(data=payload)
