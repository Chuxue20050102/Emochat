# 数据与接口交互规范

这篇文档把**前端和后端怎么传数据（接口文档）**，以及**后端怎么存数据（数据库表）**写在了一起，方便大家对照进行联调开发。

本设计旨在以最轻量级的结构快速跑通核心 AI 交互流，通过精简的 Token 与基础表结构设计，实现**低耦合、易对接、高效率**的开发目标。

---

#> **💡 提示：** .md文件，可以vscode快捷键Ctrl + Shift + V查看

先用 **SQLite** 试试水（Python自带，不需要配置 MySQL 连接啥的，直接生成一个 `.db` 文件就能跑）。一共建两张很简单的表：

### 1. 用户表 `users`
存用户的基本信息和账号密码。

| 字段名称 | 类型 | 说明 | 备注 |
| :------- | :--- | :--- | :--- |
| `id` | INTEGER | 用户ID | **主键**，自增 |
| `account` | VARCHAR(50) | 登录账号 | 唯一索引，账号名 |
| `password` | VARCHAR(100) | 登录密码 | 存储加密或明文密码 |
| `nickname` | VARCHAR(50) | 昵称 | 比如 "孤独的星星" |
| `avatar_url` | VARCHAR(255) | 头像链接 | 可为空 |
| `is_guest` | BOOLEAN | 是否是游客 | 默认为 False，1=游客 |
| `created_at` | DATETIME | 注册时间 | 自动生成 UTC 时间 |

### 2. 情绪打卡记录表 `emotion_records`
用户完成“情绪签到”的数据。

| 字段名称 | 类型 | 说明 | 备注 |
| :------- | :--- | :--- | :--- |
| `id` | INTEGER | 记录ID | **主键**，自增 |
| `user_id` | INTEGER | 用户ID | **外键** 关联 users.id (CASCADE) |
| `mood` | VARCHAR(20) | 心情关键词 | 如：`calm`, `happy`, `sad` |
| `tags` | VARCHAR(255) | 标签字符串 | 逗号分隔，如 `"学习,人际,焦虑"` |
| `description`| TEXT | 感悟随笔 | 详细文字内容 |
| `record_date`| DATE | 签到日期 | 格式 `YYYY-MM-DD` |

### 3. 问候语表 `greetings`
首页随机展示的句子。包含 `id`, `content`, `author` 三个字段。

---

## 📡 第二部分：API 接口设计

### 基础交互说明
- **基础路径 (Base URL)**: 开发的时候一般是 `http://127.0.0.1:8000/api`
- **数据交互**: 前后端统一用 JSON 传数据。
- **登录状态验证**: 我们**不用弄复杂的 JWT Token 验证**。简单化：登录成功后拿到 `user_id`，存在前端的 `uni.setStorageSync` 或 Pinia 里面。后面**调每个接口的时候，直接把 `user_id` 当参数一起传给后端就行了**。

---

### 1. 公共接口 (Common)
- **GET** `/api/common/greeting`
  - 说明：随机获取一条今日问候语。
  - 返回示例：
    ```json
    {
      "code": 200,
      "data": {
        "id": 1,
        "content": "每一朵花都会在属于它的季节绽放，你也是。",
        "author": "EmoChat"
      },
      "msg": "ok"
    }
    ```

### 2. 登录注册相关 `/api/auth`

#### 2.1 注册账号
- **POST** `/api/auth/register`
- **前端发给后端**: `{ "account": "admin", "password": "123", "nickname": "小明" }`
- **后端返回**: 保存到数据库，返回 `{ "code": 200, "data": { "user_id": 1 }, "msg": "ok" }`。

#### 2.2 登录
- **POST** `/api/auth/login`
- **前端发给后端**: `{ "account": "admin", "password": "123" }`
- **后端返回**: `{ "code": 200, "data": { "user_id": 1, "nickname": "小明" }, "msg": "ok" }`。

#### 2.3 游客“先体验”
- **POST** `/api/auth/guest`
- **说明**: 自动创建随机账号。
- **后端返回**: 返回临时身份 `{ "code": 200, "data": { "user_id": 99, "nickname": "游客_xxxx" } }`。

---

### 2. 情绪功能 `/api/emotion`

#### 2.1 提交情绪签到记录
- **POST** `/api/emotion/record`
- **前端发给后端**:
  ```json
  {
    "user_id": 1,
    "mood": "happy",
    "tags": "学习,成就感",
    "description": "今天终于调通了 AI 接口！",
    "record_date": "2026-03-19" 
  }
  ```
- **后端返回**: `{ "code": 200, "msg": "记录成功" }`

#### 2.2 取当月每一天的情绪日历
- **GET** `/api/emotion/calendar?user_id=1&year_month=2026-03`
- **说明**: 用于日历图点渲染。
- **后端返回**:
  ```json
  {
    "code": 200,
    "data": [
      { "date": "2026-03-01", "mood": "calm" },
      { "date": "2026-03-19", "mood": "happy" }
    ]
  }
  ```

#### 2.3 查看某天具体的日记明细
- **GET** `/emotion/detail?user_id=1&date=2026-03-12`
- **后端返回**: 把这一天的心情、tags标签和具体感悟文字全都返回去供弹窗显示。

---

### 3. AI 聊天功能 `/api/chat`

#### 3.1 核心：用户发消息拿 AI 回复
- **POST** `/api/chat/send`
- **前端发给后端**:
  ```json
  {
    "user_id": 1,
    "message": "今天又要熬夜写作业了...",
    "card_record_id": 102 
  }
  ```
- **后端干的事**: 调用通义千问 (Qwen-Plus) -> 存到 Redis 缓存 -> 返回。
- **后端返回**:
  ```json
  {
    "code": 200,
    "data": {
      "reply_msg": "抱抱你，熬夜肯定很累吧，千万要注意休息哦。",
      "is_crisis": false 
    }
  }
  ```

#### 3.2 加载以前的聊天内容（Redis缓存）
- **GET** `/api/chat/history?user_id=1`
- **说明**: 从 Redis 缓存中获取历史聊天记录，缓存有效期为7天。
- **返回**: 列表形式的对话历史。

#### 3.3 清空历史聊天记录
- **DELETE** `/api/chat/history?user_id=1`
- **后端返回**: `{ "code": 200, "msg": "已清空与 AI 的所有回忆" }`

---

### 4. 个人信息 `/api/user`

#### 4.1 获取“我的”页面资料
- **GET** `/api/user/profile?user_id=1`
- **后端返回**: `{ "code": 200, "data": { "nickname": "xxx", "total_days": 10 }, "msg": "ok" }`

#### 4.2 注销账号
- **DELETE** `/api/user/account?user_id=1`
- **后端返回**: `{ "code": 200, "msg": "账号已永久注销" }`
