from datetime import date
from typing import List

from sqlalchemy import desc
from sqlalchemy.orm import Session

import models


def create_record(
    db: Session,
    *,
    user_id: int,
    mood: str,
    source: str = "manual",
    tags: str = "",
    description: str = "",
    record_date: date,
) -> models.EmotionRecord:
    record = models.EmotionRecord(
        user_id=user_id,
        mood=mood,
        source=source,
        tags=tags,
        description=description,
        record_date=record_date,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def count_by_user(db: Session, user_id: int) -> int:
    return db.query(models.EmotionRecord).filter(models.EmotionRecord.user_id == user_id).count()


def list_by_user(db: Session, user_id: int) -> List[models.EmotionRecord]:
    return (
        db.query(models.EmotionRecord)
        .filter(models.EmotionRecord.user_id == user_id)
        .order_by(desc(models.EmotionRecord.record_date), desc(models.EmotionRecord.created_at), desc(models.EmotionRecord.id))
        .all()
    )


def list_by_user_and_date(
    db: Session,
    *,
    user_id: int,
    target_date: date,
) -> List[models.EmotionRecord]:
    return (
        db.query(models.EmotionRecord)
        .filter(
            models.EmotionRecord.user_id == user_id,
            models.EmotionRecord.record_date == target_date,
        )
        .order_by(desc(models.EmotionRecord.created_at), desc(models.EmotionRecord.id))
        .all()
    )


def list_paginated(
    db: Session,
    *,
    user_id: int,
    page: int,
    page_size: int,
    mood: str = "",
):
    query = db.query(models.EmotionRecord).filter(models.EmotionRecord.user_id == user_id)
    if mood:
        query = query.filter(models.EmotionRecord.mood == mood)

    total = query.count()
    records = (
        query.order_by(desc(models.EmotionRecord.record_date), desc(models.EmotionRecord.created_at), desc(models.EmotionRecord.id))
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return total, records
