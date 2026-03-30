from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, datetime

# 假设你的项目根包是 backend_fastapi
from .. import models, schemas
from ..database import get_db
from ..utils import success_resp, error_resp

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
    records = db.query(models.EmotionRecord).filter(models.EmotionRecord.user_id == user_id).all()
    calendar_data = {}
    for r in records:
        if r.record_date and r.record_date.year == year and r.record_date.month == month:
            date_str = r.record_date.strftime("%Y-%m-%d")
            if date_str not in calendar_data:
                calendar_data[date_str] = r.mood
    return success_resp(data=calendar_data)

@router.get("/detail")
def get_emotion_detail(user_id: int, date_str: str, db: Session = Depends(get_db)):
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return error_resp(msg="日期格式必须为 YYYY-MM-DD")
        
    records = db.query(models.EmotionRecord).filter(
        models.EmotionRecord.user_id == user_id, 
        models.EmotionRecord.record_date == target_date
    ).all()
    
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
