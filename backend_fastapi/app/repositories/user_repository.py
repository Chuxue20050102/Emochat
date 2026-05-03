from typing import Optional

from sqlalchemy.orm import Session

import models


def get_by_account(db: Session, account: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.account == account).first()


def get_by_credentials(db: Session, account: str, password: str) -> Optional[models.User]:
    return (
        db.query(models.User)
        .filter(models.User.account == account, models.User.password == password)
        .first()
    )


def get_by_id(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(
    db: Session,
    *,
    nickname: str,
    account: Optional[str] = None,
    password: Optional[str] = None,
    is_guest: bool = False,
) -> models.User:
    user = models.User(
        account=account,
        password=password,
        nickname=nickname,
        is_guest=is_guest,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: models.User) -> None:
    db.delete(user)
    db.commit()


def update_nickname(db: Session, user: models.User, nickname: str) -> models.User:
    user.nickname = nickname
    db.commit()
    db.refresh(user)
    return user


def update_password(db: Session, user: models.User, password_hash: str) -> models.User:
    user.password = password_hash
    db.commit()
    db.refresh(user)
    return user
