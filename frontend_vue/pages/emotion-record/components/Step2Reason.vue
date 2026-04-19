<template>
  <view class="step-content scroll-y">
    <view class="step-title">这份情绪，可能和这些<br/>有关：<text class="sub-title-mark">(多选)</text></view>
    <view class="tags-grid">
      <view 
        class="tag-item" 
        v-for="tag in reasonTags" 
        :key="tag"
        :class="{ 'selected': selectedReasons.includes(tag) }"
        :style="selectedReasons.includes(tag) ? getSelectedStyle() : {}"
        @click="$emit('toggle', tag)"
      >
        {{ tag }}
      </view>
    </view>
  </view>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  reasonTags: Array,
  selectedReasons: Array,
  selectedEmotion: Object
})
defineEmits(['toggle'])

const getSelectedStyle = () => {
  if (!props.selectedEmotion) return {}
  
  // 从情绪的 bgColor 中提取主要颜色作为选中状态的背景色
  const bgColor = props.selectedEmotion.bgColor
  // 从情绪的 glowColor 中提取颜色作为边框和阴影颜色
  const glowColor = props.selectedEmotion.glowColor
  
  // 根据不同情绪设置更合适的字体颜色，确保显眼但不过亮
  const emotionName = props.selectedEmotion.name
  let fontColor = '#333' // 默认颜色
  
  switch (emotionName) {
    case '崩溃':
      fontColor = '#E06C5B' // 深粉色
      break
    case '迷茫':
      fontColor = '#7B68EE' // 深紫色
      break
    case '低落':
      fontColor = '#64748B' // 深灰色
      break
    case '平静':
      fontColor = '#475569' // 深灰色
      break
    case '轻松':
      fontColor = '#10B981' // 深绿色
      break
    case '愉快':
      fontColor = '#F59E0B' // 深黄色
      break
    case '极好':
      fontColor = '#EF4444' // 深红色
      break
  }
  
  return {
    background: bgColor,
    borderColor: glowColor,
    color: fontColor,
    boxShadow: `0 6rpx 20rpx ${glowColor.replace('0.6', '0.15')}`
  }
}
</script>

<style lang="scss" scoped>
.step-content {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 0 50rpx;
}
.scroll-y {
  overflow-y: auto;
}
.step-title {
  font-size: 40rpx;
  line-height: 1.5;
  font-weight: 600;
  color: #1A1A1A;
  margin-bottom: 50rpx;
}
.sub-title-mark {
  font-size: 26rpx;
  color: #999;
  font-weight: normal;
  margin-left: 10rpx;
}
.tags-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 24rpx;
}
.tag-item {
  width: calc(50% - 12rpx);
  padding: 26rpx 0;
  text-align: center;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 99rpx;
  font-size: 30rpx;
  color: #333;
  transition: all 0.25s cubic-bezier(0.25, 1, 0.5, 1);
  border: 2rpx solid transparent;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.02);
}
.tag-item:active {
  transform: scale(0.96);
}
.tag-item.selected {
  background: #FFF2F0;
  color: #E06C5B;
  border-color: #FFB0A4;
  font-weight: 500;
  box-shadow: 0 6rpx 20rpx rgba(255, 155, 140, 0.15);
  transform: scale(1.02);
}
</style>
