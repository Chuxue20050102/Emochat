import os
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from database import get_db
import models
from utils import success_resp, error_resp

router = APIRouter(prefix="/api/user", tags=["3. 此账号信息"])

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads", "avatars")
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def validate_file(file: UploadFile) -> str:
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"不支持的文件格式，允许的格式: {', '.join(ALLOWED_EXTENSIONS)}")
    return ext

@router.post("/avatar")
async def update_avatar(user_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return error_resp(msg="用户不存在")
    
    try:
        ext = validate_file(file)
        
        content = await file.read()
        if len(content) > MAX_FILE_SIZE:
            return error_resp(msg="文件大小不能超过 5MB")
        
        filename = f"{uuid.uuid4().hex}{ext}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        
        with open(filepath, "wb") as f:
            f.write(content)
        
        avatar_url = f"/static/avatars/{filename}"
        user.avatar_url = avatar_url
        db.commit()
        
        return success_resp(data={"avatar_url": avatar_url}, msg="头像更新成功")
    
    except HTTPException:
        raise
    except Exception as e:
        return error_resp(msg=f"上传失败: {str(e)}")

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
