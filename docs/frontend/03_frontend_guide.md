> **💡 提示：** .md文件，可以vscode快捷键Ctrl + Shift + V查看
# 前端开发指南 (Vue3 + UniApp 大作业版)

虽然我们说这是“学生期末大作业版本”，但结构上我们引入了**私有组件切块（Component Splitting）**，这是一个妥妥的企业级规范大动作。

## 1. 文件夹都是干嘛的？ (在哪写代码)

所有的前端代码都在 `frontend` 目录下。

```text
frontend/
├── pages/                  # 🟢 页面入口：
│   ├── guide/index.vue     # 【引导页】介绍APP，含有组件components/GuideDynamic.vue等
│   ├── login/index.vue     # 【登录页】包含components/LoginRegisterForm.vue
│   ├── index/index.vue     # 【首页】分为 问候卡片、情绪模块、AI聊天入口三个子组件
│   ├── chat/index.vue      # 【AI聊天页】待开发...
│   ├── emotion-record/     # 【情绪签到页】
│   │   ├── components/     # -> 它的所有的 5 个步骤都被私有拆分在这里了！
│   │   └── index.vue       # -> 入口页只用200行把它们组合在一起
│   └── profile/index.vue   # 【日历记录页】包含 CalendarBottomSheet 等精细子组件
│
├── api/                    # 🟣 专门发请求找后端的：
│   └── index.js            # 把所有的登录、打卡、月历请求全用 Promise 包在了这
│
├── components/             # 🟡 公共全局组件：
│   └── FloatingTabBar.vue  # 我们没有使用死板丑陋的原生 tabBar，把它做成了全局圆角悬浮导航
│
├── static/                 # 🖼️ 静态资源大本营：
│   └── images/login/       # 所有页面需要的切图全部按页面类别放这里，引用永远用绝对路径 /static/xxx
│
├── utils/                  # 🛠️ 纯工具函数：
│   └── request.js          # 这个文件我已经封装好了 uni.request 拦截器。

## 4. 网络请求与 Mock 模式

项目使用 `utils/request.js` 统一封装请求。为了方便纯前端开发，目前开启了 **Mock 模式**。

- **开关**：在 `utils/request.js` 中修改 `const MOCK_MODE = true`。
- **逻辑**：当为 `true` 时，请求不会发往后端，而是直接从文件内的 `MOCK_DATA` 对象中读取并返回。
- **调试**：控制台会打印 `[Mock] POST /api/auth/login ✅` 样式的日志。
- **注意**：开发 UI 时请保持开启，提交代码前**不要**关闭此开关。

└── pages.json              # ⚙️ 路由：只要你新建了一个页面，来这注册一行代码！全局去掉了导航条。
```

## 2. 小组开发大白话约束 (关于 API 和 状态存取)
1. **统一的游客与登录态维持**：无需复杂的 Vuex / Pinia，登录或者点击“游客体验”之后，我们将后端返回的 `user_id` 和 `nickname` 立即使用 `uni.setStorageSync` 固化在本地。
2. **所有组件去中心化调用**：现在比如在 `pages/profile` 里面，要请求月历数据，不需要繁琐的层层传递。我们在页面里的 `<script setup>` `onShow` 时，直接 `uni.getStorageSync('user_id')`，然后调用 `@/api/index.js` 发给后端，丝滑无比。
3. **彻底治愈的组件封装**：像打卡的“五个步骤”，或者月历的渲染，绝对不要再堆砌几千行 `index.vue` 代码了。
   - 如果是一个页面专有的，就像现在的 `emotion-record/components/` 一样建**私有组件**。
   - 如果是多个页面都要用的（比如悬浮 TabBar），就在全局 `frontend/components/` 里面写。
