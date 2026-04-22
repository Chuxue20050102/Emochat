<template>
  <view class="header">
    <view class="topbar">
      <view class="back-btn" @click="emit('back')">返回</view>
      <view class="status-chip" :class="{ active: useMemory }">
        {{ useMemory ? '记忆开启' : '无记忆模式' }}
      </view>
    </view>

    <view class="hero-card">
      <view class="title-wrap">
        <text class="eyebrow">EmoChat Companion</text>
        <text class="title">情绪陪聊</text>
        <text class="subtitle">不用组织语言，想到什么就说什么。我会接住你的节奏。</text>
      </view>

      <view class="actions">
        <view class="action-pill" :class="{ active: useMemory }" @click="emit('toggle-memory', !useMemory)">
          {{ useMemory ? '切到无记忆' : '开启记忆' }}
        </view>
        <view class="action-pill" :class="{ disabled: isThinking || messageCount === 0 }" @click="emit('archive')">
          归档
        </view>
        <view class="action-pill" :class="{ disabled: isThinking }" @click="emit('history')">
          历史情绪
        </view>
        <view
          class="action-pill danger"
          :class="{ disabled: isThinking || messageCount === 0 }"
          @click="emit('clear')"
        >
          清空
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
defineProps({
  useMemory: {
    type: Boolean,
    default: true,
  },
  messageCount: {
    type: Number,
    default: 0,
  },
  isThinking: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['archive', 'back', 'clear', 'history', 'toggle-memory'])
</script>

<style lang="scss" scoped>
.header {
  position: relative;
  z-index: 2;
  padding: 54rpx 22rpx 10rpx;
}

.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10rpx;
}

.back-btn {
  min-width: 92rpx;
  height: 52rpx;
  padding: 0 18rpx;
  border-radius: 999rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #2d3a55;
  font-size: 22rpx;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.72);
  border: 1rpx solid rgba(255, 255, 255, 0.88);
  box-shadow: 0 8rpx 24rpx rgba(46, 55, 89, 0.08);
  backdrop-filter: blur(16rpx);
}

.status-chip {
  height: 50rpx;
  padding: 0 16rpx;
  border-radius: 999rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20rpx;
  color: #5f6d86;
  background: rgba(255, 255, 255, 0.55);
  border: 1rpx solid rgba(255, 255, 255, 0.75);
}

.status-chip.active {
  color: #21476d;
  background: rgba(213, 237, 255, 0.82);
  border-color: rgba(170, 210, 242, 0.95);
}

.hero-card {
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.84), rgba(245, 250, 255, 0.64));
  border: 1rpx solid rgba(255, 255, 255, 0.9);
  border-radius: 24rpx;
  backdrop-filter: blur(22rpx);
  padding: 18rpx 18rpx 16rpx;
  box-shadow: 0 14rpx 44rpx rgba(36, 47, 79, 0.08);
}

.title-wrap {
  display: flex;
  flex-direction: column;
  gap: 4rpx;
}

.eyebrow {
  font-size: 18rpx;
  letter-spacing: 1rpx;
  text-transform: uppercase;
  color: #7182a4;
}

.title {
  font-size: 34rpx;
  line-height: 1.15;
  font-weight: 700;
  color: #24304b;
}

.subtitle {
  font-size: 22rpx;
  line-height: 1.4;
  color: #5f6a7e;
}

.actions {
  margin-top: 12rpx;
  display: flex;
  gap: 8rpx;
  flex-wrap: wrap;
}

.action-pill {
  padding: 10rpx 18rpx;
  border-radius: 999rpx;
  font-size: 20rpx;
  color: #40506b;
  background: rgba(240, 246, 255, 0.9);
  border: 1rpx solid transparent;
}

.action-pill.active {
  color: #20476d;
  background: rgba(217, 236, 255, 0.92);
  border-color: rgba(169, 208, 240, 0.95);
}

.action-pill.danger {
  color: #874e43;
  background: rgba(255, 239, 233, 0.92);
}

.action-pill.disabled {
  opacity: 0.4;
}
</style>
