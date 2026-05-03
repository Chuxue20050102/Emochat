import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 默认使用本地 SQLite 文件，也支持通过环境变量覆盖（便于 Docker）
SQLALCHEMY_DATABASE_URL = os.getenv("EMOCHAT_DATABASE_URL", "sqlite:///./emochat.db")

# 仅在 SQLite 下需要 check_same_thread 配置
connect_args = {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
