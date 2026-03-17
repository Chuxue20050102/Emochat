<template>
  <view class="module-card chat-card" @click="goToChat">
    <view class="chat-content">
      <view class="chat-title">🫧 和我聊聊吧</view>
      <view class="chat-subtitle">不管是什么情绪，我都在听</view>
    </view>
    <view class="chat-arrow">→</view>
  </view>
</template>

<script setup>
const goToChat = () => {
  uni.switchTab({ url: '/pages/chat/index' })
}
</script>

<style lang="scss" scoped>
.module-card {
  background: rgba(255, 255, 255, 0.65);
  backdrop-filter: blur(20px);
  border-radius: 40rpx;
  padding: 50rpx 40rpx;
  box-shadow: 0 16rpx 40rpx rgba(0, 0, 0, 0.03);
  border: 2rpx solid rgba(255, 255, 255, 0.8);
}
.chat-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between; 
  align-items: flex-start; 
  min-height: 320rpx; 
  padding: 50rpx 40rpx;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.8) 0%, rgba(255, 255, 255, 0.5) 100%);
  transition: all 0.3s;
}
.chat-card:active {
  transform: scale(0.98);
}
.chat-content {
  display: flex;
  flex-direction: column;
  gap: 12rpx;
}
.chat-title {
  font-size: 36rpx;
  font-weight: 600;
  color: #1A1A1A;
}
.chat-subtitle {
  font-size: 26rpx;
  color: #666;
}
.chat-arrow {
  align-self: flex-end; 
  width: 88rpx;
  height: 88rpx;
  border-radius: 50%;
  background: linear-gradient(135deg, #FF9B8C, #FFB0A4);
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 42rpx;
  color: #FFF;
  box-shadow: 0 10rpx 26rpx rgba(255, 155, 140, 0.35);
}
</style>
