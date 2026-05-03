from sqlalchemy.orm import Session

from app.core.response import error_resp
from app.repositories import emotion_repository, user_repository


def get_profile(db: Session, user_id: int):
    user = user_repository.get_by_id(db, user_id)
    if not user:
        return False, error_resp(msg='用户不存在')

    total_records = emotion_repository.count_by_user(db, user_id)
    return True, {'nickname': user.nickname, 'total_records': total_records}


def delete_account(db: Session, user_id: int):
    user = user_repository.get_by_id(db, user_id)
    if user:
        user_repository.delete_user(db, user)
    return {'msg': '账号及其相关数据已删除'}


def update_nickname(db: Session, user_id: int, nickname: str):
    user = user_repository.get_by_id(db, user_id)
    if not user:
        return False, error_resp(msg='用户不存在')

    normalized = str(nickname or '').strip()
    if not normalized:
        return False, error_resp(msg='昵称不能为空')
    if len(normalized) > 20:
        return False, error_resp(msg='昵称不能超过20个字符')

    user_repository.update_nickname(db, user, normalized)
    return True, {'user_id': user.id, 'nickname': user.nickname}
