from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import schemas
from app.core.database import get_db
from app.core.response import success_resp
from app.services import auth_service

router = APIRouter(prefix="/api/auth", tags=["1. 登录与注册"])


@router.post("/register")
def register(req: schemas.RegisterRequest, db: Session = Depends(get_db)):
    ok, payload = auth_service.register(db, req)
    if not ok:
        return payload
    return success_resp(data=payload)


@router.post("/login")
def login(req: schemas.LoginRequest, db: Session = Depends(get_db)):
    ok, payload = auth_service.login(db, req)
    if not ok:
        return payload
    return success_resp(data=payload)


@router.post("/guest")
def guest_login(db: Session = Depends(get_db)):
    payload = auth_service.guest_login(db)
    return success_resp(data=payload)
