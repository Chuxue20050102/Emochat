# 项目目录说明

## 根目录
- `backend_fastapi/`：后端服务（FastAPI）
- `frontend_vue/`：前端应用（uni-app + Vue）
- `scripts/`：本地启动/停止脚本
- `docs/`：文档与调试示例
- `docker-compose.yml`：本地基础服务（MySQL、Redis）

## 后端目录（`backend_fastapi`）
- `app/`：分层主实现（当前主代码）
  - `api/routes/`：接口路由层
  - `services/`：业务逻辑层
  - `repositories/`：数据访问层
  - `core/`：配置/数据库/通用能力
- `routers/`：兼容导出层（旧路径兼容）
- `services/ai/`：AI、记忆、安全与归档能力实现
- `tests/`：自动化测试
- `requirements.txt`：Python 依赖

## 前端目录（`frontend_vue`）
- `pages/`：页面
- `components/`：通用组件
- `api/`：接口封装
- `config/`：运行时配置
- `utils/`：请求与工具函数

## docs 目录建议
- `backend/`：后端设计与使用文档
- `frontend/`：前端设计与使用文档
- `common/`：跨端文档（接口、数据设计）
- `examples/`：调试示例请求/样例体
- `部署排障简记.md`：排障历史记录（可持续追加）
- `问题.md`：问题记录与经验沉淀

## 备注
- 运行时数据库文件（`*.db`、`*.db-journal`）已在 `.gitignore` 中忽略。
- 兼容层会逐步收敛，但短期保留以减少重构风险。
