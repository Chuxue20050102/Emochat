# EmoChat

EmoChat 是一个面向情绪自我觉察的 AI 情绪陪伴与情绪管理系统。项目围绕“说出来、留下来、回看自己”设计，将情绪记录、AI 对话、聊天归档、情绪日历、个人档案和安全兜底串成一个轻量级 AI 应用闭环。

## 项目截图

<p align="center">
  <img src="assets/overview-1.png" alt="EmoChat 项目功能概览上" width="900">
</p>

<p align="center">
  <img src="assets/overview-2.png" alt="EmoChat 项目功能概览下" width="900">
</p>

## 功能概览

- 情绪记录：5 步向导记录情绪等级、原因标签、细分感受和文字描述。
- AI 陪伴对话：结合历史对话、情绪上下文和用户画像生成温和回复。
- 轻量级 Agent 编排：根据用户输入分发到陪伴回复、历史回看、聊天归档等任务。
- 聊天归档：将近期聊天总结为情绪等级、标签和摘要，并写入情绪档案。
- 个人档案：展示累计记录数、AI 近况总结、情绪日历和近期记录。
- 风险兜底：识别自伤、自杀等高风险表达，跳过普通对话流程并返回安全提示。

## 技术栈

- 前端：Vue 3、uni-app、Sass、Vite、H5 / 小程序多端构建
- 后端：FastAPI、SQLAlchemy、Pydantic、MySQL / SQLite、Redis、Pytest
- AI：DashScope / Qwen、OpenAI-compatible API、LangChain memory 相关能力
- 部署：Docker Compose、MySQL 8、Redis 7、natapp 本地隧道（真机调试可选）

## 架构说明

```text
EmoChat/
  frontend_vue/              # uni-app + Vue 3 前端
    pages/index/             # 首页
    pages/emotion-record/    # 情绪记录
    pages/chat/              # AI 聊天
    pages/profile/           # 个人档案
    api/                     # 前端接口封装
    config/                  # 基础配置和情绪配置

  backend_fastapi/           # FastAPI 后端
    app/api/routes/          # 路由层
    app/services/            # 业务服务层
    app/repositories/        # 数据访问层
    app/agent/               # Agent 编排和工具函数
    services/ai/             # AI 调用、Prompt、记忆、安全、归档
    tests/                   # Pytest 测试

  docker-compose.yml         # MySQL / Redis / backend 编排
```

后端采用 `routes / services / repositories` 分层结构。`app/agent` 负责意图识别、任务分发和 trace 记录，`services/ai` 负责模型调用、Prompt、Redis 记忆、风险检测和聊天归档。

核心数据流：

```text
用户输入
-> 风险内容检测
-> 轻量级 Agent 任务分发
-> 读取 Redis 历史 / 情绪上下文
-> 组装 Prompt
-> 调用 Qwen
-> 返回回复 / 查询历史 / 聊天归档
```

## Prompt 与 Vibe

Prompt 位于：

```text
backend_fastapi/services/ai/prompts.py
```

整体 Vibe 是“稳定、共情、克制、低压力”。AI 被设定为情绪陪伴者，而不是心理医生或诊断工具。

主要 Prompt：

- `SYSTEM_PROMPT`：定义陪伴角色，要求真实聊天口吻、短回复、先共情、不诊断。
- `RESPONSE_MODE_PROMPTS`：根据用户状态切换倾听、低压追问、稳定情绪、安全优先等策略。
- `ARCHIVE_PROMPT`：将聊天内容整理为 `mood`、`tags`、`summary`。
- `MEMORY_PROFILE_PROMPT`：从对话中提取长期用户画像，如核心困扰、触发因素和沟通偏好。

回复策略示意：

```text
normal  -> listener   -> 倾听陪伴
sad     -> followup   -> 低压支持
anxious -> stabilize  -> 稳定情绪
crisis  -> safety     -> 安全优先
```

## AI 调用逻辑

项目通过 DashScope 的 OpenAI-compatible API 调用 Qwen，配置位于：

```text
backend_fastapi/services/ai/client.py
backend_fastapi/services/ai/config.py
```

关键环境变量：

```env
DASHSCOPE_API_KEY=your_api_key
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
DASHSCOPE_MODEL=qwen3-vl-32b-thinking
```

模型调用前会组装：

```text
System Prompt
-> 回复策略 Prompt
-> 情绪记录上下文
-> 用户长期画像
-> 最近若干轮历史消息
-> 当前用户输入
```

Agent 主入口：

```http
POST /api/agent/run
```

当前支持：

- `support_chat`：普通陪伴回复
- `emotion_review`：查询最近情绪记录
- `archive_chat`：归档聊天为情绪记录
- `safety`：风险内容兜底

项目没有使用标准 OpenAI function calling。这里的“工具调用”是应用层轻量级编排：识别任务意图后调用 Python 业务函数完成历史查询、聊天归档或回复生成。

后端保留了流式接口：

```http
POST /api/chat/stream
```

该接口基于 `StreamingResponse` 返回 NDJSON；当前聊天页主链路使用非流式 Agent 入口 `/api/agent/run`，并在前端展示 Agent 处理状态。

## 本地运行

后端环境：

```powershell
cd backend_fastapi
py -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

创建 `backend_fastapi/.env`：

```env
DASHSCOPE_API_KEY=your_api_key
DASHSCOPE_MODEL=qwen3-vl-32b-thinking
EMOCHAT_DATABASE_URL=mysql+pymysql://emochat:emochat123@127.0.0.1:3306/emochat?charset=utf8mb4
```

启动依赖和后端：

```powershell
docker compose up -d mysql redis
cd backend_fastapi
python main.py
```

接口文档：

```text
http://127.0.0.1:8000/docs
```

启动前端：

```powershell
cd frontend_vue
npm install
npm run dev:h5
```

构建：

```powershell
npm run build:h5
npm run build:mp-weixin
```

## Docker 部署

一键启动 MySQL、Redis 和后端：

```powershell
docker compose up -d --build
```

默认端口：

```text
backend: 8000
mysql:   3306
redis:   6379
```

如果本机已有其他后端占用 `8000`，可修改 `docker-compose.yml`：

```yaml
ports:
  - "8010:8000"
```

## DNS / HTTPS

真机调试可使用 natapp，将公网域名转发到本机后端端口：

```powershell
.\natapp.exe -authtoken=your_token
```

前端非 H5 环境的接口域名在：

```text
frontend_vue/config/index.js
```

示例：

```js
const LOCAL_IP = 'your-domain.natappfree.cc'
```

生产部署建议使用 Nginx / Caddy 反向代理 FastAPI 服务，并通过 Certbot、Caddy 自动证书或云厂商证书开启 HTTPS。小程序或 App 真机环境需要使用 HTTPS 域名，并在平台后台配置合法请求域名。

## 核心接口

```text
POST /api/auth/register        # 注册
POST /api/auth/login           # 登录
POST /api/auth/guest           # 游客登录

GET  /api/common/greeting      # 首页问候语
GET  /api/emotion/tags         # 情绪配置
POST /api/emotion/record       # 创建情绪记录
GET  /api/emotion/calendar     # 情绪日历
GET  /api/emotion/insights     # 情绪洞察
GET  /api/emotion/history      # 历史记录

POST /api/agent/run            # Agent 入口
GET  /api/agent/traces         # Agent trace
POST /api/chat/archive         # 聊天归档
GET  /api/chat/history         # 聊天历史
GET  /api/chat/memory-profile  # 记忆画像
```

## 测试

```powershell
cd backend_fastapi
.\.venv\Scripts\python.exe -m pytest
```

前端构建验证：

```powershell
cd frontend_vue
npm run build:h5
```

## 项目亮点

- 记录、陪伴、归档、回看形成完整情绪管理闭环。
- 轻量级 Agent 编排清晰，不依赖重型 Agent 框架。
- Redis 对话记忆和结构化用户画像提升上下文连续性。
- Prompt 风格围绕“温和、低压力、短回复”设计。
- 风险内容检测在工具调用前执行，明确安全边界。
