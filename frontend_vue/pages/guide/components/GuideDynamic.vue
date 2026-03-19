<template>
  <view class="page-content">
    <view class="hero-gradient page5-bg"></view>
    
    <view class="dynamic-header">
      <text class="top-hint">{{ dynamicContent.hint }}</text>
      <view class="title">{{ dynamicContent.title }}</view>
    </view>

    <view class="illustration-placeholder large-placeholder">
      <view class="placeholder-text">{{ dynamicContent.illus }}</view>
    </view>
    
    <view class="text-section dynamic-text">
      <view class="title">{{ dynamicContent.title }}</view>
      <view class="subtitle" v-html="dynamicContent.subtitle"></view>
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

.illustration-placeholder {
  position: relative;
  z-index: 1;
  height: 500rpx;
  margin: 40rpx 60rpx;
  background-color: rgba(255,255,255,0.4);
  border: 2rpx dashed #C7C7CC;
  border-radius: 40rpx;
  display: flex;
  justify-content: center;
  align-items: center;
}
.large-placeholder {
  height: 400rpx;
  margin-top: 20rpx;
}
.placeholder-text {
  color: #888;
  font-size: 28rpx;
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
