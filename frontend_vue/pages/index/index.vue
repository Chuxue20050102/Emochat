<template>
  <view class="home-page">
    <view class="hero-gradient"></view>

    <view class="content-wrapper">
      <GreetingCard />
      <EmotionCard />
      <ChatEntryCard />
      <view class="ios-padding-bottom"></view>
    </view>

    <FloatingTabBar currentTab="index" />
  </view>
</template>

<script setup>
import { onShow } from '@dcloudio/uni-app'
import FloatingTabBar from '@/components/FloatingTabBar.vue'
import ChatEntryCard from './components/ChatEntryCard.vue'
import EmotionCard from './components/EmotionCard.vue'
import GreetingCard from './components/GreetingCard.vue'

onShow(() => {
  uni.hideTabBar({ animation: false })
})
</script>

<style lang="scss" scoped>
.home-page {
  min-height: 100vh;
  position: relative;
  padding: 110rpx 30rpx 30rpx;
  overflow: hidden;
}

.hero-gradient {
  position: absolute;
  top: -12%;
  left: -10%;
  right: -10%;
  bottom: -10%;
  z-index: 0;
  filter: blur(80rpx);
  background:
    radial-gradient(circle at 14% 18%, rgba(141, 187, 255, 0.34) 0%, transparent 45%),
    radial-gradient(circle at 84% 16%, rgba(255, 168, 158, 0.34) 0%, transparent 42%),
    radial-gradient(circle at 24% 80%, rgba(132, 219, 194, 0.3) 0%, transparent 42%),
    radial-gradient(circle at 75% 82%, rgba(208, 164, 255, 0.28) 0%, transparent 40%);
}

.content-wrapper {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

.ios-padding-bottom {
  height: 190rpx;
}
</style>
