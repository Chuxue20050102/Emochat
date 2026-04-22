from pydantic import BaseModel, Field
from typing import Optional, List, Union
from datetime import date

# 基础响应模型
class ResponseModel(BaseModel):
    code: int = 200
    data: Union[dict, list, None] = None
    msg: str = "ok"

class RegisterRequest(BaseModel):
    account: str
    password: str
    nickname: str

class LoginRequest(BaseModel):
    account: str
    password: str

class RecordRequest(BaseModel):
    user_id: int
    mood: str
    tags: Optional[str] = ""
    description: Optional[str] = ""
    record_date: Optional[date] = None

class ChatSendRequest(BaseModel):
    user_id: int
    message: str
    card_record_id: Optional[int] = None
    use_memory: bool = True
    emotion_context: Optional[dict] = None


class ChatArchiveRequest(BaseModel):
    user_id: int
    max_messages: int = Field(default=30, ge=6, le=200)

class GreetingSchema(BaseModel):
    id: int
    content: str
    author: Optional[str] = None

    class Config:
        from_attributes = True

