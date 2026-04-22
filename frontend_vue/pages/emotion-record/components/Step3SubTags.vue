<template>
  <view class="step-content">
    <view class="step-title">
      再细一点描述这种感受
      <text class="sub-title-mark">（可选）</text>
    </view>

    <view v-if="selectedEmotion" class="context-chip">当前心情：{{ selectedEmotion.emoji }} {{ selectedEmotion.name }}</view>

    <view class="tags-grid">
      <view
        v-for="tag in currentSubTags"
        :key="tag"
        class="tag-item"
        :class="{ selected: selectedSubTags.includes(tag) }"
        @click="$emit('toggle', tag)"
      >
        {{ tag }}
      </view>
    </view>
  </view>
</template>

<script setup>
defineProps({
  currentSubTags: {
    type: Array,
    default: () => [],
  },
  selectedSubTags: {
    type: Array,
    default: () => [],
  },
  selectedEmotion: {
    type: Object,
    default: null,
  },
})

defineEmits(['toggle'])
</script>

<style lang="scss" scoped>
.step-content {
  padding: 0 36rpx;
}

.step-title {
  font-size: 34rpx;
  font-weight: 700;
  color: #25314a;
  margin-bottom: 20rpx;
}

.sub-title-mark {
  font-size: 24rpx;
  font-weight: 400;
  color: #8090ad;
  margin-left: 8rpx;
}

.context-chip {
  display: inline-flex;
  align-items: center;
  padding: 10rpx 18rpx;
  border-radius: 999rpx;
  background: rgba(255, 255, 255, 0.82);
  color: #495a7b;
  font-size: 24rpx;
  margin-bottom: 20rpx;
}

.tags-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 14rpx;
}

.tag-item {
  height: 88rpx;
  border-radius: 999rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.86);
  color: #3a4765;
  font-size: 26rpx;
}

.tag-item.selected {
  background: linear-gradient(135deg, rgba(141, 187, 255, 0.27), rgba(142, 222, 195, 0.28));
  color: #22314e;
  font-weight: 600;
}
</style>
