> **💡 提示：** .md文件，可以vscode快捷键Ctrl + Shift + V查看


> **你们只需要修改 `frontend_vue/pages/` 下面的几个子文件夹。（ `pages/chat/` AI 聊天模块除外）**
> `frontend_vue/api/`、`frontend_vue/utils/`、`frontend_vue/components/FloatingTabBar.vue` 已经写好了，不要动。
---

## 🟢 当前现状（你们拿到的是什么）
目前为了方便大家调试视觉效果，前端已开启 **Mock 模式**：
- 接口会秒回“假数据”，**不需要跑后端程序**也能正常点登录、点记录、点日历。
- 你们的任务是 **给毛坯房做精装**（颜色、动效、间距、细节、插图等），先不用担心后端连不上。
- 所有的“精装修”代码请直接在对应的卡片/组件里修改。

---

**核心审美方向参考（写在 `uni.scss` 里已有）剩下自己发挥**：
- 主按钮渐变色：`linear-gradient(135deg, #FF9B8C, #FFB0A4)`
- 卡片底色：半透明白 `rgba(255,255,255,0.65)` + `backdrop-filter: blur(20px)`
- 全局底色：`#FAFCFF`（微微偏蓝白，不刺眼）
- 圆角风格：药丸按钮 `border-radius: 99rpx`，卡片圆角 `40rpx`

---

## ⚠️ 注意事项
1. **图片素材**全部放 `frontend_vue/static/images/` 下，按页面建子文件夹（如 `guide/`、`login/`）
2. **不要改** `api/index.js`、`utils/request.js`、`components/FloatingTabBar.vue`、`App.vue` 这些已定型的公共文件
3. 样式统一用 SCSS（`<style lang="scss" scoped>`），全局变量在 `uni.scss` 里已有定义
