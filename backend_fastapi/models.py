from datetime import datetime

from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String, Text

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
    source = Column(String(20), nullable=False, default="manual")
    tags = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    record_date = Column(Date)
    created_at = Column(DateTime, default=datetime.now)


class Greeting(Base):
    __tablename__ = "greetings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    content = Column(Text, nullable=False)
    author = Column(String(50), nullable=True)


class HomeCopy(Base):
    __tablename__ = "home_copies"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    module = Column(String(50), index=True, nullable=False)
    state = Column(String(30), index=True, nullable=False, default="default")
    field = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)


class AgentTrace(Base):
    __tablename__ = "agent_traces"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, index=True)
    message = Column(Text, nullable=False)
    intent = Column(String(100), nullable=False)
    tool_calls = Column(Text, nullable=True)
    trace = Column(Text, nullable=True)
    reply = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
