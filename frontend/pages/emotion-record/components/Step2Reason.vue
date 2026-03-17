<template>
  <view class="step-content scroll-y">
    <view class="step-title">这份情绪，可能和这些<br/>有关：<text class="sub-title-mark">(多选)</text></view>
    <view class="tags-grid">
      <view 
        class="tag-item" 
        v-for="tag in reasonTags" 
        :key="tag"
        :class="{ 'selected': selectedReasons.includes(tag) }"
        @click="$emit('toggle', tag)"
      >
        {{ tag }}
      </view>
    </view>
  </view>
</template>

<script setup>
defineProps({
  reasonTags: Array,
  selectedReasons: Array
})
defineEmits(['toggle'])
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
