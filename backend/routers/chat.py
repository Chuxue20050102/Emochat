import time
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
import models, schemas
from utils import success_resp, error_resp

router = APIRouter(prefix="/api/chat", tags=["4. AI 聊天模拟"])

@router.post("/send")
def send_chat(req: schemas.ChatSendRequest, db: Session = Depends(get_db)):
    user_msg = models.ChatMessage(
        user_id=req.user_id,
        role="user",
        content=req.message,
        card_record_id=req.card_record_id
    )
    db.add(user_msg)
    
    time.sleep(1)
    ai_msg = models.ChatMessage(
        user_id=req.user_id,
        role="assistant",
        content="我看到你刚刚发出来的话了，一切的情绪都是可以被接纳的，我会陪着你。 （注：此为假大模型数据）",
        card_record_id=req.card_record_id
    )
    db.add(ai_msg)
    db.commit()
    
    return success_resp(data={"reply_msg": ai_msg.content, "is_crisis": False})

@router.get("/history")
def get_chat_history(user_id: int, db: Session = Depends(get_db)):
    messages = db.query(models.ChatMessage).filter(models.ChatMessage.user_id == user_id).order_by(models.ChatMessage.created_at.asc()).all()
    res = [{"role": m.role, "content": m.content, "time": str(m.created_at)} for m in messages]
    return success_resp(data=res)

@router.delete("/history")
def clear_chat_history(user_id: int, db: Session = Depends(get_db)):
    db.query(models.ChatMessage).filter(models.ChatMessage.user_id == user_id).delete()
    db.commit()
    return success_resp(msg="聊天记忆清空完毕")
