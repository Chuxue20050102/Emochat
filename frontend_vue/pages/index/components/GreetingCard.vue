<template>
  <view class="greeting-card emo-fade-up">
    <view class="halo"></view>
    <view class="title">欢迎回来</view>
    <view class="desc">今天的感受，也值得被认真对待</view>
  </view>
</template>

<script setup>
</script>

<style lang="scss" scoped>
.greeting-card {
  position: relative;
  overflow: hidden;
  padding: 34rpx 36rpx;
  border-radius: 34rpx;
  background: rgba(255, 255, 255, 0.72);
  border: 2rpx solid rgba(255, 255, 255, 0.85);
  box-shadow: 0 14rpx 40rpx rgba(45, 57, 93, 0.12);
}

.halo {
  position: absolute;
  width: 360rpx;
  height: 360rpx;
  right: -120rpx;
  top: -210rpx;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 175, 167, 0.45) 0%, rgba(255, 175, 167, 0) 70%);
}

.title {
  position: relative;
  z-index: 1;
  font-size: 42rpx;
  font-weight: 700;
  letter-spacing: 1rpx;
  color: #20283c;
}

.desc {
  position: relative;
  z-index: 1;
  margin-top: 8rpx;
  font-size: 27rpx;
  color: #5e6881;
}
</style>
