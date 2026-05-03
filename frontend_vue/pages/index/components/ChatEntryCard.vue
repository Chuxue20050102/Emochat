<template>
  <view class="chat-entry-card" @click="goChat">
    <image class="chat-image" src="/static/images/chat-illustration.jpg" mode="widthFix"></image>

    <view class="chat-content">
      <view class="chat-copy">
        <text class="title">想说的时候，我在这里。</text>
        <text class="desc">不用整理好语言，带着现在的感觉开始就可以。</text>
      </view>

      <view class="chat-action">
        <text class="action-text">开始聊天</text>
      </view>
    </view>
  </view>
</template>

<script setup>
const goChat = () => {
  uni.switchTab({ url: '/pages/chat/index' })
}
</script>

<style lang="scss" scoped>
.chat-entry-card {
  padding: 18rpx;
  border-radius: 36rpx;
  overflow: hidden;
  background:
    linear-gradient(135deg, rgba(237, 250, 243, 0.92), rgba(255, 246, 232, 0.9)),
    radial-gradient(circle at 96% 0%, rgba(143, 184, 160, 0.22), transparent 42%);
  border: 2rpx solid rgba(255, 255, 255, 0.92);
  box-shadow: 0 22rpx 60rpx rgba(83, 62, 45, 0.1);
}

.chat-image {
  display: block;
  width: 100%;
  border-radius: 28rpx;
}

.chat-content {
  padding: 24rpx 10rpx 8rpx;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 22rpx;
}

.chat-copy {
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.eyebrow {
  width: fit-content;
  padding: 6rpx 14rpx;
  border-radius: 999rpx;
  font-size: 20rpx;
  font-weight: 700;
  color: $emo-sage-text;
  background: rgba(255, 255, 255, 0.68);
}

.title {
  margin-top: 14rpx;
  font-size: 34rpx;
  font-weight: 900;
  line-height: 1.35;
  color: $emo-text-main;
}

.desc {
  margin-top: 8rpx;
  font-size: 23rpx;
  line-height: 1.5;
  color: $emo-text-sub;
}

.chat-action {
  flex-shrink: 0;
  min-width: 152rpx;
  height: 72rpx;
  padding: 0 26rpx;
  border-radius: 999rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #365f4d;
  background: rgba(255, 255, 255, 0.72);
  border: 1rpx solid rgba(143, 184, 160, 0.42);
}

.action-text {
  font-size: 23rpx;
  font-weight: 800;
}
</style>
