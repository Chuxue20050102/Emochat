from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import schemas
from app.core.database import get_db
from app.core.response import success_resp
from app.services import user_service

router = APIRouter(prefix="/api/user", tags=["3. 用户信息"])


@router.get("/profile")
def get_profile(user_id: int, db: Session = Depends(get_db)):
    ok, payload = user_service.get_profile(db, user_id)
    if not ok:
        return payload
    return success_resp(data=payload)


@router.delete("/account")
def delete_account(user_id: int, db: Session = Depends(get_db)):
    payload = user_service.delete_account(db, user_id)
    return success_resp(msg=payload["msg"])


@router.post("/nickname")
def update_nickname(req: schemas.UpdateNicknameRequest, db: Session = Depends(get_db)):
    ok, payload = user_service.update_nickname(db, req.user_id, req.nickname)
    if not ok:
        return payload
    return success_resp(data=payload)
