> **💡 提示：** .md文件，可以vscode快捷键Ctrl + Shift + V查看

# ⚙️ 后端组

> **你们只需要关心 `backend_fastapi/routers/` 下的 `.py` 文件和 `backend_fastapi/schemas.py`。**
> `main.py`、`database.py`、`models.py`、`utils.py` 已经写好了，一般不需要动。
> `routers/chat.py` 是 AI 模块agent开发部分，其他部分写完的话，这部分感兴趣可以尝试一下。

---

## 🟢 当前现状（你们拿到的是什么）

后端使用 Python + FastAPI + SQLite，已经AI生成了大概，需要测试是否能跑通。项目目录为 `backend_fastapi/`（PyCharm 初始化，含虚拟环境）。运行方式：
```bash
cd backend_fastapi
# 激活虚拟环境（PyCharm 会自动激活，或手动执行）
.venv\Scripts\activate
python main.py
```
启动后浏览器打开 `http://127.0.0.1:8000/docs`，就能看到自动生成的 Swagger 接口文档，可以直接点 Try it out 测试。

> **📢 开发提示：**
> 为了让前端组专心搞视觉优化，前端目前切到了 `MOCK_MODE`（离线假数据）。
> 后端同学请先通过 `http://127.0.0.1:8000/docs` 自行测试接口功能，确保代码逻辑正确。等前端精装修完，我们会统一连上。

---

## 📂 你们只需关注的文件

```
backend_fastapi/
├── routers/           ← 【主战场！你的代码写在这里】
│   ├── auth.py          认证接口
│   ├── emotion.py       情绪记录接口
│   └── user.py          用户档案接口
│
├── schemas.py         ← 【如果要加新接口参数，在这里加 class】
│
├── models.py          ← 理解表结构用，一般不改
├── utils.py           ← 只有 success_resp / error_resp 两个函数，不改
└── database.py        ← 数据库连接配置，不改
```

---

## 📋 任务总表：调通现有接口（核心目标）AI划分的任务，你们自行协商。自己记住完成了什么部分，给老师的文档要填具体的分工技术部分

目前的后端代码已具备基本框架，但仍有一些逻辑漏洞或对接细节需要你们**调通并验证**。

### 「用户与认证模块」调通
**涉及文件：** `routers/auth.py` + `routers/user.py`

任务是确保用户能正常注册、登录，并获取到个人信息：

1. **注册接口调通** (`/api/auth/register`)：目前注册成功后只返回了 `user_id`，请确保同时返回 `nickname`（数据库里有这个字段）。
2. **登录接口逻辑验证** (`/api/auth/login`)：测试一下账号不存在、密码错误时，是否正确返回了错误提示。
3. **档案接口验证** (`/api/user/profile`)：确保能根据 `user_id` 正确查出用户的昵称。

---

### 「情绪记录与语料库模块」调通
**涉及文件：** `routers/emotion.py` + `routers/common.py`

任务是确保情绪数据能存得进去，并且首页能随机展示语录：

1. **打卡接口调通** (`/api/emotion/record`)：确保前端传来的 `mood`, `tags`, `description` 能正确存入 `EmotionRecord` 表。
2. **日历接口验证** (`/api/emotion/calendar`)：确保能根据年月（如 2026-03）返回该用户当月的所有打卡记录。
3. **语料库接口实现** (`/api/common/greeting`)：
   - 这是给首页模块 1 提供的“今日问候语”。
   - 需要从 `greetings` 表随机取一条返回；如果表为空，需返回一行默认文案防止前端报错（参考代码示例已写在 `common.py`）。
   - **进阶建议**：可以自己在数据库手动塞几条温暖的话进去测试效果。


---

## 🛠️ 怎么叫“调通”？（调试流程）

1. **启动服务**：在 `backend_fastapi` 目录下激活 `.venv` 后运行 `python main.py`。
2. **打开 Swagger**：访问 `http://127.0.0.1:8000/docs`。
3. **模拟测试**：
   - 点开接口展开 -> 点击 **Try it out**。
   - 输入参数 -> 点击 **Execute**。
   - 查看 **Server response**。如果返回的 `code` 是 200 且数据格式符合 `common/02_api_database_design.md` 的约定，就算调通。


## ⚠️ 注意事项

1. 所有接口返回格式统一用 `success_resp(data={...})` 或 `error_resp(msg="...")`（在 `utils.py` 里定义好了）
2. 前端传参方式：POST 请求用 JSON body，GET 请求用 query 参数（如 `?user_id=1&year=2026`）
3. 如果新增了字段想改表结构（`models.py`），最简单的方法是**删掉 `emochat.db`** 再重新运行 `python main.py`，它会自动重建新库
4. 写完后在 `http://127.0.0.1:8000/docs` 先自己测一遍，确保 200 返回正常
