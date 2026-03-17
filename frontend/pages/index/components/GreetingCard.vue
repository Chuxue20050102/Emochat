<template>
  <view class="module-card greeting-card">
    <view class="greeting-emoji">☁️</view>
    <view class="greeting-text-area">
      <view class="greeting-title">今天也在慢慢变好</view>
      <view class="greeting-subtitle">"你已经很努力了，不用再逼自己。"</view>
    </view>
  </view>
</template>

<script setup>
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
.greeting-card {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 28rpx;
  padding: 48rpx 40rpx;
  background: rgba(255, 255, 255, 0.45); 
  border-color: rgba(255, 255, 255, 0.5);
}
.greeting-emoji {
  font-size: 64rpx;
  flex-shrink: 0;
}
.greeting-text-area {
  display: flex;
  flex-direction: column;
  gap: 12rpx;
}
.greeting-title {
  font-size: 38rpx;
  font-weight: 700;
  color: #1A1A1A;
  letter-spacing: 1rpx;
}
.greeting-subtitle {
  font-size: 28rpx;
  color: #777;
  line-height: 1.5;
}
</style>
