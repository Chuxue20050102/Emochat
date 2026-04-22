from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import date, datetime

from database import get_db
import models, schemas
from utils import success_resp, error_resp

router = APIRouter(prefix="/api/emotion", tags=["2. 情绪功能"])

@router.post("/record")
def create_record(req: schemas.RecordRequest, db: Session = Depends(get_db)):
    r_date = req.record_date or date.today()
    record = models.EmotionRecord(
        user_id=req.user_id,
        mood=req.mood,
        tags=req.tags,
        description=req.description,
        record_date=r_date
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return success_resp(data={"record_id": record.id})

@router.get("/calendar")
def get_calendar(user_id: int, year: int, month: int, db: Session = Depends(get_db)):
    records = (
        db.query(models.EmotionRecord)
        .filter(models.EmotionRecord.user_id == user_id)
        .order_by(desc(models.EmotionRecord.record_date), desc(models.EmotionRecord.id))
        .all()
    )
    calendar_data = {}
    for r in records:
        if r.record_date and r.record_date.year == year and r.record_date.month == month:
            date_str = r.record_date.strftime("%Y-%m-%d")
            if date_str not in calendar_data:
                calendar_data[date_str] = {"mood": r.mood, "count": 0}
            calendar_data[date_str]["count"] += 1
    return success_resp(data=calendar_data)

@router.get("/detail")
def get_emotion_detail(user_id: int, date_str: str, db: Session = Depends(get_db)):
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return error_resp(msg="日期格式必须为 YYYY-MM-DD")
        
    records = (
        db.query(models.EmotionRecord)
        .filter(
            models.EmotionRecord.user_id == user_id,
            models.EmotionRecord.record_date == target_date
        )
        .order_by(desc(models.EmotionRecord.id))
        .all()
    )
    
    if not records:
        return success_resp(data=[])
        
    res_data = [
        {
            "id": r.id,
            "mood": r.mood,
            "tags": r.tags,
            "description": r.description,
            "record_date": str(r.record_date)
        } for r in records
    ]
    return success_resp(data=res_data)


@router.get("/history")
def get_emotion_history(
    user_id: int = Query(..., description="用户ID"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    mood: str = Query("", description="按情绪筛选，可选"),
    db: Session = Depends(get_db),
):
    query = db.query(models.EmotionRecord).filter(models.EmotionRecord.user_id == user_id)
    if mood:
        query = query.filter(models.EmotionRecord.mood == mood)

    total = query.count()
    records = (
        query.order_by(desc(models.EmotionRecord.record_date), desc(models.EmotionRecord.id))
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return success_resp(
        data={
            "total": total,
            "page": page,
            "page_size": page_size,
            "records": [
                {
                    "id": r.id,
                    "mood": r.mood,
                    "tags": r.tags or "",
                    "description": r.description or "",
                    "record_date": str(r.record_date),
                }
                for r in records
            ],
        }
    )
