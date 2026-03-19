> **💡 提示：** .md文件，可以vscode快捷键Ctrl + Shift + V查看

# 📄 后端开发细节指南
 (Python + FastAPI)

当前后端基于非常轻量的单体模块化组织，项目目录为 `backend_fastapi/`（PyCharm 初始化，含 `.venv` 虚拟环境）。所有业务逻辑直接写在 `routers/` 里的各个文件中（如 `auth.py`, `emotion.py`, `user.py`, `common.py`）。

## 1. 新增一个接口的完整步骤

假设我们要给“用户”模块加一个“修改昵称”的接口。

**第一步：去 `schemas.py` 定义前端传来的参数格式**
```python
class UpdateNameRequest(BaseModel):
    user_id: int
    new_nickname: str
```

**第二步：去 `routers/user.py` 写逻辑**
```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from utils import success_resp, error_resp

@router.put("/nickname")
def update_nickname(req: schemas.UpdateNameRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == req.user_id).first()
    if not user:
        return error_resp(msg="用户不存在")
    
    user.nickname = req.new_nickname
    db.commit()
    return success_resp(msg="修改成功")
```

**第三步：保存即可，FastAPI 热更新会立刻生效！**
去浏览器打开 `http://127.0.0.1:8000/docs` 就能直接在 Swagger 页面里点 `Try it out` 测试你新写的接口。

## 2. 数据库注意点
1. **自动建表**: `main.py` 启动时执行了 `models.Base.metadata.create_all(bind=engine)`，所以修改了 `models.py` 里的字段后，SQLite 不会自动帮你更新列。如果有大规模字段变动，学生作业期间最简单的方法是**直接把 `backend_fastapi/emochat.db` 删掉**，重新运行 `python main.py` 让它重建新库。
2. **依赖注入**: 所有操作数据库的函数接口里，统一接收 `db: Session = Depends(get_db)` 作为参数，这样能保证发完请求后自动关闭连接。

## 3. 下一步 AI 模块建议
后续如果要接入真实的大模型（如 DeepSeek）：
- 尽量在 `routers/chat.py` 中写调用第三方 API 的请求，而不是阻塞在 `main.py`。
- 如果请求 AI 需要十几秒，前端最好做好骨架屏或者 `uni.showLoading` 相应的等待。
