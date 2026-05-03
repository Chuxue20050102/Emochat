from collections import Counter
from datetime import date, datetime, timedelta

from sqlalchemy.orm import Session

import schemas
from app.repositories import emotion_repository
from services.ai.client import get_client
from services.ai.config import DASHSCOPE_MODEL
from services.ai.utils import safe_print


def format_created_at(record) -> str:
    if not getattr(record, "created_at", None):
        return ""
    return record.created_at.strftime("%Y-%m-%d %H:%M")


def create_record(db: Session, req: schemas.RecordRequest):
    record = emotion_repository.create_record(
        db,
        user_id=req.user_id,
        mood=req.mood,
        source="manual",
        tags=req.tags or "",
        description=req.description or "",
        record_date=req.record_date or date.today(),
    )
    return {"record_id": record.id}


def get_calendar(db: Session, *, user_id: int, year: int, month: int):
    records = emotion_repository.list_by_user(db, user_id)
    calendar_data = {}
    for r in records:
        if r.record_date and r.record_date.year == year and r.record_date.month == month:
            date_str = r.record_date.strftime("%Y-%m-%d")
            if date_str not in calendar_data:
                calendar_data[date_str] = {"mood": r.mood, "count": 0}
            calendar_data[date_str]["count"] += 1
    return calendar_data


def get_detail(db: Session, *, user_id: int, date_str: str):
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return False, {"code": 400, "data": None, "msg": "日期格式必须是 YYYY-MM-DD"}

    records = emotion_repository.list_by_user_and_date(
        db,
        user_id=user_id,
        target_date=target_date,
    )
    return True, [
        {
            "id": r.id,
            "mood": r.mood,
            "source": r.source or "manual",
            "tags": r.tags,
            "description": r.description,
            "record_date": str(r.record_date),
            "created_at": format_created_at(r),
        }
        for r in records
    ]


def get_history(
    db: Session,
    *,
    user_id: int,
    page: int,
    page_size: int,
    mood: str = "",
):
    total, records = emotion_repository.list_paginated(
        db,
        user_id=user_id,
        page=page,
        page_size=page_size,
        mood=mood,
    )
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "records": [
            {
                "id": r.id,
                "mood": r.mood,
                "source": r.source or "manual",
                "tags": r.tags or "",
                "description": r.description or "",
                "record_date": str(r.record_date),
                "created_at": format_created_at(r),
            }
            for r in records
        ],
    }


def _month_range(year: int, month: int):
    start = date(year, month, 1)
    if month == 12:
        end = date(year + 1, 1, 1)
    else:
        end = date(year, month + 1, 1)
    return start, end


def _split_tags(tags: str):
    return [item.strip() for item in str(tags or "").replace("，", ",").split(",") if item.strip()]


def _time_bucket(created_at) -> str:
    if not created_at:
        return ""
    hour = created_at.hour
    if 5 <= hour < 11:
        return "上午"
    if 11 <= hour < 14:
        return "中午"
    if 14 <= hour < 18:
        return "下午"
    if 18 <= hour < 24:
        return "晚上"
    return "凌晨"


INSIGHT_PROMPT = """你是 EmoChat 的情绪洞察助手。根据用户本月的情绪记录数据，生成 2-3 句温暖、有洞察力的自然语言总结。

要求：
1. 不只说"本月记录了 X 次"，而要发现模式：频率变化、情绪之间的关联、时段规律
2. 如果有标签和情绪的关联（如"人际"标签常伴随愉快），一定要提到
3. 周对比有变化时指出来，让用户感到被看见
4. 语气温暖但不油腻，用"你"称呼，不要用"用户"
5. 2-3 句话，每句不超过 25 个字，总字数控制在 80 以内
6. 如果本月没有记录，返回空字符串
7. 只返回纯文本，不要 JSON，不要 markdown"""


def _build_insight_prompt(data: dict) -> str:
    total = data.get("total_records", 0)
    if total == 0:
        return ""

    mood_dist = data.get("mood_distribution", {})
    top_mood = data.get("top_mood", "")
    top_tag = data.get("top_tag", "")
    top_time = data.get("top_time", "")
    active_days = data.get("active_days", 0)
    last_7 = data.get("last_7_records", 0)
    prev_7 = data.get("previous_7_records", 0)
    mood_tag_pairs = data.get("mood_tag_pairs", [])

    parts = [
        f"本月数据：共 {total} 条记录，分布在 {active_days} 天",
        f"最常出现的情绪：{top_mood}",
    ]
    if top_tag:
        parts.append(f"最常关联的线索：{top_tag}")
    if top_time:
        parts.append(f"最常记录的时段：{top_time}")
    if mood_dist:
        dist_text = "、".join(f"{m}({c}次)" for m, c in list(mood_dist.items())[:5])
        parts.append(f"情绪分布：{dist_text}")

    if last_7 or prev_7:
        parts.append(f"近 7 天 {last_7} 次，前 7 天 {prev_7} 次")
        if last_7 > prev_7:
            parts.append("趋势：记录频率上升")
        elif last_7 < prev_7:
            parts.append("趋势：记录频率下降")

    if mood_tag_pairs:
        pairs_text = "；".join(f"「{m}」常和「{t}」同时出现" for m, t in mood_tag_pairs[:3])
        parts.append(f"情绪-标签关联：{pairs_text}")

    return "\n".join(parts)


def _generate_ai_insight(data: dict) -> str:
    prompt = _build_insight_prompt(data)
    if not prompt:
        return ""

    client = get_client()
    if client is None:
        return ""

    try:
        response = client.with_options(timeout=4).chat.completions.create(
            model=DASHSCOPE_MODEL,
            temperature=0,
            max_tokens=160,
            messages=[
                {"role": "system", "content": INSIGHT_PROMPT},
                {"role": "user", "content": prompt},
            ],
        )
        text = (response.choices[0].message.content or "").strip()
        if text:
            safe_print(f"[AI Insight] generated {len(text)} chars for prompt length {len(prompt)}")
            return text
    except Exception as exc:
        safe_print(f"[AI Insight] generation failed: {exc}")

    return ""


def _compute_mood_tag_pairs(records) -> list:
    """Find frequent mood-tag co-occurrences."""
    pairs = []
    for r in records:
        mood = (r.mood or "").strip()
        for tag in _split_tags(r.tags or ""):
            if mood and tag:
                pairs.append((mood, tag))
    if not pairs:
        return []
    counter = Counter(pairs)
    return [{"mood": m, "tag": t} for (m, t), _ in counter.most_common(5)]


def get_insights(db: Session, *, user_id: int, year: int, month: int):
    records = emotion_repository.list_by_user(db, user_id)
    month_start, month_end = _month_range(year, month)
    month_records = [r for r in records if r.record_date and month_start <= r.record_date < month_end]

    today = date.today()
    last_7_start = today - timedelta(days=6)
    prev_7_start = today - timedelta(days=13)
    prev_7_end = today - timedelta(days=7)
    last_7_records = [r for r in records if r.record_date and last_7_start <= r.record_date <= today]
    prev_7_records = [r for r in records if r.record_date and prev_7_start <= r.record_date <= prev_7_end]

    mood_counts = Counter(r.mood for r in month_records if r.mood)
    tag_counts = Counter(tag for r in month_records for tag in _split_tags(r.tags or ""))
    time_counts = Counter(_time_bucket(r.created_at) for r in month_records if _time_bucket(r.created_at))
    active_days = {r.record_date for r in month_records if r.record_date}

    top_mood = mood_counts.most_common(1)[0][0] if mood_counts else ""
    top_tag = tag_counts.most_common(1)[0][0] if tag_counts else ""
    top_time = time_counts.most_common(1)[0][0] if time_counts else ""

    if not month_records:
        return {
            "trend_text": "这个月还没有记录，先留下今天的一小段感受就很好。",
            "ai_insight": "",
            "insights": [
                {"label": "本月记录", "value": "还没有开始"},
                {"label": "建议下一步", "value": "先记录今天"},
            ],
            "suggestion": "不用写很多，选一个最贴近的心情也算开始。",
            "summary": {
                "total_records": 0,
                "active_days": 0,
                "top_mood": "",
                "top_tag": "",
                "top_time": "",
                "last_7_records": len(last_7_records),
                "previous_7_records": len(prev_7_records),
            },
        }

    mood_tag_pairs = _compute_mood_tag_pairs(month_records)
    insight_data = {
        "total_records": len(month_records),
        "active_days": len(active_days),
        "top_mood": top_mood,
        "top_tag": top_tag,
        "top_time": top_time,
        "mood_distribution": dict(mood_counts),
        "mood_tag_pairs": [
            {"mood": pair["mood"], "tag": pair["tag"]}
            for pair in mood_tag_pairs
        ],
        "last_7_records": len(last_7_records),
        "previous_7_records": len(prev_7_records),
    }

    ai_insight = _generate_ai_insight(insight_data)

    if ai_insight:
        trend_text = ai_insight
    else:
        trend_text = f"这个月你记录了 {len(month_records)} 次，最常出现的是「{top_mood}」。"
        if top_tag:
            trend_text += f" 和「{top_tag}」有关的线索比较多。"

    if len(last_7_records) > len(prev_7_records):
        comparison = "比上周更愿意把感受留下来了。"
    elif len(last_7_records) < len(prev_7_records):
        comparison = "这周记录少了一些，也没关系，想到时再写就好。"
    else:
        comparison = "最近的记录节奏比较平稳。"

    insights = [
        {"label": "本月记录", "value": f"{len(month_records)} 次"},
        {"label": "最常出现", "value": top_mood or "暂无"},
        {"label": "记录天数", "value": f"{len(active_days)} 天"},
        {"label": "近 7 天", "value": f"{len(last_7_records)} 次"},
    ]
    if top_time:
        insights.append({"label": "常记录时段", "value": top_time})
    if top_tag:
        insights.append({"label": "高频线索", "value": top_tag})

    return {
        "trend_text": trend_text,
        "ai_insight": ai_insight,
        "insights": insights,
        "suggestion": comparison,
        "summary": {
            "total_records": len(month_records),
            "active_days": len(active_days),
            "top_mood": top_mood,
            "top_tag": top_tag,
            "top_time": top_time,
            "last_7_records": len(last_7_records),
            "previous_7_records": len(prev_7_records),
            "mood_tag_pairs": [
                {"mood": pair["mood"], "tag": pair["tag"]}
                for pair in mood_tag_pairs
            ],
        },
    }
