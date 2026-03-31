<template>
  <view class="chat-page">
    <!-- 自然柔和的极光背景 -->
    <view class="hero-gradient page-bg"></view>

    <!-- 顶栏标题 -->
    <ChatHeader />

    <!-- 聊天内容区 -->
    <ChatMessageList 
      :chatList="chatList" 
      :isThinking="isThinking" 
      :scrollTopId="scrollTopId" 
    />

    <!-- 底部输入区 -->
    <ChatInputArea @send="sendMessage" />

    <!-- 底部安全留白，避免被浮动导航栏遮挡 -->
    <view class="ios-padding-bottom"></view>
    
    <!-- 使用全局的浮动自定义导航栏 -->
    <FloatingTabBar currentTab="chat" />
  </view>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import FloatingTabBar from '@/components/FloatingTabBar.vue'

import ChatHeader from './components/ChatHeader.vue'
import ChatMessageList from './components/ChatMessageList.vue'
import ChatInputArea from './components/ChatInputArea.vue'

import { sendChatApi } from '@/api/index.js'

const chatList = ref([
  { role: 'assistant', content: '今天想聊点什么，或者只是待一会也可以。' }
])
const isThinking = ref(false)
const scrollTopId = ref('')

onShow(() => {
  uni.hideTabBar({ animation: false })

  // 检查是否从情绪记录页的"和我聊聊这件事"跳过来
  const context = uni.getStorageSync('pendingChatContext')
  if (context) {
    uni.removeStorageSync('pendingChatContext') // 用完即删，防止重复触发

    // 把情绪记录摘要拼成一段自然语言
    let contextMsg = `我刚才记录了"${context.emotion}"的情绪`
    if (context.tags && context.tags.length > 0) {
      contextMsg += `，原因和${context.tags.join('、')}有关`
    }
    if (context.detail && context.detail.length > 0) {
      contextMsg += `，具体感觉是${context.detail.join('、')}`
    }
    if (context.content) {
      contextMsg += `。我写了：${context.content}`
    }

    // 延迟一点再发送，确保页面渲染完成
    setTimeout(() => {
      sendMessage(contextMsg)
    }, 500)
  }
})

const sendMessage = async (text) => {
  if (!text || isThinking.value) return

  // 用户发消息
  chatList.value.push({ role: 'user', content: text })
  scrollToBottom()

  isThinking.value = true

  try {
    const userId = uni.getStorageSync('user_id') || 1001

    const res = await sendChatApi({
      user_id: userId,
      message: text,
      card_record_id: null
    })
    
    // AI回信
    if(res && res.reply_msg) {
      chatList.value.push({ role: 'assistant', content: res.reply_msg })
    }
    scrollToBottom()
  } catch (error) {
    console.error('发送消息失败', error)
    uni.showToast({ title: '网络有些小问题，请稍后再试', icon: 'none' })
  } finally {
    isThinking.value = false
  }
}

const scrollToBottom = async () => {
  await nextTick()
  // 留一点延迟确保渲染完成
  setTimeout(() => {
    scrollTopId.value = 'scroll-bottom'
  }, 100)
}
</script>

<style lang="scss" scoped>
.chat-page {
  height: 100vh;
  position: relative;
  background-color: $emo-bg-base;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 自然柔和的极光背景 */
.hero-gradient {
  position: absolute;
  top: -10%; left: -10%; right: -10%; bottom: -10%;
  z-index: 0;
  filter: blur(60px);
  background: 
    radial-gradient(circle at 15% 30%, rgba(135, 235, 205, 0.4) 0%, transparent 50%),
    radial-gradient(circle at 85% 20%, rgba(255, 179, 167, 0.4) 0%, transparent 50%),
    radial-gradient(circle at 30% 70%, rgba(214, 232, 246, 0.5) 0%, transparent 50%),
    radial-gradient(circle at 75% 85%, rgba(255, 224, 142, 0.4) 0%, transparent 50%);
  transform: scale(1.1);
  pointer-events: none;
}

.ios-padding-bottom {
  height: 220rpx; /* 给悬浮导航留出充足空间 */
  background: rgba(255, 255, 255, 0.6); /* 底部背景统一 */
  backdrop-filter: blur(20px);
  z-index: 1;
}
</style>
