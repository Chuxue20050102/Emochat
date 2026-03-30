import time
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..utils import success_resp, error_resp
# 导入 AI 服务
from backend_fastapi.services.ai_service import chat_with_ai

router = APIRouter(prefix="/api/chat", tags=["4. AI 聊天"])

@router.post("/send")
def send_chat(req: schemas.ChatSendRequest, db: Session = Depends(get_db)):
    """发送消息并获取 AI 回复（已接入 DeepSeek 大模型）"""
    
    # 1. 保存用户消息到数据库
    user_msg = models.ChatMessage(
        user_id=req.user_id,
        role="user",
        content=req.message,
        card_record_id=req.card_record_id
    )
    db.add(user_msg)
    
    # 2. 查询历史对话，构建上下文（最近 10 轮）
    history_records = (
        db.query(models.ChatMessage)
        .filter(models.ChatMessage.user_id == req.user_id)
        .order_by(models.ChatMessage.created_at.desc())
        .limit(20)
        .all()
    )
    # 倒序取出后再反转为正序
    history = [
        {"role": msg.role, "content": msg.content}
        for msg in reversed(history_records)
    ]
    
    # 3. 调用 AI 服务获取回复
    ai_reply = chat_with_ai(req.message, history=history)
    
    # 4. 保存 AI 回复到数据库
    ai_msg = models.ChatMessage(
        user_id=req.user_id,
        role="assistant",
        content=ai_reply,
        card_record_id=req.card_record_id
    )
    db.add(ai_msg)
    db.commit()
    
    return success_resp(data={"reply_msg": ai_reply, "is_crisis": False})

@router.get("/history")
def get_chat_history(user_id: int, db: Session = Depends(get_db)):
    """获取用户的聊天历史"""
    messages = (
        db.query(models.ChatMessage)
        .filter(models.ChatMessage.user_id == user_id)
        .order_by(models.ChatMessage.created_at.asc())
        .all()
    )
    res = [{"role": m.role, "content": m.content, "time": str(m.created_at)} for m in messages]
    return success_resp(data=res)

@router.delete("/history")
def clear_chat_history(user_id: int, db: Session = Depends(get_db)):
    """清空用户的聊天记录"""
    db.query(models.ChatMessage).filter(models.ChatMessage.user_id == user_id).delete()
    db.commit()
    return success_resp(msg="聊天记忆清空完毕")
