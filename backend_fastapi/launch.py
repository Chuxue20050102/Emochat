import sys
import os

# 在导入任何模块之前，先修补sys.modules
# 这样当其他模块尝试导入asyncio时，会使用我们的假模块
class FakeAsyncio:
    class WindowsSelectorEventLoopPolicy:
        pass
    
    @staticmethod
    def set_event_loop_policy(policy):
        pass

# 将假的asyncio模块放入sys.modules
sys.modules['asyncio'] = FakeAsyncio()

# 现在导入其他模块
try:
    import uvicorn
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from database import engine
    import models
    
    # 初始化建表
    models.Base.metadata.create_all(bind=engine)
    
    # 创建FastAPI应用
    app = FastAPI(
        title="EmoChat 极简架构版 API", 
        description="采用了分层 Router 路由架构进行代码组织，结构更清晰易拓展。"
    )
    
    # 配置跨域
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 导入路由模块
    from routers import auth, emotion, user, chat, common
    
    # 挂载路由
    app.include_router(auth.router)
    app.include_router(emotion.router)
    app.include_router(user.router)
    app.include_router(chat.router)
    app.include_router(common.router)
    
    # 运行服务器
    if __name__ == "__main__":
        uvicorn.run("launch:app", host="0.0.0.0", port=8000, reload=True)
        
except Exception as e:
    print(f"启动失败: {e}")
    import traceback
    traceback.print_exc()
