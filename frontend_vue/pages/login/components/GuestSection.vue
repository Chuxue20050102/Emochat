<template>
  <view class="guest-section">
    <button class="guest-btn" @click="$emit('guest')">先体验</button>
    <view class="guest-hint">在未登录的情况下体验核心功能</view>
  </view>
</template>

<script setup>
defineEmits(['guest'])
</script>

<style lang="scss" scoped>
.guest-section {
  position: relative;
  z-index: 1;
  width: 630rpx;
  margin-top: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 80rpx;
}
.guest-btn {
  width: 100%;
  height: 90rpx;
  border-radius: 45rpx;
  background: linear-gradient(135deg, #FF9B8C, #FFB0A4);
  color: #FFF;
  font-size: 32rpx;
  font-weight: 500;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 10rpx 28rpx rgba(255, 155, 140, 0.4);
}
.guest-btn:active {
  transform: scale(0.98);
}
.guest-hint {
  font-size: 24rpx;
  color: #999;
  text-align: center;
  margin-top: 24rpx;
}
</style>
