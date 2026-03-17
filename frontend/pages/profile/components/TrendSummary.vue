<template>
  <view class="trend-summary-card">
    <text class="trend-text">{{ trendText }}</text>
  </view>
</template>

<script setup>
defineProps({
  trendText: { type: String, default: '' }
})
</script>

<style lang="scss" scoped>
.trend-summary-card {
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(10px);
  padding: 30rpx 40rpx;
  border-radius: 30rpx;
  border: 2rpx solid rgba(255,255,255,0.8);
  box-shadow: 0 8rpx 30rpx rgba(0,0,0,0.02);
  margin-bottom: 40rpx;
}
.trend-text {
  font-size: 30rpx;
  color: #1A1A1A;
  font-weight: 500;
}
</style>
