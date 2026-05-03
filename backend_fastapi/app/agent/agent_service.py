import json
import time
from typing import Any, Dict, List

from sqlalchemy.orm import Session

import models
import schemas
from app.agent import tools
from services.ai.client import get_client
from services.ai.config import DASHSCOPE_MODEL
from services.ai.safety import crisis_help_message, detect_crisis
from services.ai.utils import llm_json_parse

ALLOWED_INTENTS = {"support_chat", "emotion_review", "archive_chat"}

PLANNER_PROMPT = """
你是 EmoChat 的 Agent Planner。请根据用户输入决定要执行哪些意图，只输出 JSON。

可选 intents:
- support_chat: 普通情绪陪伴聊天
- emotion_review: 查询或回顾历史情绪记录
- archive_chat: 将最近聊天总结并写入情绪档案

输出格式:
{
  "intents": ["emotion_review"],
  "reason": "用户想查看最近情绪状态"
}

规则:
1. 用户只是倾诉、表达感受时，使用 support_chat。
2. 用户想看最近状态、历史记录、情绪趋势、这周/这几天怎么样时，使用 emotion_review。
3. 用户想保存、归档、写入档案、整理聊天时，使用 archive_chat。
4. 如果一句话包含多个任务，可以返回多个 intents。
""".strip()


def _normalize_text(text: str) -> str:
    return str(text or "").strip().lower()


def _rule_based_intents(message: str) -> List[str]:
    text = _normalize_text(message)
    intents: List[str] = []

    history_keywords = (
        "历史",
        "记录",
        "最近",
        "状态",
        "回顾",
        "趋势",
        "情绪变化",
        "这周",
        "这几天",
        "看看我",
        "复盘",
    )
    archive_keywords = (
        "归档",
        "保存",
        "记下来",
        "加入档案",
        "写入档案",
        "整理进档案",
        "整理一下",
        "保存感受",
    )

    if any(keyword in text for keyword in history_keywords):
        intents.append("emotion_review")
    if any(keyword in text for keyword in archive_keywords):
        intents.append("archive_chat")
    if not intents:
        intents.append("support_chat")

    return intents


def _sanitize_intents(raw_intents: Any) -> List[str]:
    if not isinstance(raw_intents, list):
        return []
    cleaned: List[str] = []
    for item in raw_intents:
        intent = str(item or "").strip()
        if intent in ALLOWED_INTENTS and intent not in cleaned:
            cleaned.append(intent)
    return cleaned


def plan_intents(message: str) -> Dict[str, Any]:
    fallback_intents = _rule_based_intents(message)
    client = get_client()
    if client is None:
        return {
            "intents": fallback_intents,
            "planner": "rule",
            "reason": "model_not_configured",
        }

    try:
        response = client.chat.completions.create(
            model=DASHSCOPE_MODEL,
            temperature=0,
            max_tokens=180,
            messages=[
                {"role": "system", "content": PLANNER_PROMPT},
                {"role": "user", "content": message},
            ],
        )
        raw = response.choices[0].message.content or ""
        parsed = llm_json_parse(raw)
        intents = _sanitize_intents(parsed.get("intents"))
        if intents:
            return {
                "intents": intents,
                "planner": "llm",
                "reason": str(parsed.get("reason") or "").strip(),
            }
    except Exception as exc:
        return {
            "intents": fallback_intents,
            "planner": "rule",
            "reason": f"planner_error: {exc}",
        }

    return {
        "intents": fallback_intents,
        "planner": "rule",
        "reason": "invalid_planner_output",
    }


CRISIS_KEYWORDS = (
    "不想活", "想死", "自杀", "自残", "结束生命", "伤害自己",
    "活不下去", "死了算了", "生无可恋", "一了百了", "了断",
    "没有意义活着", "不如死了", "去死", "寻死",
)

MODERATE_CONCERN_KEYWORDS = (
    "想消失", "撑不下去了", "熬不下去", "看不到希望",
    "活着好累", "没有希望", "走投无路", "无处可逃",
    "不想存在", "消失算了", "撑不住", "扛不住",
    "快要崩溃", "撑不了多久",
)


def _is_safety_message(message: str) -> bool:
    text = _normalize_text(message)
    if any(keyword in text for keyword in CRISIS_KEYWORDS):
        return True
    if detect_crisis(message):
        return True
    return False


def _has_moderate_concern(message: str) -> bool:
    text = _normalize_text(message)
    return any(keyword in text for keyword in MODERATE_CONCERN_KEYWORDS)


def _record_tool_call(name: str, started_at: float, status: str, result: Any = None) -> Dict[str, Any]:
    return {
        "name": name,
        "status": status,
        "elapsed_ms": int((time.perf_counter() - started_at) * 1000),
        "result": result,
    }


def _format_history_summary(records: List[dict]) -> str:
    if not records:
        return "我还没有查到可用于回看的历史情绪记录。"

    lines = []
    for record in records[:5]:
        date = record.get("record_date", "")
        mood = record.get("mood", "未知")
        tags = record.get("tags") or ""
        lines.append(f"{date}: {mood}{' (' + tags + ')' if tags else ''}")
    return "我查到了最近的情绪记录：\n" + "\n".join(lines)


def _save_trace(
    db: Session,
    req: schemas.AgentRunRequest,
    payload: Dict[str, Any],
) -> int:
    trace = models.AgentTrace(
        user_id=req.user_id,
        message=req.message,
        intent=payload.get("intent") or "",
        tool_calls=json.dumps(payload.get("tool_calls") or [], ensure_ascii=False),
        trace=json.dumps(payload.get("trace") or {}, ensure_ascii=False),
        reply=payload.get("reply") or "",
    )
    db.add(trace)
    db.commit()
    db.refresh(trace)
    return trace.id


def run_agent(req: schemas.AgentRunRequest, db: Session) -> Dict[str, Any]:
    started_at = time.perf_counter()
    tool_calls: List[Dict[str, Any]] = []

    moderate_concern = _has_moderate_concern(req.message)

    if _is_safety_message(req.message):
        payload = {
            "reply": crisis_help_message(),
            "intent": "safety",
            "intents": ["safety"],
            "tool_calls": [],
            "trace": {
                "elapsed_ms": int((time.perf_counter() - started_at) * 1000),
                "fallback_reason": "crisis_detected",
                "planner": "safety_guard",
                "planner_reason": "命中危机风险表达，跳过工具调用",
                "tool_count": 0,
                "moderate_concern": moderate_concern,
            },
        }
        payload["trace_id"] = _save_trace(db, req, payload)
        return payload

    rule_intents = _rule_based_intents(req.message)
    if req.skip_emotion_review and "emotion_review" in rule_intents:
        rule_intents.remove("emotion_review")
        if not rule_intents:
            rule_intents.append("support_chat")
    if rule_intents == ["support_chat"]:
        plan = {"intents": rule_intents, "planner": "rule_fast", "reason": "纯聊天，跳过 LLM Planner"}
    else:
        plan = plan_intents(req.message)
    intents = plan["intents"]
    reply_parts: List[str] = []

    if "emotion_review" in intents:
        tool_started = time.perf_counter()
        try:
            history_payload = tools.get_emotion_history_tool(req.user_id, req.history_limit, db)
            records = history_payload.get("records", [])
            tool_calls.append(_record_tool_call("get_emotion_history", tool_started, "success", history_payload))
            reply_parts.append(_format_history_summary(records))
        except Exception as exc:
            tool_calls.append(_record_tool_call("get_emotion_history", tool_started, "error", str(exc)))
            reply_parts.append("我刚才查询历史情绪时遇到了一点问题，稍后可以再试。")

    if "archive_chat" in intents:
        tool_started = time.perf_counter()
        try:
            archive_result = tools.archive_chat_to_emotion_tool(
                req.user_id,
                req.archive_max_messages,
                db,
            )
            status = "success" if archive_result.get("ok") else "empty"
            tool_calls.append(_record_tool_call("archive_chat_to_emotion", tool_started, status, archive_result))
            payload = archive_result.get("payload") or {}
            if archive_result.get("ok"):
                reply_parts.append(
                    f"我已经把最近聊天整理进情绪档案：{payload.get('mood', '未知')}，{payload.get('summary', '')}"
                )
            else:
                reply_parts.append(payload.get("msg") or "目前还没有足够的聊天内容可以保存。")
        except Exception as exc:
            tool_calls.append(_record_tool_call("archive_chat_to_emotion", tool_started, "error", str(exc)))
            reply_parts.append("我刚才保存聊天时失败了，稍后可以再试。")

    if "support_chat" in intents:
        tool_started = time.perf_counter()
        try:
            chat_payload = tools.chat_reply_tool(req, db)
            tool_calls.append(_record_tool_call("chat_reply", tool_started, "success", chat_payload))
            reply_parts.append(chat_payload.get("reply_msg") or "我在。")
        except Exception as exc:
            tool_calls.append(_record_tool_call("chat_reply", tool_started, "error", str(exc)))
            reply_parts.append("我刚才有点卡住了，你愿意再说一遍吗？")

    payload = {
        "reply": "\n\n".join([part for part in reply_parts if part]).strip(),
        "intent": "+".join(intents),
        "intents": intents,
        "tool_calls": tool_calls,
        "trace": {
            "elapsed_ms": int((time.perf_counter() - started_at) * 1000),
            "fallback_reason": "",
            "planner": plan.get("planner", "rule"),
            "planner_reason": plan.get("reason", ""),
            "tool_count": len(tool_calls),
            "moderate_concern": moderate_concern,
        },
    }
    payload["trace_id"] = _save_trace(db, req, payload)
    return payload


def get_agent_traces(user_id: int, limit: int, db: Session) -> Dict[str, Any]:
    rows = (
        db.query(models.AgentTrace)
        .filter(models.AgentTrace.user_id == user_id)
        .order_by(models.AgentTrace.created_at.desc(), models.AgentTrace.id.desc())
        .limit(limit)
        .all()
    )
    return {
        "traces": [
            {
                "id": row.id,
                "user_id": row.user_id,
                "message": row.message,
                "intent": row.intent,
                "tool_calls": json.loads(row.tool_calls or "[]"),
                "trace": json.loads(row.trace or "{}"),
                "reply": row.reply,
                "created_at": row.created_at.isoformat() if row.created_at else "",
            }
            for row in rows
        ]
    }
