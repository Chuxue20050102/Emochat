<template>
  <view class="feedback-page fade-in">
    <view class="feedback-card">
      <text class="feedback-icon">🌿</text>
      <view class="feedback-title">已记录</view>
      <view class="feedback-desc">你刚刚认真地感受了自己，这很好。</view>
      
      <view class="action-buttons">
        <button class="primary-btn action-btn" @click="$emit('goChat')">和我聊聊这件事 →</button>
        <text class="cancel-text" @click="$emit('goHome')">完成，回首页</text>
      </view>
    </view>
  </view>
</template>

<script setup>
defineEmits(['goChat', 'goHome'])
</script>

<style lang="scss" scoped>
.feedback-page {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 0 60rpx;
  margin-top: -100rpx;
}
.feedback-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border-radius: 50rpx;
  padding: 100rpx 50rpx 80rpx;
  width: 100%;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  box-shadow: 0 40rpx 80rpx rgba(135, 235, 205, 0.15);
  border: 4rpx solid rgba(255,255,255,0.8);
}
.feedback-icon {
  font-size: 120rpx;
  margin-bottom: 30rpx;
  text-shadow: 0 20rpx 40rpx rgba(135, 235, 205, 0.6);
}
.feedback-title {
  font-size: 44rpx;
  font-weight: 600;
  color: #1A1A1A;
  margin-bottom: 24rpx;
}
.feedback-desc {
  font-size: 30rpx;
  color: #666;
  margin-bottom: 80rpx;
  line-height: 1.6;
}
.action-buttons {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  gap: 30rpx;
}
.action-btn {
  width: 100%;
}
.primary-btn {
  width: 100%;
  height: 100rpx;
  border-radius: 50rpx;
  background: linear-gradient(135deg, #FF9B8C, #FFB0A4);
  color: #FFF;
  font-size: 32rpx;
  font-weight: 600;
  letter-spacing: 2rpx;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 12rpx 30rpx rgba(255, 176, 164, 0.4);
}
.primary-btn:active {
  transform: scale(0.98);
}
.cancel-text {
  font-size: 28rpx;
  color: #999;
  padding: 20rpx;
}
.fade-in {
  animation: fadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(40rpx) scale(0.95); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
</style>
