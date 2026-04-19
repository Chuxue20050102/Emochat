<template>
  <view class="step-content">
    <view class="cards-container">
      <view class="text-card">
        <view class="card-title">此刻的你，更接近哪种状态？</view>
        <view class="text-content">
          <text class="text-desc">每个人的情绪都是独一无二的，选择最符合你当下感受的状态，让我们一起探索你的内心世界。</text>
        </view>
      </view>
      <view class="emotion-card">
        <view class="emoji-grid">
          <view 
            class="emoji-item" 
            v-for="(item, index) in emotionList" 
            :key="index"
            :class="{ 'selected': selectedEmotion && selectedEmotion.name === item.name }"
            @click="$emit('select', item)"
          >
            <image v-if="item.name === '崩溃'" :src="emotionCrash" class="emoji-image"></image>
            <image v-else-if="item.name === '迷茫'" :src="emotionConfused" class="emoji-image"></image>
            <image v-else-if="item.name === '低落'" :src="emotionDown" class="emoji-image"></image>
            <image v-else-if="item.name === '平静'" :src="emotionCalm" class="emoji-image"></image>
            <image v-else-if="item.name === '轻松'" :src="emotionRelaxed" class="emoji-image"></image>
            <image v-else-if="item.name === '愉快'" :src="emotionHappy" class="emoji-image"></image>
            <image v-else-if="item.name === '极好'" :src="emotionExcellent" class="emoji-image"></image>
            <text v-else class="emoji-icon">{{ item.emoji }}</text>
            <view class="emoji-name">{{ item.name }}</view>
            <view v-if="selectedEmotion && selectedEmotion.name === item.name" class="glow-backdrop" :style="{ background: 'radial-gradient(circle, ' + item.glowColor + ' 0%, transparent 60%)' }"></view>
          </view>
        </view>
      </view>
    </view>
    <view class="hint-pill-container">
      <view class="hint-pill">点击选择</view>
    </view>
  </view>
</template>

<script setup>
import emotionCrash from '@/static/images/emotion-crash.png'
import emotionConfused from '@/static/images/emotion-confused.png'
import emotionDown from '@/static/images/emotion-down.png'
import emotionCalm from '@/static/images/emotion-calm.png'
import emotionRelaxed from '@/static/images/emotion-relaxed.png'
import emotionHappy from '@/static/images/emotion-happy.png'
import emotionExcellent from '@/static/images/emotion-excellent.png'

const props = defineProps({
  emotionList: Array,
  selectedEmotion: Object
})
defineEmits(['select'])
</script>

<style lang="scss" scoped>
.step-content {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 0 50rpx;
  font-family: 'SimSun', serif;
  color: #6B5B47;
  font-size: 28rpx;
}
.step-title {
  font-size: 44rpx;
  line-height: 1.5;
  font-weight: 600;
  color: #6B5B47;
  margin-bottom: 50rpx;
  font-family: 'SimSun', serif;
}
.cards-container {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
  margin: 40rpx 0 60rpx;
  padding: 0 20rpx;
}
.text-card {
  flex: 1;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 30rpx;
  padding: 40rpx 30rpx;
  box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.05);
  border: 2rpx solid rgba(255, 255, 255, 0.8);
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.emotion-card {
  flex: 1;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 30rpx;
  padding: 30rpx;
  box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.05);
  border: 2rpx solid rgba(255, 255, 255, 0.8);
}
.card-title {
  font-size: 32rpx;
  font-weight: 700;
  color: #6B5B47;
  margin-bottom: 30rpx;
  text-align: left;
  line-height: 1.5;
  white-space: nowrap;
}
.text-content {
  display: flex;
  flex-direction: column;
  gap: 15rpx;
}
.text-desc {
  font-size: 28rpx;
  font-weight: 600;
  color: #6B5B47;
  line-height: 1.5;
  text-align: left;
  white-space: nowrap;
}
.emoji-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15rpx;
}
.emoji-item {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20rpx;
  border-radius: 20rpx;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  transform: scale(0.9);
  opacity: 0.7;
}
.emoji-item:hover {
  transform: scale(0.95);
  opacity: 0.9;
  background: rgba(255, 255, 255, 0.5);
}
.emoji-item.selected {
  transform: scale(1.1);
  opacity: 1;
  background: rgba(255, 255, 255, 0.8);
}
.emoji-icon {
  font-size: 60rpx;
  position: relative;
  z-index: 2;
  margin-bottom: 10rpx;
}
.emoji-image {
  width: 60rpx;
  height: 60rpx;
  object-fit: contain;
  position: relative;
  z-index: 2;
  margin-bottom: 10rpx;
}
.emoji-name {
  font-size: 24rpx;
  color: #6B5B47;
  position: relative;
  z-index: 2;
  text-align: center;
}
.glow-backdrop {
  position: absolute;
  top: -40rpx; right: -40rpx; bottom: -40rpx; left: -40rpx;
  z-index: 1;
  border-radius: 50%;
  animation: pulseGlow 2s infinite alternate;
}
@keyframes pulseGlow {
  0% { transform: scale(0.9); opacity: 0.8; }
  100% { transform: scale(1.1); opacity: 1; }
}
.hint-pill-container {
  display: flex;
  justify-content: center;
  margin-top: 40rpx;
}
.hint-pill {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(245, 245, 220, 0.9));
  box-shadow: 0 6rpx 20rpx rgba(107, 91, 71, 0.15);
  color: #6B5B47;
  font-size: 26rpx;
  padding: 18rpx 48rpx;
  border-radius: 48rpx;
  border: 2rpx solid rgba(107, 91, 71, 0.3);
  transition: all 0.3s ease;
  font-weight: 600;
}
.hint-pill:hover {
  background: linear-gradient(135deg, #6B5B47, #5A4A37);
  color: #FFF;
  box-shadow: 0 8rpx 24rpx rgba(107, 91, 71, 0.3);
  transform: translateY(-3rpx) scale(1.02);
}
</style>
