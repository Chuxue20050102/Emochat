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
  color: $emo-text-main;
  margin-bottom: 10rpx;
}

.card-desc {
  font-size: 25rpx;
  color: $emo-text-sub;
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
  background: rgba(255, 252, 247, 0.78);
  border: 1rpx solid rgba(232, 219, 207, 0.82);
}

.emoji-item.selected {
  background: linear-gradient(135deg, rgba(255, 220, 181, 0.48), rgba(188, 226, 205, 0.5));
  border-color: rgba(92, 131, 111, 0.38);
}

.emoji-icon {
  font-size: 46rpx;
}

.emoji-name {
  font-size: 24rpx;
  color: $emo-text-main;
}
</style>
