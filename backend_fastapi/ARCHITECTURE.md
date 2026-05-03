# 后端架构说明

## 一、目录结构

```text
backend_fastapi/
  app/
    api/
      router.py
      routes/
        auth.py
        emotion.py
        user.py
        chat.py
        common.py
    core/
      config.py
      database.py
      response.py
      security.py
    repositories/
      user_repository.py
      emotion_repository.py
      greeting_repository.py
      home_copy_repository.py
    services/
      auth_service.py
      emotion_service.py
      user_service.py
      chat_service.py
      common_service.py
  services/
    ai/
      chat.py
      memory.py
      safety.py
      archive.py
  tests/
  models.py
  schemas.py
  database.py
  main.py
```

## 二、分层职责

- `api/routes`：接口层，只处理参数解析、调用服务、包装响应。
- `services`：业务层，编排业务流程和规则，不直接写 SQL。
- `repositories`：数据访问层，负责 SQLAlchemy 查询与持久化。
- `core`：基础能力层，包含配置、数据库依赖、响应工具、安全工具。

## 三、AI 相关模块放置

- `services/ai/`：AI 底层能力（模型调用、记忆、安全、归档、流式输出）。
- `app/agent/`：Agent 编排层，负责意图识别、工具调用和 trace 记录。
- `app/services/chat_service.py`：聊天业务编排（上下文拼装、归档、情绪摘要等）。

这样拆分的好处是：
- AI 能力可以复用，不和接口层耦合。
- 业务逻辑集中在 service，便于测试。
- 路由保持轻量，后续扩展接口成本低。

## 四、当前兼容层说明

- `backend_fastapi/routers/` 下文件为兼容导出层（旧导入路径兼容）。
- 当前主实现在 `backend_fastapi/app/`。
- 兼容层短期保留，后续可逐步收敛。
