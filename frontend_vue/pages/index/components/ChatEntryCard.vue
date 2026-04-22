<template>
  <view class="chat-card" @click="goToChat">
    <view class="text-area">
      <text class="tag">Companion AI</text>
      <text class="title">和我聊聊吧</text>
      <text class="subtitle">不需要整理好语言，你开口我就在</text>
      <text class="desc">开心、委屈、迷茫，或者只是想找人陪你待一会，都可以。</text>
    </view>
    <view class="illustration">
      <image src="/static/images/chat-illustration.jpg" mode="aspectFit"></image>
    </view>
    <view class="arrow">Go</view>
  </view>
</template>

<script setup>
const goToChat = () => {
  uni.switchTab({ url: '/pages/chat/index' })
}
</script>

<style lang="scss" scoped>
.chat-card {
  position: relative;
  overflow: hidden;
  padding: 30rpx;
  border-radius: 34rpx;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.88), rgba(250, 252, 255, 0.66));
  border: 2rpx solid rgba(255, 255, 255, 0.9);
  box-shadow: 0 20rpx 52rpx rgba(42, 56, 92, 0.13);
}

.text-area {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  gap: 10rpx;
}

.tag {
  align-self: flex-start;
  padding: 4rpx 14rpx;
  border-radius: 999rpx;
  font-size: 18rpx;
  color: #35507f;
  background: rgba(141, 187, 255, 0.22);
}

.title {
  font-size: 42rpx;
  font-weight: 700;
  color: #1f2942;
}

.subtitle {
  font-size: 27rpx;
  color: #4f5e79;
}

.desc {
  font-size: 24rpx;
  color: #6d788f;
  line-height: 1.58;
  max-width: 80%;
}

.illustration {
  margin-top: 10rpx;
  height: 250rpx;
  width: 100%;
}

.illustration image {
  width: 100%;
  height: 100%;
}

.arrow {
  position: absolute;
  right: 24rpx;
  bottom: 24rpx;
  width: 78rpx;
  height: 78rpx;
  border-radius: 50%;
  color: #fff;
  font-size: 22rpx;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #8fb8ff 0%, #7ed2bc 100%);
  box-shadow: 0 10rpx 24rpx rgba(103, 162, 202, 0.35);
}
</style>
