<template>
  <view class="page-content">
    <view class="hero-gradient page5-bg"></view>
    
    <view class="dynamic-header">
      <text class="top-hint">{{ dynamicContent.hint }}</text>
    </view>

    <view class="illustration-container">
      <image :src="dynamicContent.image" mode="aspectFit" class="illustration-image"></image>
    </view>
    
    <view class="text-section dynamic-text">
      <view class="title">{{ dynamicContent.title }}</view>
      <view class="subtitle" v-html="dynamicContent.subtitle"></view>
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
  dynamicContent: { type: Object, required: true }
})
</script>

<style lang="scss" scoped>
.page-content {
  height: 100%;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
  padding-top: 120rpx; 
}

/* 渐变背景 */
.hero-gradient {
  position: absolute;
  top: -150rpx;
  left: -50rpx;
  width: 130%;
  height: 800rpx;
  filter: blur(50px);
  z-index: 0;
  opacity: 0.85;
}
.page5-bg {
  background: radial-gradient(circle at 20% 20%, #D3F0E6 0%, transparent 50%),
              radial-gradient(circle at 80% 80%, #F6DACD 0%, transparent 50%);
}

.illustration-container {
  position: relative;
  z-index: 1;
  height: 400rpx;
  margin: 20rpx 60rpx;
  border-radius: 40rpx;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  background: transparent;
}
.illustration-image {
  width: 100%;
  height: 100%;
  border-radius: 40rpx;
  opacity: 0.9;
  filter: saturate(0.9) brightness(1.05);
  transition: all 0.3s ease;
  background: transparent;
  mix-blend-mode: soft-light;
}

/* 特性列表 */
.feature-list {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
  margin-top: 30rpx;
  padding: 0 40rpx;
}
.feature-item {
  display: flex;
  align-items: center;
  gap: 16rpx;
  padding: 16rpx 0;
}
.feature-icon {
  font-size: 36rpx;
  width: 48rpx;
  height: 48rpx;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(255, 155, 140, 0.1);
  border-radius: 50%;
}
.feature-text {
  font-size: 28rpx;
  color: #666;
  flex: 1;
  text-align: left;
}

.text-section {
  position: relative;
  z-index: 1;
  padding: 0 60rpx;
  margin-top: auto;
  margin-bottom: 220rpx; 
  text-align: center;
}
.title {
  font-size: 52rpx;
  font-weight: 600;
  color: #1A1A1A;
  line-height: 1.4;
  margin-bottom: 24rpx;
}
.subtitle {
  font-size: 30rpx;
  color: #666;
  line-height: 1.6;
  margin-bottom: 20rpx;
}
.description {
  font-size: 28rpx;
  color: #888;
  line-height: 1.5;
  margin-bottom: 30rpx;
  padding: 0 40rpx;
}
.dynamic-header {
  padding: 0 60rpx;
  text-align: center;
  margin-bottom: 20rpx;
  z-index: 1;
}
.top-hint {
  font-size: 26rpx;
  color: #666;
  font-weight: 500;
}
.dynamic-text {
  margin-bottom: 260rpx;
}
</style>
