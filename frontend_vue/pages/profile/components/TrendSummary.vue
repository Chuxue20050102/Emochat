<template>
  <view class="trend-summary-card">
    <text class="trend-tag">Monthly Insight</text>
    <text class="trend-text">{{ trendText }}</text>
  </view>
</template>

<script setup>
defineProps({
  trendText: { type: String, default: '' },
})
</script>

<style lang="scss" scoped>
.trend-summary-card {
  margin-top: 14rpx;
  margin-bottom: 18rpx;
  padding: 22rpx 24rpx;
  border-radius: 28rpx;
  background: rgba(255, 255, 255, 0.75);
  border: 2rpx solid rgba(255, 255, 255, 0.88);
  box-shadow: 0 12rpx 34rpx rgba(43, 53, 89, 0.12);
}

.trend-tag {
  display: inline-block;
  padding: 4rpx 12rpx;
  border-radius: 999rpx;
  font-size: 18rpx;
  color: #39588c;
  background: rgba(141, 187, 255, 0.23);
}

.trend-text {
  margin-top: 10rpx;
  display: block;
  font-size: 28rpx;
  line-height: 1.55;
  color: #25314d;
}
</style>
