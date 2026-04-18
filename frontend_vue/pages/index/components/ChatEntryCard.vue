<template>
  <view class="module-card chat-card" @click="goToChat">
    <view class="chat-content">
      <view class="chat-text">
        <view class="chat-header">
          <view class="chat-title">🫧 和我聊聊吧</view>
          <view class="chat-subtitle">不管是什么情绪，我都在听</view>
        </view>
        <view class="chat-description">
          开心的事想分享？
          烦恼的事想倾诉？
          或者只是想随便聊聊？
          我在这里，随时准备倾听
        </view>
      </view>
      <view class="chat-image">
        <image src="/static/images/chat-illustration.jpg" mode="aspectFit"></image>
      </view>
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

.chat-card {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
  min-height: 600rpx;
  padding: 60rpx 50rpx;
  background-color: rgba(255, 255, 255, 0.6);
  transition: all 0.3s;
  width: 100%;
  position: relative;
  overflow: hidden;
}
.chat-content {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
  width: 100%;
  flex: 1;
}
.chat-text {
  display: flex;
  flex-direction: column;
  gap: 15rpx;
  width: 100%;
  position: relative;
  z-index: 3;
}
.chat-header {
  display: flex;
  flex-direction: column;
  gap: 6rpx;
}
.chat-title {
  font-size: 40rpx;
  font-weight: 600;
  color: #333;
}
.chat-subtitle {
  font-size: 32rpx;
  color: #666;
}
.chat-description {
  font-size: 28rpx;
  color: #888;
  line-height: 1.5;
  white-space: pre-line;
}
.chat-image {
  position: relative;
  width: 120%;
  height: 360rpx;
  margin-top: 20rpx;
  align-self: flex-start;
  text-align: left;
}
.chat-image image {
  width: 100%;
  height: 100%;
  object-fit: contain;
}
.chat-image::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at center, rgba(255, 255, 255, 0) 0%, rgba(255, 255, 255, 0) 60%, rgba(255, 255, 255, 1) 100%);
  pointer-events: none;
  z-index: 1;
}
.chat-arrow {
  align-self: flex-end; 
  width: 80rpx;
  height: 80rpx;
  border-radius: 50%;
  background: linear-gradient(135deg, #B8E0D2, #98D9C2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32rpx;
  font-weight: 600;
  color: #fff;
  box-shadow: 0 8rpx 20rpx rgba(184, 224, 210, 0.3);
  transition: all 0.3s ease;
  position: relative;
  z-index: 3;
}
.chat-arrow:hover {
  transform: scale(1.1);
  box-shadow: 0 12rpx 28rpx rgba(184, 224, 210, 0.4);
}
</style>
