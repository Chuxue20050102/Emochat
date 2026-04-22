<template>
  <view class="step-content">
    <view class="intro-card">
      <view class="card-title">此刻的你，更接近哪一种心情？</view>
      <text class="card-desc">从负面到正面共 8 个等级，选一个最贴近你现在状态的心情。</text>
    </view>

    <view class="grid-card">
      <view class="emoji-grid">
        <view
          v-for="item in emotionList"
          :key="item.name"
          class="emoji-item"
          :class="{ selected: selectedEmotion && selectedEmotion.name === item.name }"
          @click="$emit('select', item)"
        >
          <text class="emoji-icon">{{ item.emoji }}</text>
          <view class="emoji-name">{{ item.name }}</view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
defineProps({
  emotionList: {
    type: Array,
    default: () => [],
  },
  selectedEmotion: {
    type: Object,
    default: null,
  },
})

defineEmits(['select'])
</script>

<style lang="scss" scoped>
.step-content {
  padding: 0 36rpx;
}

.intro-card,
.grid-card {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 24rpx;
  padding: 24rpx;
  border: 1rpx solid rgba(255, 255, 255, 0.85);
}

.grid-card {
  margin-top: 16rpx;
}

.card-title {
  font-size: 30rpx;
  font-weight: 700;
  color: #2d3451;
  margin-bottom: 10rpx;
}

.card-desc {
  font-size: 25rpx;
  color: #5f6b86;
  line-height: 1.5;
}

.emoji-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12rpx;
}

.emoji-item {
  min-height: 116rpx;
  border-radius: 18rpx;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 6rpx;
  background: rgba(245, 248, 255, 0.92);
  border: 1rpx solid rgba(223, 232, 247, 0.8);
}

.emoji-item.selected {
  background: linear-gradient(135deg, rgba(141, 187, 255, 0.25), rgba(142, 222, 195, 0.26));
  border-color: rgba(130, 170, 240, 0.55);
}

.emoji-icon {
  font-size: 46rpx;
}

.emoji-name {
  font-size: 24rpx;
  color: #2e3449;
}
</style>
