from sqlalchemy import Boolean, Column, Integer, String, Text, Date, DateTime, ForeignKey
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    account = Column(String(50), unique=True, index=True, nullable=True)
    password = Column(String(100), nullable=True)
    nickname = Column(String(50))
    avatar_url = Column(String(255), nullable=True)
    is_guest = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class EmotionRecord(Base):
    __tablename__ = "emotion_records"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    mood = Column(String(20))
    tags = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    record_date = Column(Date)

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    role = Column(String(10)) # user 或者 assistant
    content = Column(Text)
    card_record_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
