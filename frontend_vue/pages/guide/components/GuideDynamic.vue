<template>
  <view class="page-content">
    <view class="hero-gradient page5-bg"></view>

    <view class="dynamic-header">
      <text class="top-hint">{{ dynamicContent.hint }}</text>
    </view>

    <view class="illustration-container">
      <image :src="dynamicContent.image" mode="aspectFill" class="illustration-image"></image>
    </view>

    <view class="text-section">
      <view class="title">{{ dynamicContent.title }}</view>
      <view class="subtitle">{{ dynamicContent.subtitle }}</view>
      <view class="description" v-if="dynamicContent.description">{{ dynamicContent.description }}</view>
      <view class="feature-list" v-if="dynamicContent.features">
        <view class="feature-item" v-for="(feature, index) in dynamicContent.features" :key="index">
          <view class="feature-icon">{{ feature.icon }}</view>
          <view class="feature-text">{{ feature.text }}</view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
defineProps({
  dynamicContent: { type: Object, required: true },
})
</script>

<style lang="scss" scoped>
.page-content {
  height: 100%;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
  padding-top: 90rpx;
}

.hero-gradient {
  position: absolute;
  inset: -12% -10% auto -10%;
  height: 780rpx;
  filter: blur(70rpx);
  z-index: 0;
}

.page5-bg {
  background: radial-gradient(circle at 20% 30%, rgba(141, 187, 255, 0.35) 0%, transparent 55%),
    radial-gradient(circle at 78% 66%, rgba(255, 177, 166, 0.35) 0%, transparent 55%);
}

.dynamic-header {
  position: relative;
  z-index: 1;
  text-align: center;
}

.top-hint {
  font-size: 24rpx;
  color: #65728f;
}

.illustration-container {
  position: relative;
  z-index: 1;
  margin: 24rpx 44rpx 0;
  height: 370rpx;
  border-radius: 34rpx;
  overflow: hidden;
  box-shadow: 0 20rpx 38rpx rgba(39, 52, 92, 0.14);
}

.illustration-image {
  width: 100%;
  height: 100%;
}

.text-section {
  position: relative;
  z-index: 1;
  margin-top: 24rpx;
  padding: 0 46rpx;
  text-align: center;
}

.title {
  font-size: 50rpx;
  font-weight: 700;
  color: #1d2740;
}

.subtitle {
  margin-top: 14rpx;
  font-size: 28rpx;
  color: #5b6683;
  line-height: 1.5;
}

.description {
  margin-top: 12rpx;
  font-size: 24rpx;
  color: #6d7891;
  line-height: 1.55;
}

.feature-list {
  margin-top: 20rpx;
  display: flex;
  flex-direction: column;
  gap: 10rpx;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 10rpx;
  padding: 10rpx 18rpx;
  border-radius: 999rpx;
  background: rgba(255, 255, 255, 0.64);
}

.feature-icon {
  width: 42rpx;
  height: 42rpx;
  border-radius: 50%;
  background: rgba(143, 184, 255, 0.22);
  color: #355481;
  font-size: 20rpx;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

.feature-text {
  font-size: 24rpx;
  color: #56627f;
  text-align: left;
}
</style>
