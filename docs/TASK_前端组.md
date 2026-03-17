> **💡 提示：** .md文件，可以vscode快捷键Ctrl + Shift + V查看

# 🎨 前端组任务书（共 2 人）

> **你们只需要关心 `frontend/pages/` 下面的几个子文件夹。**
> `frontend/api/`、`frontend/utils/`、`frontend/components/FloatingTabBar.vue` 已经写好了，不要动。
> `pages/chat/` 是楚雪负责的 AI 聊天模块，**不要碰**。

---

## 🟢 当前现状（你们拿到的是什么）

目前为了方便大家调试视觉效果，前端已开启 **Mock 模式**：
- 接口会秒回“假数据”，**不需要跑后端程序**也能正常点登录、点记录、点日历。
- 你们的任务是 **给毛坯房做精装**（颜色、动效、间距、细节、插图等），先不用担心后端连不上。
- 所有的“精装修”代码请直接在对应的卡片/组件里修改。

---

## 📋 任务总表

### 前端同学 A：负责「引导页 + 登录页」

你只需改以下路径下的文件：

| 文件路径 | 当前状态 | 你的任务 |
|:---|:---|:---|
| `pages/guide/index.vue` | 有 5 页 swiper 滑动引导，极光渐变背景，**但前 3 页的插图是虚线框占位符** | ① 把 3 个虚线框换成真正的插图（图放 `static/images/guide/` 下，用 `<image src="/static/images/guide/xxx.png" />`）；② 优化文案排版间距 |
| `pages/guide/components/GuideSelection.vue` | 第 4 页"你想做什么"三选一卡片 | 美化选中态（比如加阴影放大 / 增加边框主题色高亮） |
| `pages/guide/components/GuideDynamic.vue` | 第 5 页动态结果页 | 同样的插图占位需要替换 |
| `pages/login/index.vue` | 有极光背景 + 顶部插图，功能完整 | ① 整体登录页审美润色（间距、阴影、配色细节）|
| `pages/login/components/LoginRegisterForm.vue` | 登录/注册表单卡片，功能完整 | ② 输入框聚焦态样式优化；③ 登录/注册 tab 指示条动画 |
| `pages/login/components/GuestSection.vue` | "先体验"游客按钮 | ③ 按钮样式对齐整体主题 |

**核心审美方向参考（写在 `uni.scss` 里已有）**：
- 主按钮渐变色：`linear-gradient(135deg, #FF9B8C, #FFB0A4)`
- 卡片底色：半透明白 `rgba(255,255,255,0.65)` + `backdrop-filter: blur(20px)`
- 全局底色：`#FAFCFF`（微微偏蓝白，不刺眼）
- 圆角风格：药丸按钮 `border-radius: 99rpx`，卡片圆角 `40rpx`

---

### 前端同学 B：负责「首页 + 档案页 + 情绪记录页」

你只需改以下路径下的文件：

| 文件路径 | 当前状态 | 你的任务 |
|:---|:---|:---|
| **首页** |||
| `pages/index/index.vue` | 主框架页（极光背景 + 三卡片排列），结构完整 | 调整三张卡片之间的间距、整体间距呼吸感 |
| `pages/index/components/GreetingCard.vue` | "今天也在慢慢变好"问候卡 | 增强卡片视觉层次（比如微渐变底色、增加细微阴影）；**注意：文案先在代码里写死几条随机展示，后面要接后端，用后端语料库** |
| `pages/index/components/EmotionCard.vue` | 7 个 Emoji 选择 + 选中反馈 | ① Emoji 选中态放大缩放自然度；② 选中后展示结果的入场动画 |
| `pages/index/components/ChatEntryCard.vue` | "和我聊聊吧"入口卡片 | 优化主题渐变高亮，右下角箭头按钮美化 |
| **档案页** |||
| `pages/profile/index.vue` | 框架页 | 大背景视觉优化（可以加极光渐变，参考 index 页） |
| `pages/profile/components/ProfileHeader.vue` | 头像 + 昵称 + 火苗勋章 | 头像渐变环、昵称排版优化 |
| `pages/profile/components/TrendSummary.vue` | "这个月大多是平静的🌿"一句话卡片 | 卡片样式增强 |
| `pages/profile/components/EmotionCalendar.vue` | 情绪月历（可翻月，带彩色圆点） | ① 今日日期的高亮样式；② 情绪圆点的色彩表现力加强 |
| `pages/profile/components/CalendarBottomSheet.vue` | 点击日期弹出的底部抽屉 | 抽屉拉出动画、内部排版润色 |
| **情绪记录页** |||
| `pages/emotion-record/index.vue` | 四步 swiper，功能完整，已对接 API | 顶部进度条样式、底部按钮样式统一 |
| `pages/emotion-record/components/Step1Mood.vue` | 7 个大 Emoji 横滑选择 | 选中态辉光动效（已有 `glowColor`，增强表现） |
| `pages/emotion-record/components/Step2Reason.vue` | 原因标签多选 | 标签选中态配色增强 |
| `pages/emotion-record/components/Step3SubTags.vue` | 情绪细化标签 | 同上 |
| `pages/emotion-record/components/Step4FreeInput.vue` | 文字输入框 | 输入框样式美化 |
| `pages/emotion-record/components/Step5Feedback.vue` | 记录完成反馈卡 | 完成页入场动效优化 |

---

## ⚠️ 注意事项

1. **图片素材**全部放 `frontend/static/images/` 下，按页面建子文件夹（如 `guide/`、`login/`）
2. **不要改** `api/index.js`、`utils/request.js`、`components/FloatingTabBar.vue`、`App.vue` 这些已定型的公共文件
3. **不要碰** `pages/chat/` 目录——这是楚雪的 AI 模块
4. 样式统一用 SCSS（`<style lang="scss" scoped>`），全局变量在 `uni.scss` 里已有定义
5. 提交代码前先在 HBuilderX 预览确认不影响现有功能
