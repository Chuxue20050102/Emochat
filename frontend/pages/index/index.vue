<template>
  <view class="home-page">
    <!-- 自然柔和的极光背景 -->
    <view class="hero-gradient page-bg"></view>

    <view class="content-wrapper">
      <!-- 模块1: 今日问候 (不可点击) -->
      <GreetingCard />

      <!-- 模块2: 情绪选择 (核心交互) -->
      <EmotionCard />

      <!-- 模块3: AI情绪陪伴入口 (温柔陪伴方案) -->
      <ChatEntryCard />

      <!-- 底部安全留白，避免被浮动导航栏遮挡 -->
      <view class="ios-padding-bottom"></view>
    </view>

    <!-- 使用全局的浮动自定义导航栏 -->
    <FloatingTabBar currentTab="index" />
  </view>
</template>

<script setup>
import { onShow } from '@dcloudio/uni-app'
import FloatingTabBar from '@/components/FloatingTabBar.vue'
import GreetingCard from './components/GreetingCard.vue'
import EmotionCard from './components/EmotionCard.vue'
import ChatEntryCard from './components/ChatEntryCard.vue'

onShow(() => {
  // 原生 tabBar 在各端情况不同，我们通过调用 hideTabBar 让视觉只留下自定义的浮动圆角栏
  uni.hideTabBar({ animation: false })
})
</script>

<style lang="scss" scoped>
.home-page {
  min-height: 100vh;
  position: relative;
  background-color: #FAFCFF;
  padding: 140rpx 40rpx 60rpx;
  overflow: hidden;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
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

.content-wrapper {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  gap: 40rpx;
  flex: 1;
}

.ios-padding-bottom {
  height: 200rpx; /* 安全留白 */
}
</style>
