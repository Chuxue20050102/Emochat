> **💡 提示：** .md文件，可以vscode快捷键Ctrl + Shift + V查看

# EmoChat 项目概览与开发规范

本文档面向全组开发人员，旨在帮助大家快速了解项目基本情况、核心业务逻辑以及团队建议的开发规范。

## 1. 项目简介
**EmoChat** 是一款极简、治愈的 AI 情绪陪伴 App（目前为学生期末大作业极速落地版本）。
- **前端技术**: UniApp + Vue3 (Setup 语法) + 全局组件/私有组件分离架构
- **后端技术**: Python 3.8+ + FastAPI + SQLite + **Qwen (通义千问) LLM**
- **UI 风格**: 现代毛玻璃 (Glassmorphism) + 柔和极光渐变 (Aurora Gradients)

## 2. 📚 组员开发必需文档 (按职能分类)

为了让大家开发时不迷路，文档已分类放入专有文件夹：

### 🤝 前后端共用文档 (必看)
- 📄 **`docs/common/02_api_database_design.md`**：【核心！】定义了接口路径、请求体以及数据库的核心表结构。

### 🎨 前端组 (必看)
- 📄 **`docs/TASK_前端组.md`**：**前端组详细任务分工**。
- 📄 **`docs/frontend/03_frontend_guide.md`**：前端架构指南。包含了全局组件与页面私有组件（`components/`）是如何拆分的。
- 📄 **`docs/frontend/04_ui_design_spec.md`**：UI 视觉规范。包含极光渐变背景色、毛玻璃卡片参数标准 CSS 实现。

### ⚙️ 后端组 (必看)
- 📄 **`docs/TASK_后端组.md`**：**后端组详细任务分工**。
- 📄 **`docs/backend/05_backend_architecture.md`** & **`06_backend_guide.md`**：后端架构说明。解释了为何采用 `routers/` + `services/` 分层机制。

---

## 3. 前后端对接现状 (当前状态：本地运行 + Mock 可选 🛠️)

- **✅ 运行环境**：后端项目位于 `backend_fastapi/`，自带 `.venv` 虚拟环境，运行 `python main.py` 即可启动。
- **✅ AI 对话**：后端已集成 AI Service，直接调用大模型 API。
- **✅ Mock 模式**：前端同学如需纯离线 UI 装修，可在 `frontend_vue/utils/request.js` 中开启 `MOCK_MODE`。
- **✅ 一键连接**：UI 优化完成后，将 `MOCK_MODE` 设为 `false` 即可连接真实后端数据库和 AI。
