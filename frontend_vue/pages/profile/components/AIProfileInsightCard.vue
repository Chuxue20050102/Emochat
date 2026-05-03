<template>
  <view class="ai-insight-card">
    <view class="card-glow"></view>

    <view class="card-head">
      <view>
        <text class="eyebrow">AI 近况总结</text>
        <text class="title">最近的你</text>
      </view>
      <text class="status-pill">{{ statusLabel }}</text>
    </view>

    <text class="summary-text">{{ summaryText }}</text>
    <text v-if="suggestion" class="suggestion-text">{{ suggestion }}</text>

    <view v-if="overviewItems.length" class="overview-grid">
      <view v-for="item in overviewItems" :key="item.label" class="overview-item">
        <text class="item-label">{{ item.label }}</text>
        <text class="item-value">{{ item.value }}</text>
      </view>
    </view>

    <view class="action-row">
      <view class="chat-action" @click="emit('chat')">和我一起看看</view>
    </view>
  </view>
</template>

<script setup>
const emit = defineEmits(['chat'])

defineProps({
  summaryText: {
    type: String,
    default: '记录几次后，我会在这里帮你整理最近的情绪线索。',
  },
  suggestion: {
    type: String,
    default: '',
  },
  overviewItems: {
    type: Array,
    default: () => [],
  },
  statusLabel: {
    type: String,
    default: '本月',
  },
})
</script>

<style lang="scss" scoped>
.ai-insight-card {
  position: relative;
  overflow: hidden;
  margin-bottom: 18rpx;
  padding: 26rpx;
  border-radius: 30rpx;
  background:
    linear-gradient(150deg, rgba(255, 255, 255, 0.9), rgba(255, 248, 239, 0.82)),
    radial-gradient(circle at 96% 0%, rgba(143, 184, 160, 0.28), transparent 44%);
  border: 2rpx solid rgba(255, 255, 255, 0.9);
  box-shadow: 0 24rpx 58rpx rgba(74, 54, 40, 0.11);
}

.card-glow {
  position: absolute;
  right: -92rpx;
  top: -118rpx;
  width: 260rpx;
  height: 260rpx;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(217, 162, 127, 0.26), rgba(217, 162, 127, 0));
}

.card-head,
.summary-text,
.suggestion-text,
.overview-grid,
.action-row {
  position: relative;
  z-index: 1;
}

.card-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16rpx;
}

.eyebrow,
.status-pill {
  display: inline-flex;
  align-items: center;
  width: fit-content;
  padding: 5rpx 13rpx;
  border-radius: 999rpx;
  font-size: 19rpx;
  line-height: 1.25;
}

.eyebrow {
  color: $emo-sage-text;
  background: rgba(237, 250, 243, 0.88);
}

.status-pill {
  flex-shrink: 0;
  color: #8a684e;
  background: rgba(255, 241, 222, 0.86);
}

.title {
  display: block;
  margin-top: 10rpx;
  font-size: 32rpx;
  line-height: 1.35;
  font-weight: 800;
  color: $emo-text-main;
}

.summary-text {
  display: block;
  margin-top: 18rpx;
  font-size: 28rpx;
  line-height: 1.62;
  color: $emo-text-main;
}

.suggestion-text {
  display: block;
  margin-top: 12rpx;
  padding-left: 18rpx;
  border-left: 6rpx solid rgba(217, 162, 127, 0.5);
  font-size: 23rpx;
  line-height: 1.55;
  color: $emo-text-sub;
}

.overview-grid {
  margin-top: 20rpx;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12rpx;
}

.overview-item {
  min-height: 96rpx;
  padding: 14rpx 10rpx;
  border-radius: 22rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6rpx;
  background: rgba(250, 246, 239, 0.68);
  border: 1rpx solid rgba(255, 255, 255, 0.86);
}

.item-label {
  font-size: 20rpx;
  color: $emo-text-sub;
}

.item-value {
  max-width: 100%;
  font-size: 24rpx;
  font-weight: 800;
  color: $emo-text-main;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.action-row {
  margin-top: 20rpx;
  display: flex;
  justify-content: flex-end;
}

.chat-action {
  padding: 10rpx 18rpx;
  border-radius: 999rpx;
  font-size: 22rpx;
  line-height: 1.35;
  font-weight: 800;
  color: #ffffff;
  background: linear-gradient(135deg, #5c836f, #3f6d59);
  box-shadow: 0 12rpx 26rpx rgba(63, 109, 89, 0.18);
}
</style>
