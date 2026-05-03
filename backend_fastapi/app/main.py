from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect, text

import models
from app.api.router import api_router
from app.core.config import settings
from app.core.database import engine
from app.core.database import SessionLocal
from app.services import common_service
from services.ai.utils import safe_print


def ensure_emotion_record_created_at_column() -> None:
    inspector = inspect(engine)
    columns = {column["name"] for column in inspector.get_columns("emotion_records")}
    if "created_at" in columns:
        return

    dialect = engine.dialect.name
    with engine.begin() as conn:
        if dialect == "mysql":
            conn.execute(text("ALTER TABLE emotion_records ADD COLUMN created_at DATETIME NULL"))
        else:
            conn.execute(text("ALTER TABLE emotion_records ADD COLUMN created_at DATETIME"))
        conn.execute(text("UPDATE emotion_records SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL"))


def ensure_emotion_record_source_column() -> None:
    inspector = inspect(engine)
    columns = {column["name"] for column in inspector.get_columns("emotion_records")}
    if "source" in columns:
        return

    dialect = engine.dialect.name
    with engine.begin() as conn:
        if dialect == "mysql":
            conn.execute(text("ALTER TABLE emotion_records ADD COLUMN source VARCHAR(20) NULL"))
        else:
            conn.execute(text("ALTER TABLE emotion_records ADD COLUMN source VARCHAR(20)"))
        conn.execute(text("UPDATE emotion_records SET source = 'manual' WHERE source IS NULL"))


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, description=settings.app_description)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router)

    @app.on_event("startup")
    def init_database() -> None:
        try:
            models.Base.metadata.create_all(bind=engine)
            ensure_emotion_record_created_at_column()
            ensure_emotion_record_source_column()
            db = SessionLocal()
            try:
                added = common_service.init_greetings(db)
                if added > 0:
                    safe_print(f"[Startup] greetings initialized: +{added}")
                added_home_copy = common_service.init_home_copies(db)
                if added_home_copy > 0:
                    safe_print(f"[Startup] home copies initialized: +{added_home_copy}")
            finally:
                db.close()
        except Exception as exc:
            safe_print(f"[Startup DB Init Warning] {exc}")

    return app


app = create_app()
