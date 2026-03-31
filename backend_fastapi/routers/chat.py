from fastapi import APIRouter
import schemas
from utils import success_resp
from services.ai_service import chat_with_ai

router = APIRouter(prefix="/api/chat", tags=["4. AI 聊天"])

@router.post("/send")
def send_chat(req: schemas.ChatSendRequest):
    """【极简版本】直接发送消息获取AI回复，去掉所有数据库操作"""
    
    print(f"\n👉 [收到用户消息]: {req.message}")
    
    # 极简调用：不带历史记录，直接跟AI单轮对话
    ai_reply = chat_with_ai(req.message, history=[])
    
    print(f"✨ [AI回复内容]: {ai_reply}\n")
    
    return success_resp(data={"reply_msg": ai_reply, "is_crisis": False})
