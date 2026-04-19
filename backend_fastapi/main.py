import asyncio
import sys
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine
import models

# ==== 导入拆分好的路由模块 ====
from routers import auth, emotion, user, chat, common

# 初始化建表（如果不存表则自动根据 models.py 建表）
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EmoChat 极简架构版 API", 
    description="采用了分层 Router 路由架构进行代码组织，结构更清晰易拓展。"
)

# 配置跨域，允许前端调用
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==== 挂载所有模块的 API 路由 ====
app.include_router(auth.router)
app.include_router(emotion.router)
app.include_router(user.router)
app.include_router(chat.router)
app.include_router(common.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
