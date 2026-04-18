<template>
  <view class="module-card greeting-card">
    <view class="greeting-emoji">🌱</view>
    <view class="greeting-text-area">
      <view class="greeting-title">慢慢来，你的情绪都能被看见</view>
    </view>
  </view>
</template>

<script setup>
</script>

<style lang="scss" scoped>

.greeting-card {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 28rpx;
  padding: 24rpx 40rpx;
  background: rgba(255, 255, 255, 0.6); 
  border-color: rgba(255, 255, 255, 0.7);
  transition: all 0.3s ease;
  min-height: 140rpx;
  height: 140rpx;
}
.greeting-card:hover {
  transform: translateY(-4rpx);
  box-shadow: 0 20rpx 48rpx rgba(0, 0, 0, 0.06);
  background: rgba(255, 255, 255, 0.7);
  border-color: rgba(255, 255, 255, 0.8);
}
.greeting-emoji {
  font-size: 64rpx;
  flex-shrink: 0;
}
.greeting-text-area {
  display: flex;
  flex-direction: column;
  gap: 12rpx;
  flex: 1;
}
.greeting-title {
  font-size: 42rpx;
  font-weight: 700;
  color: #5D4037;
  letter-spacing: 3rpx;
  text-align: center;
  text-shadow: 1rpx 1rpx 3rpx rgba(0, 0, 0, 0.1);
  font-family: 'SimSun', '宋体', serif;
  line-height: 1.3;
  padding: 10rpx 0;
  transform: skew(-2deg);
  width: 100%;
}
</style>
