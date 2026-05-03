<template>
  <view class="guest-section">
    <button class="emo-btn-ghost guest-btn" @click="$emit('guest')">先体验看看</button>
    <view class="guest-hint">先体验一下，之后也可以再创建账号</view>
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
  padding-top: 36rpx;
}

.guest-btn {
  width: 100%;
}

.guest-hint {
  margin-top: 14rpx;
  font-size: 23rpx;
  color: #7f8aa0;
}
</style>
