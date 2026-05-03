from typing import Iterable, List

from sqlalchemy.orm import Session

import models


def list_all(db: Session) -> List[models.Greeting]:
    return db.query(models.Greeting).all()


def has_any(db: Session) -> bool:
    return db.query(models.Greeting).first() is not None


def bulk_insert(db: Session, items: Iterable[models.Greeting]) -> None:
    db.add_all(list(items))
    db.commit()

