<template>
  <view class="header">
    <text class="subtitle">不用整理好再说，想到什么就说什么。</text>
  </view>
</template>

<script setup>
</script>

<style lang="scss" scoped>
.header {
  position: relative;
  z-index: 1;
  padding: 100rpx 40rpx 40rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12rpx;
}

.subtitle {
  font-size: 26rpx;
  color: $emo-text-sub;
}
</style>
