#> **💡 提示：** .md文件，可以vscode快捷键Ctrl + Shift + V查看

# ⚙️ EmoChat 后端大本营 (架构指北)

为了让期末大作业的后端代码既标准规范，又好改好交差，我们采用了 **“轻量级 Router 模块分层架构”**。放弃了企业里复杂的 Controller/Service/DAO 三层结构，一切为了“好懂、好对接”。

## 1. 目录结构说明

```text
backend_fastapi/
├── main.py          👉 【核心入口】
│                       创建 FastAPI 实例，挂载跨域中间件 (CORS)，并引入 routers/ 下的所有模块。
│
├── routers/         👉 【路由层：只负责接口定义】
│   ├── auth.py        - 登录、注册、游客模式接口。
│   ├── emotion.py     - 提交打卡、获取月历数据接口。
│   ├── user.py        - 获取用户档案统计接口。
│   ├── chat.py        - 聊天接口（调用 services/ai_service.py 处理）。
│   └── common.py      - 公共接口模块（如语料库）。
│
├── services/        👉 【逻辑层：负责干活/调用 AI】
│   ├── ai_service.py  - 对接大模型 API，处理 Prompt 和对话逻辑。
│   └── __init__.py    - 包初始化文件。
│
├── database.py      👉 【数据库引擎】
├── models.py        👉 【数据表模型 (SQLAlchemy)】
├── schemas.py       👉 【数据校验 (Pydantic)】
├── utils.py         👉 【公共工具】 (success_resp / error_resp)
├── requirements.txt 👉 【依赖清单】
└── emochat.db       👉 【SQLite 数据库文件】
```

## 2. 开发协作优势

哪怕整个小组都在改后端，只要你们修改的是不同的功能模块，**Git 提交绝对不会撞车冲突！**
- 比如你想修改登录逻辑，只去 `backend_fastapi/routers/auth.py`。
- 想增加月历判断逻辑，只去 `backend_fastapi/routers/emotion.py`。
- 主文件 `main.py` 极其干净，只有几十行。
