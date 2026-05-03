<template>
  <view class="header">
    <view class="topbar">
      <view class="nav-pill" @click="emit('back')">回首页</view>
      <view class="top-title">
        <text class="brand">我在听</text>
        <text class="state">{{ isThinking ? '正在陪你慢慢整理' : '不用整理好，先说出来也可以' }}</text>
      </view>
      <view class="nav-pill primary" @click="emit('history')">最近的你</view>
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
  isArchiving: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['archive', 'back', 'history'])
</script>

<style lang="scss" scoped>
.header {
  position: relative;
  z-index: 2;
  padding: calc(var(--status-bar-height) + 24rpx) 24rpx 10rpx;
}

.topbar {
  min-height: 72rpx;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nav-pill {
  min-width: 82rpx;
  height: 58rpx;
  padding: 0 18rpx;
  border-radius: 999rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #5c514b;
  font-size: 22rpx;
  font-weight: 700;
  background: rgba(255, 255, 255, 0.7);
  border: 1rpx solid rgba(255, 255, 255, 0.9);
  box-shadow: 0 12rpx 30rpx rgba(64, 48, 36, 0.08);
}

.nav-pill.primary {
  color: #476256;
  background: rgba(237, 251, 244, 0.86);
  border-color: rgba(193, 235, 212, 0.95);
}

.top-title {
  flex: 1;
  min-width: 0;
  padding: 0 18rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rpx;
}

.brand {
  font-size: 32rpx;
  line-height: 1.16;
  font-weight: 800;
  letter-spacing: 0.3rpx;
  color: #2d2926;
}

.state {
  max-width: 420rpx;
  font-size: 20rpx;
  color: #8b7c72;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
