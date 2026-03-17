<template>
  <view class="page-content selection-page">
    <view class="header-section">
      <view class="skip-btn" @click="$emit('skip')">Skip</view>
      <view class="title-main">开始之前<br>想了解一下你的需求</view>
      <view class="subtitle-main">选择一个最接近你当前需求的方向</view>
    </view>
    
    <view class="options-container">
      <view class="option-card green-card" :class="{'selected': selectedNeed === 'record'}" @click="$emit('select', 'record')">
        <view class="option-title">情绪整理</view>
        <view class="option-desc">想记录和整理自己的情绪</view>
      </view>
      
      <view class="option-card purple-card" :class="{'selected': selectedNeed === 'chat'}" @click="$emit('select', 'chat')">
        <view class="option-title">放松与陪伴</view>
        <view class="option-desc">希望有一个地方聊天和倾诉</view>
      </view>
      
      <view class="option-card blue-card" :class="{'selected': selectedNeed === 'understand'}" @click="$emit('select', 'understand')">
        <view class="option-title">了解自己</view>
        <view class="option-desc">想更好地理解自己的内心</view>
      </view>
    </view>
  </view>
</template>

<script setup>
defineProps({
  selectedNeed: { type: String, default: 'record' }
})
defineEmits(['select', 'skip'])
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
.selection-page {
  padding-top: 100rpx;
}
.header-section {
  padding: 0 60rpx;
  position: relative;
}
.skip-btn {
  position: absolute;
  top: 0;
  right: 60rpx;
  font-size: 30rpx;
  color: #999;
}
.title-main {
  font-size: 56rpx;
  font-weight: 600;
  color: #1A1A1A;
  line-height: 1.4;
  margin-top: 60rpx;
  margin-bottom: 20rpx;
}
.subtitle-main {
  font-size: 28rpx;
  color: #666;
  margin-bottom: 60rpx;
}
.options-container {
  padding: 0 50rpx;
  display: flex;
  flex-direction: column;
  gap: 30rpx;
}
.option-card {
  height: 140rpx;
  border-radius: 99rpx; 
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border: 4rpx solid transparent;
  transition: all 0.3s ease;
}
.option-title {
  font-size: 34rpx;
  font-weight: 600;
  color: #1A1A1A;
  margin-bottom: 8rpx;
}
.option-desc {
  font-size: 24rpx;
  color: #666;
}
.green-card { background-color: #E2F5EE; }
.purple-card { background-color: #EFE8FA; }
.blue-card { background-color: #E2F0F9; }

.option-card.selected {
  border-color: #FFB3A7;
  transform: scale(1.02);
  box-shadow: 0 10rpx 30rpx rgba(255, 179, 167, 0.3);
}
</style>
