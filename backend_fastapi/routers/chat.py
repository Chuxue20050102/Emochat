from fastapi import APIRouter, Query
import schemas
from utils import success_resp
from services.ai_service import chat_with_ai, get_memory, get_chat_message_history

router = APIRouter(prefix="/api/chat", tags=["4. AI 聊天"])

@router.post("/send")
def send_chat(req: schemas.ChatSendRequest):
    """发送消息获取AI回复，使用ConversationBufferMemory实现记忆功能"""

    print(f"\n👉 [收到用户消息]: {req.message} [用户ID]: {req.user_id}")

    # 调用AI服务，传入user_id以实现记忆功能
    ai_reply = chat_with_ai(req.message, user_id=req.user_id)

    print(f"✨ [AI回复内容]: {ai_reply}\n")

    return success_resp(data={"reply_msg": ai_reply, "is_crisis": False})

@router.get("/history")
def get_history(user_id: int = Query(..., description="用户ID")):
    """获取用户的历史聊天记录"""
    try:
        memory = get_memory(user_id)
        history_messages = memory.chat_memory.messages
        messages = []
        for msg in history_messages:
            if hasattr(msg, 'type') and msg.type == 'human':
                messages.append({"role": "user", "content": msg.content})
            elif hasattr(msg, 'type') and msg.type == 'ai':
                messages.append({"role": "assistant", "content": msg.content})
        return success_resp(data={"messages": messages})
    except Exception as e:
        print(f"[Get History Error] {e}")
        return success_resp(data={"messages": []})

@router.delete("/history")
def delete_history(user_id: int = Query(..., description="用户ID")):
    """清空用户的历史聊天记录"""
    try:
        chat_history = get_chat_message_history(user_id)
        chat_history.clear()
        return success_resp(msg="已清空与 AI 的所有回忆")
    except Exception as e:
        print(f"[Delete History Error] {e}")
        return success_resp(msg="清空失败")
