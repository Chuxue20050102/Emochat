<template>
  <view class="emotion-card">
    <view v-if="!selectedEmotion" class="unselected-state">
      <view class="emotion-title">这一刻，你更接近哪一种心情？</view>
      <view class="emoji-list">
        <view v-for="item in emotionItems" :key="item.name" class="emoji-item" @click="handleSelect(item)">
          <text class="emoji-icon">{{ item.emoji }}</text>
          <text class="emoji-label">{{ item.name }}</text>
        </view>
      </view>
    </view>

    <view v-else class="selected-state emo-fade-up">
      <view class="selected-top">
        <view class="emoji-glow">{{ selectedEmotion.emoji }}</view>
        <view class="selected-meta">
          <text class="selected-name">{{ selectedEmotion.name }}</text>
          <text class="selected-desc">谢谢你认真感受自己，我们把它温柔地记录下来。</text>
        </view>
      </view>

      <view class="action-buttons">
        <button class="emo-btn-primary primary-btn" @click="goToRecord">记录此刻</button>
        <button class="emo-btn-ghost secondary-btn" @click="cancelSelection">重新选择</button>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'
import { emotionList } from '@/config/emotionConfig.js'

const selectedEmotion = ref(null)
const emotionItems = emotionList || []

const handleSelect = (item) => {
  selectedEmotion.value = item
}

const cancelSelection = () => {
  selectedEmotion.value = null
}

const goToRecord = () => {
  if (selectedEmotion.value) {
    uni.setStorageSync('preSelectedEmotion', selectedEmotion.value.name)
  }
  uni.switchTab({ url: '/pages/emotion-record/index' })
}
</script>

<style lang="scss" scoped>
.emotion-card {
  padding: 28rpx;
  border-radius: 34rpx;
  background: rgba(255, 255, 255, 0.76);
  border: 2rpx solid rgba(255, 255, 255, 0.9);
  box-shadow: 0 18rpx 48rpx rgba(42, 56, 96, 0.12);
}

.emotion-title {
  font-size: 31rpx;
  font-weight: 600;
  color: #202a41;
  margin-bottom: 20rpx;
}

.emoji-list {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12rpx;
}

.emoji-item {
  border-radius: 20rpx;
  background: rgba(247, 250, 255, 0.95);
  border: 2rpx solid rgba(225, 233, 249, 0.95);
  min-height: 106rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2rpx;
}

.emoji-icon {
  font-size: 34rpx;
}

.emoji-label {
  font-size: 19rpx;
  color: #68738c;
  max-width: 92%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.selected-state {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

.selected-top {
  display: flex;
  gap: 18rpx;
  align-items: center;
}

.emoji-glow {
  width: 106rpx;
  height: 106rpx;
  border-radius: 26rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48rpx;
  background: linear-gradient(135deg, rgba(255, 185, 178, 0.45), rgba(151, 197, 255, 0.42));
  box-shadow: 0 10rpx 20rpx rgba(149, 169, 211, 0.2);
}

.selected-meta {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8rpx;
}

.selected-name {
  font-size: 35rpx;
  font-weight: 700;
  color: #1d2438;
}

.selected-desc {
  font-size: 24rpx;
  color: #62708a;
  line-height: 1.45;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 12rpx;
}

.primary-btn,
.secondary-btn {
  width: 100%;
}
</style>
