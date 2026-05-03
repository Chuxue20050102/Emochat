import time

from sqlalchemy.orm import Session

import schemas
from app.core.response import error_resp
from app.core.security import hash_password, is_hashed_password, verify_password
from app.repositories import user_repository


def register(db: Session, req: schemas.RegisterRequest):
    exists = user_repository.get_by_account(db, req.account)
    if exists:
        return False, error_resp(msg='账号已存在')

    user = user_repository.create_user(
        db,
        account=req.account,
        password=hash_password(req.password),
        nickname=req.nickname,
        is_guest=False,
    )
    return True, {'user_id': user.id, 'nickname': user.nickname}


def login(db: Session, req: schemas.LoginRequest):
    user = user_repository.get_by_account(db, req.account)
    if not user or not user.password:
        return False, error_resp(msg='账号或密码错误')

    if not verify_password(req.password, user.password):
        return False, error_resp(msg='账号或密码错误')

    # Backward compatibility: upgrade legacy plaintext password after successful login.
    if not is_hashed_password(user.password):
        user_repository.update_password(db, user, hash_password(req.password))

    return True, {'user_id': user.id, 'nickname': user.nickname, 'is_guest': user.is_guest}


def guest_login(db: Session):
    user = user_repository.create_user(
        db,
        nickname=f'游客{int(time.time())}',
        is_guest=True,
    )
    return {'user_id': user.id, 'nickname': user.nickname}
