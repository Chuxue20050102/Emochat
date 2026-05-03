# EmoChat

EmoChat 是一个面向情绪自我觉察的 AI 陪伴 Agent 应用。项目围绕“说出来、留下来、回看自己”设计，支持用户记录每日情绪、与 AI 进行温和对话、将聊天内容归档为情绪记录，并在个人档案页回看自己的情绪线索。

这个项目既可以作为本科毕业设计，也适合作为 Agent 应用开发方向的简历项目。它不是单纯的聊天 Demo，而是把 AI 对话、工具调用、情绪档案、历史回看和安全兜底串成了一个完整闭环。

## 核心功能

- 情绪记录：用户可以选择情绪、补充标签和文字内容，形成每日情绪记录。
- AI 聊天陪伴：聊天页提供温和的情绪陪伴回复，支持结合上下文继续聊。
- Agent 工具调用：后端 Agent 会根据用户意图决定是否执行聊天回复、历史情绪检索、聊天归档等工具。
- 聊天归档：用户可以把一段重要聊天整理成情绪档案，进入后续回看。
- 个人档案：展示 AI 近况总结、本月概览、情绪日历、最近记录。
- 情绪日历：按日期回看记录，并可带着某条记录继续聊天。
- 首页情绪氛围卡：根据用户记录状态和后端语库展示个性化情绪氛围语。
- 危机内容兜底：命中危机表达时跳过普通 Agent 工具调用，优先返回安全提示。

## 用户闭环

```text
首页情绪氛围
  -> 快速记录今天情绪
  -> 进入 AI 聊天
  -> 保存重要聊天为情绪记录
  -> 档案页查看日历和近况总结
  -> 带着某条记录继续聊
```

这个闭环让项目从“记录工具”变成了“有记忆的情绪陪伴 Agent”。

## Agent 设计

后端 Agent 入口为 `/api/agent/run`，核心实现位于：

```text
backend_fastapi/app/agent/agent_service.py
backend_fastapi/app/agent/tools.py
backend_fastapi/app/services/chat_service.py
backend_fastapi/services/ai/
```

Agent 当前支持三类主要意图：

- `support_chat`：普通情绪陪伴聊天。
- `emotion_review`：查询并总结最近情绪记录。
- `archive_chat`：将最近聊天整理并写入情绪档案。

工具能力包括：

- `get_emotion_history`：读取用户最近情绪记录。
- `archive_chat_to_emotion`：把聊天归档为结构化情绪记录。
- `chat_reply`：结合记忆和上下文生成陪伴回复。

前端会临时展示 Agent 的处理状态，例如“正在认真读你说的话”“正在参考你留下的线索”。最终回复生成后，内部过程提示会收起，避免长期打扰用户。

## 危机内容处理

项目实现了安全优先的危机内容兜底机制。

当前策略是一层判断：

```text
crisis：命中危机表达
none：未命中危机表达
```

处理流程：

1. 用户发送消息。
2. 后端 Agent 在 Planner 和工具调用之前先执行危机检测。
3. 如果命中危机表达，直接返回安全支持话术。
4. 此时不会调用历史检索、聊天归档或普通聊天工具。
5. 前端展示安全回复，并弹出“心理援助提醒”。

核心文件：

```text
backend_fastapi/services/ai/safety.py
backend_fastapi/app/agent/agent_service.py
frontend_vue/pages/chat/index.vue
```

当前项目采用“关键词硬拦截 + 安全提示 + Agent 工具跳过”的方案。这样做的优点是稳定、可解释、适合毕业设计和中小型项目展示。

对于隐晦表达，推荐后续扩展为混合方案：

- 第一层：关键词硬拦截，处理明确危机表达。
- 第二层：低落/焦虑状态识别，调整回复策略但不弹危机提示。
- 第三层：可选的 LLM 风险分类器，对隐晦表达做二次判断。
- 第四层：记录安全 trace，便于调试和审计。

也就是说，不是完全依赖关键词，而是在工程上先保证明确危机场景不会漏过，再逐步补充模型分类能力。

## 技术栈

前端：

- Vue 3
- uni-app
- Sass
- H5 / 小程序多端构建

后端：

- FastAPI
- SQLAlchemy
- MySQL / SQLite
- Redis
- OpenAI-compatible API / DashScope
- LangChain memory 相关能力
- Pytest

部署与本地服务：

- Docker Compose
- MySQL
- Redis
- FastAPI backend

## 目录结构

```text
EmoChat/
  frontend_vue/              # uni-app 前端
    pages/index/             # 首页三张卡片
    pages/chat/              # AI 聊天页
    pages/profile/           # 情绪档案页
    pages/emotion-record/    # 情绪记录页
    api/                     # 前端接口封装
    config/                  # 情绪配置和基础配置

  backend_fastapi/           # FastAPI 后端
    app/api/routes/          # 路由层
    app/agent/               # Agent 编排和工具
    app/services/            # 业务服务
    app/repositories/        # 数据访问层
    services/ai/             # AI、记忆、安全、归档能力
    tests/                   # 后端测试

  docker-compose.yml         # MySQL / Redis / backend 编排
```

## 本地运行

### 1. 启动后端依赖

```bash
docker compose up -d mysql redis
```

如果需要连同后端一起启动：

```bash
docker compose up -d --build
```

### 2. 后端本地开发

```bash
cd backend_fastapi
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

后端默认运行在：

```text
http://127.0.0.1:8000
```

接口文档：

```text
http://127.0.0.1:8000/docs
```

### 3. 初始化后端语库

首次部署或更新首页文案后，需要调用：

```http
POST /api/common/init-greetings
POST /api/common/init-home-copy
```

这两个接口会写入或同步首页问候语、首页卡片文案等种子数据。

### 4. 前端运行

```bash
cd frontend_vue
npm install
npm run dev:h5
```

H5 开发环境会通过代理访问本地后端。

构建 H5：

```bash
npm run build:h5
```

## 关键接口

首页：

```text
GET /api/common/greeting
GET /api/common/home-copy
GET /api/emotion/history
GET /api/emotion/insights
```

情绪记录：

```text
POST /api/emotion/record
GET  /api/emotion/history
GET  /api/emotion/calendar
GET  /api/emotion/detail
GET  /api/emotion/insights
```

聊天与 Agent：

```text
POST /api/agent/run
GET  /api/agent/traces
POST /api/chat/archive
GET  /api/chat/emotion-history
GET  /api/chat/memory-profile
```

## 项目亮点

- 不只是 AI 聊天，而是将对话、记录、归档和回看做成了完整产品闭环。
- Agent 支持意图识别和工具调用，能根据用户请求检索情绪历史或归档聊天。
- 前端交互围绕“温度感”设计，弱化机械按钮感，强调情绪陪伴氛围。
- 档案页将 AI 总结、月度数据、情绪日历和最近记录进行模块化整合。
- 危机内容在 Agent 工具调用前被拦截，避免继续执行普通对话链路。
- 后端采用 routes / services / repositories 分层，便于测试和维护。
- 首页和聊天页文案支持后端语库配置，方便后续做运营化调整。

## 简历写法参考

项目名称：

```text
EmoChat：基于情绪记忆与工具调用的 AI 情绪陪伴 Agent
```

项目描述：

```text
设计并实现一个面向情绪自我觉察的 AI 陪伴 Agent 应用，支持情绪记录、AI 对话、聊天归档、情绪日历回看和个人档案分析。后端基于 FastAPI 实现 Agent 编排，通过意图识别调用情绪历史检索、聊天归档和陪伴回复等工具；前端基于 uni-app 构建多端页面，并围绕情绪陪伴场景优化交互文案和视觉层级。
```

可写进简历的要点：

- 实现 Agent 意图识别与工具调用流程，支持 `support_chat`、`emotion_review`、`archive_chat` 等场景。
- 设计聊天归档链路，将自然语言对话总结为结构化情绪记录，并接入档案页回看。
- 构建情绪日历和最近记录继续聊功能，实现“记录-回看-继续对话”的上下文闭环。
- 接入对话记忆和用户情绪档案，使 AI 回复能够结合历史线索。
- 实现危机表达安全兜底，在工具调用前拦截风险内容并返回援助提示。
- 对首页、聊天页、档案页进行产品化打磨，优化文案温度感、模块职责和视觉层级。

## 测试

后端测试：

```bash
cd backend_fastapi
.venv\Scripts\python.exe -m pytest
```

Agent 相关测试：

```bash
cd backend_fastapi
.venv\Scripts\python.exe -m pytest tests\test_agent_eval.py
```

前端构建验证：

```bash
cd frontend_vue
npm run build:h5
```

## 后续优化方向

- 为危机内容增加 LLM 风险分类器，补充隐晦表达识别。
- 增加本地化心理援助资源配置，例如校园心理中心、地区热线等。
- 为 Agent trace 增加可视化调试页，方便展示工具调用路径。
- 为首页和档案页增加更多端到端测试。
- 将首页文案语库扩展为可运营配置后台。
