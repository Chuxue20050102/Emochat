from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.response import success_resp
from app.services import common_service

router = APIRouter(prefix="/api/common", tags=["公共接口"])


@router.get("/greeting")
def get_daily_greeting(db: Session = Depends(get_db)):
    payload = common_service.get_daily_greeting(db)
    return success_resp(data=payload)


@router.post("/init-greetings")
def init_greetings(db: Session = Depends(get_db)):
    created = common_service.init_greetings(db)
    if created == 0:
        return success_resp(msg="问候语已是最新，无需重复初始化")
    return success_resp(msg=f"问候语初始化完成，新增 {created} 条")


@router.get("/home-copy")
def get_home_copy(module: str, state: str = "default", db: Session = Depends(get_db)):
    payload = common_service.get_home_copy(db, module=module, state=state)
    return success_resp(data=payload)


@router.post("/init-home-copy")
def init_home_copy(db: Session = Depends(get_db)):
    created = common_service.init_home_copies(db)
    if created == 0:
        return success_resp(msg="首页语库已是最新，无需重复初始化")
    return success_resp(msg=f"首页语库初始化完成，新增 {created} 条")
