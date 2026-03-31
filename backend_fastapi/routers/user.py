from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
import models
from utils import success_resp, error_resp

router = APIRouter(prefix="/api/user", tags=["3. 此账号信息"])

@router.get("/profile")
def get_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return error_resp(msg="用户不存在")
    total_records = db.query(models.EmotionRecord).filter(models.EmotionRecord.user_id == user_id).count()
    return success_resp(data={"nickname": user.nickname, "total_records": total_records})

@router.delete("/account")
def delete_account(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return success_resp(msg="账号及一切痕迹已彻底注销")
