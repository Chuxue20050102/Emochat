from typing import Iterable, List

from sqlalchemy.orm import Session

import models


def list_by_module(db: Session, module: str) -> List[models.HomeCopy]:
    return db.query(models.HomeCopy).filter(models.HomeCopy.module == module).all()


def list_by_module_and_state(db: Session, module: str, state: str) -> List[models.HomeCopy]:
    return (
        db.query(models.HomeCopy)
        .filter(models.HomeCopy.module == module, models.HomeCopy.state == state)
        .all()
    )


def bulk_insert(db: Session, items: Iterable[models.HomeCopy]) -> None:
    db.add_all(list(items))
    db.commit()
