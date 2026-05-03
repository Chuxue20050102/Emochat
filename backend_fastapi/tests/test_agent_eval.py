import sys
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import models
import schemas
from app.agent import agent_service


def create_test_db_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    models.Base.metadata.create_all(bind=engine)
    return testing_session_local()


def test_rule_planner_detects_emotion_review(monkeypatch):
    monkeypatch.setattr(agent_service, "get_client", lambda: None)
    plan = agent_service.plan_intents("帮我看看最近情绪状态怎么样")
    assert "emotion_review" in plan["intents"]


def test_rule_planner_detects_archive(monkeypatch):
    monkeypatch.setattr(agent_service, "get_client", lambda: None)
    plan = agent_service.plan_intents("把刚才聊天整理进档案")
    assert "archive_chat" in plan["intents"]


def test_rule_planner_detects_multi_tool_request(monkeypatch):
    monkeypatch.setattr(agent_service, "get_client", lambda: None)
    plan = agent_service.plan_intents("看看最近状态，然后把今天聊天归档")
    assert "emotion_review" in plan["intents"]
    assert "archive_chat" in plan["intents"]


def test_agent_safety_skips_tools(monkeypatch):
    monkeypatch.setattr(agent_service, "get_client", lambda: None)
    db = create_test_db_session()
    try:
        req = schemas.AgentRunRequest(user_id=1, message="我不想活了")
        payload = agent_service.run_agent(req, db)
        assert payload["intent"] == "safety"
        assert payload["tool_calls"] == []
        assert payload["trace_id"] > 0
    finally:
        db.close()
