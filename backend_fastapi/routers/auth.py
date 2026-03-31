import time
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
import models, schemas
from utils import success_resp, error_resp

router = APIRouter(prefix="/api/auth", tags=["1. 登录与注册"])

@router.post("/register")
def register(req: schemas.RegisterRequest, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.account == req.account).first()
    if db_user:
        return error_resp(code=400, msg="账号已存在")
    
    new_user = models.User(
        account=req.account,
        password=req.password,
        nickname=req.nickname,
        is_guest=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return success_resp(data={"user_id": new_user.id})

@router.post("/login")
def login(req: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.account == req.account,
        models.User.password == req.password
    ).first()
    
    if not user:
        return error_resp(code=400, msg="账号或密码错误")
    return success_resp(data={"user_id": user.id, "nickname": user.nickname, "is_guest": user.is_guest})

@router.post("/guest")
def guest_login(db: Session = Depends(get_db)):
    guest_user = models.User(
        nickname=f"游客{int(time.time())}",
        is_guest=True
    )
    db.add(guest_user)
    db.commit()
    db.refresh(guest_user)
    return success_resp(data={"user_id": guest_user.id, "nickname": guest_user.nickname})
