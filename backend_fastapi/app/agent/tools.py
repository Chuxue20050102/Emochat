from typing import Any, Dict

from sqlalchemy.orm import Session

import schemas
from app.services import chat_service


def get_emotion_history_tool(user_id: int, limit: int, db: Session) -> Dict[str, Any]:
    return chat_service.get_emotion_history(user_id=user_id, limit=limit, db=db)


def archive_chat_to_emotion_tool(user_id: int, max_messages: int, db: Session) -> Dict[str, Any]:
    req = schemas.ChatArchiveRequest(user_id=user_id, max_messages=max_messages)
    ok, payload = chat_service.archive_chat_to_emotion(req, db)
    return {
        "ok": ok,
        "payload": payload,
    }


def chat_reply_tool(req: schemas.AgentRunRequest, db: Session) -> Dict[str, Any]:
    chat_req = schemas.ChatSendRequest(
        user_id=req.user_id,
        message=req.message,
        use_memory=req.use_memory,
        card_record_id=req.card_record_id,
        emotion_context=req.emotion_context,
    )
    return chat_service.send_chat(chat_req, db)
