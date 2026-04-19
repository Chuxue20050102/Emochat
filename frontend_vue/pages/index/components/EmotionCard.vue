<template>
  <view class="module-card emotion-card">
    <view v-if="!selectedEmotion" class="unselected-state">
      <view class="emotion-title">现在的你，更接近哪种感觉？</view>
      <view class="emoji-list">
        <view class="emoji-item" v-for="(item, index) in emotionList" :key="index" @click="handleSelect(item)">
          <image v-if="item.name === '崩溃'" :src="emotionCrash" class="emoji-image"></image>
          <image v-else-if="item.name === '迷茫'" :src="emotionConfused" class="emoji-image"></image>
          <image v-else-if="item.name === '低落'" :src="emotionDown" class="emoji-image"></image>
          <image v-else-if="item.name === '平静'" :src="emotionCalm" class="emoji-image"></image>
          <image v-else-if="item.name === '轻松'" :src="emotionRelaxed" class="emoji-image"></image>
          <image v-else-if="item.name === '愉快'" :src="emotionHappy" class="emoji-image"></image>
          <image v-else-if="item.name === '极好'" :src="emotionExcellent" class="emoji-image"></image>
          <text v-else class="emoji-icon">{{ item.emoji }}</text>
        </view>
      </view>
    </view>
    
    <view v-else class="selected-state fade-in">
      <view class="selected-header">
        <image v-if="selectedEmotion.name === '崩溃'" :src="emotionCrash" class="large-emoji-image"></image>
        <image v-else-if="selectedEmotion.name === '迷茫'" :src="emotionConfused" class="large-emoji-image"></image>
        <image v-else-if="selectedEmotion.name === '低落'" :src="emotionDown" class="large-emoji-image"></image>
        <image v-else-if="selectedEmotion.name === '平静'" :src="emotionCalm" class="large-emoji-image"></image>
        <image v-else-if="selectedEmotion.name === '轻松'" :src="emotionRelaxed" class="large-emoji-image"></image>
        <image v-else-if="selectedEmotion.name === '愉快'" :src="emotionHappy" class="large-emoji-image"></image>
        <image v-else-if="selectedEmotion.name === '极好'" :src="emotionExcellent" class="large-emoji-image"></image>
        <text v-else class="large-emoji">{{ selectedEmotion.emoji }}</text>
        <text class="emotion-name">{{ selectedEmotion.name }}</text>
      </view>
      <view class="emotion-reply">{{ selectedEmotion.reply }}</view>
      
      <view class="action-buttons">
        <button class="primary-btn" @click="goToRecord">记录这一刻 →</button>
        <text class="cancel-text" @click="cancelSelection">先不记录</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'
import emotionCrash from '@/static/images/emotion-crash.png'
import emotionConfused from '@/static/images/emotion-confused.png'
import emotionDown from '@/static/images/emotion-down.png'
import emotionCalm from '@/static/images/emotion-calm.png'
import emotionRelaxed from '@/static/images/emotion-relaxed.png'
import emotionHappy from '@/static/images/emotion-happy.png'
import emotionExcellent from '@/static/images/emotion-excellent.png'

const emotionList = [
  { emoji: '😣', name: '崩溃', reply: '看到你这么难受，抱抱你，辛苦了' },
  { emoji: '😕', name: '迷茫', reply: '心里有些乱乱的没关系，允许自己停下来' },
  { emoji: '🙁', name: '低落', reply: '允许自己有一点不开心，这很正常' },
  { emoji: '😐', name: '平静', reply: '平平静静的，也是一种很好的状态哦' },
  { emoji: '🙂', name: '轻松', reply: '感觉还不错对吧，继续保持这个节奏' },
  { emoji: '😊', name: '愉快', reply: '看到你有一点开心，真好' },
  { emoji: '😄', name: '极好', reply: '心情大好！这一刻绝对值得被记录下来' }
]

const selectedEmotion = ref(null)

const handleSelect = (item) => {
  selectedEmotion.value = item
}

const cancelSelection = () => {
  selectedEmotion.value = null
}

const goToRecord = () => {
  // 将首页选中的情绪存入缓存，供情绪记录页读取
  if (selectedEmotion.value) {
    uni.setStorageSync('preSelectedEmotion', selectedEmotion.value.name)
  }
  uni.switchTab({ url: '/pages/emotion-record/index' })
}
</script>

<style lang="scss" scoped>

.emotion-card {
  min-height: 320rpx;
  height: 320rpx;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  padding-top: 20rpx;
}
.unselected-state {
  display: flex;
  flex-direction: column;
  gap: 35rpx;
}
.emotion-title {
  font-size: 34rpx;
  font-weight: 600;
  color: #1A1A1A;
  margin-bottom: 50rpx;
  text-align: left;
}
.emoji-list {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.emoji-item {
  transition: transform 0.2s;
  padding: 10rpx;
}
.emoji-item:active {
  transform: scale(1.3);
}
.emoji-icon {
  font-size: 56rpx;
}
.emoji-image {
  width: 56rpx;
  height: 56rpx;
  object-fit: contain;
}
.large-emoji-image {
  width: 80rpx;
  height: 80rpx;
  object-fit: contain;
  margin-right: 16rpx;
}

.selected-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}
.fade-in {
  animation: fadeIn 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(16rpx); }
  to { opacity: 1; transform: translateY(0); }
}

.selected-header {
  display: flex;
  align-items: center;
  gap: 16rpx;
  margin-bottom: 20rpx;
}
.large-emoji {
  font-size: 64rpx;
}
.emotion-name {
  font-size: 40rpx;
  font-weight: 600;
  color: #1A1A1A;
}
.emotion-reply {
  font-size: 28rpx;
  color: #666;
  margin-bottom: 50rpx;
}
.action-buttons {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16rpx;
  width: 100%;
}
.primary-btn {
  width: 80%;
  height: 96rpx;
  border-radius: 48rpx;
  background: linear-gradient(135deg, #FF9B8C, #FFB0A4);
  color: #FFF;
  font-size: 32rpx;
  font-weight: 600;
  letter-spacing: 2rpx;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 12rpx 30rpx rgba(255, 155, 140, 0.35);
  border: none;
  transition: transform 0.2s ease;
}
.primary-btn::after {
  border: none;
}
.primary-btn:active {
  transform: scale(0.97);
}
.cancel-text {
  font-size: 26rpx;
  color: #888;
  padding: 16rpx 30rpx;
}
</style>
