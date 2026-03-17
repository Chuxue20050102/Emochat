<template>
  <view class="step-content">
    <view class="step-title">此刻的你，更接近<br/>哪种状态？</view>
    <scroll-view class="emoji-scroll" scroll-x="true" :show-scrollbar="false">
      <view class="emoji-row">
        <view 
          class="emoji-item-row" 
          v-for="(item, index) in emotionList" 
          :key="index"
          :class="{ 'selected-row': selectedEmotion && selectedEmotion.name === item.name }"
          @click="$emit('select', item)"
        >
          <text class="emoji-icon-row">{{ item.emoji }}</text>
          <view v-if="selectedEmotion && selectedEmotion.name === item.name" class="glow-backdrop" :style="{ background: 'radial-gradient(circle, ' + item.glowColor + ' 0%, transparent 60%)' }"></view>
        </view>
      </view>
    </scroll-view>
    <view class="hint-pill-container">
      <view class="hint-pill">点击选择 / 滑动选择</view>
    </view>
  </view>
</template>

<script setup>
defineProps({
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
}
.step-title {
  font-size: 40rpx;
  line-height: 1.5;
  font-weight: 600;
  color: #1A1A1A;
  margin-bottom: 50rpx;
}
.emoji-scroll {
  width: 100%;
  margin: 40rpx 0 60rpx;
}
.emoji-row {
  display: inline-flex;
  align-items: center;
  gap: 40rpx;
  padding: 20rpx; 
}
.emoji-item-row {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  transform: scale(0.9);
  opacity: 0.5;
}
.emoji-item-row.selected-row {
  transform: scale(1.4);
  opacity: 1;
  padding: 0 20rpx; 
}
.emoji-icon-row {
  font-size: 80rpx;
  position: relative;
  z-index: 2;
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
}
.hint-pill {
  background: rgba(255, 255, 255, 0.7);
  box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.03);
  color: #666;
  font-size: 24rpx;
  padding: 16rpx 40rpx;
  border-radius: 40rpx;
}
</style>
