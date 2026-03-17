#> **💡 提示：** .md文件，可以vscode快捷键Ctrl + Shift + V查看

# ⚙️ EmoChat 后端大本营 (架构指北)

为了让期末大作业的后端代码既标准规范，又好改好交差，我们采用了 **“轻量级 Router 模块分层架构”**。放弃了企业里复杂的 Controller/Service/DAO 三层结构，一切为了“好懂、好对接”。

## 1. 目录结构说明

```text
backend/
├── main.py          👉 【核心入口】
│                       创建 FastAPI 实例，挂载跨域中间件 (CORS)，并引入 routers/ 下的所有模块。
│
├── routers/         👉 【业务路由分组】（写接口逻辑的核心区！）
│   ├── auth.py        - 登录、注册、游客模式接口。
│   ├── emotion.py     - 提交打卡、获取月历数据、获取详情接口。
│   ├── user.py        - 获取用户档案统计接口。
│   ├── common.py      - 公共接口模块（如语料库/今日问候语）。
│   └── chat.py        - 假装 AI 聊天的接口（未来接入大模型就在这里扩写）。
│
├── database.py      👉 【数据库引擎】
│                       配置并连接本地 SQLite 数据库（emochat.db），提供 get_db 的依赖注入。
│
├── models.py        👉 【数据表模型 (SQLAlchemy)】
│                       利用 ORM 思想，在这里把 users、emotion_records、chat_messages、greetings 定义成 Python Class。
│
├── schemas.py       👉 【数据校验 (Pydantic)】
│                       定义前端传过来的入参必须包含什么字段，返回给前端出参的统一格式。
│
├── utils.py         👉 【公共工具】
│                       封装了 success_resp 和 error_resp 统一返回 {code, data, msg} 格式。
│
├── requirements.txt 👉 【依赖清单】
│                       pip install -r requirements.txt 一键安装。
│
└── emochat.db       👉 【真实数据库文件】
                        自动生成的 SQLite 库，直接用 Navicat 就可以打开看数据。
```

## 2. 开发协作优势

哪怕整个小组都在改后端，只要你们修改的是不同的功能模块，**Git 提交绝对不会撞车冲突！**
- 比如你想修改登录逻辑，只去 `routers/auth.py`。
- 想增加月历判断逻辑，只去 `routers/emotion.py`。
- 主文件 `main.py` 极其干净，只有几十行。
