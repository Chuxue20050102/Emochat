from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 使用本地 SQLite 数据库文件
SQLALCHEMY_DATABASE_URL = "sqlite:///./emochat.db"

# connect_args={"check_same_thread": False} 是 SQLite 特有的配置，用于防止多线程错误
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
