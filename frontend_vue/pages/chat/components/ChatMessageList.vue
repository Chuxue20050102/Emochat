<template>
  <scroll-view
    class="chat-scroll"
    scroll-y="true"
    :scroll-into-view="scrollTopId"
    scroll-with-animation
    :style="scrollStyle"
  >
    <view class="message-list">
      <view
        v-for="(msg, index) in chatList"
        :key="msg.localId || index"
        :id="'msg-' + index"
        class="message-item"
        :class="`is-${msg.role}`"
      >
        <view v-if="msg.role !== 'system'" class="avatar" :class="msg.role === 'user' ? 'avatar-user' : 'avatar-ai'">
          <text class="avatar-icon">{{ msg.role === 'user' ? '我' : 'AI' }}</text>
        </view>

        <view class="bubble-wrap">
          <view class="bubble" :class="{ failed: msg.status === 'failed' }">
            <text v-if="msg.content" class="content">{{ msg.content }}</text>
            <view v-else-if="msg.status === 'streaming'" class="streaming-placeholder">
              <text class="thinking-text">AI 正在思考</text>
              <view class="dot"></view>
              <view class="dot"></view>
              <view class="dot"></view>
            </view>
            <view v-if="msg.status === 'failed'" class="failed-row">
              <text class="failed-tip">发送失败</text>
              <text class="retry-btn" @click="$emit('retry', msg.retryPayload)">重试</text>
            </view>
          </view>
          <text v-if="msg.time" class="time">{{ msg.time }}</text>
        </view>
      </view>

      <view id="scroll-bottom" class="scroll-bottom"></view>
    </view>
  </scroll-view>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  bottomPadding: {
    type: [Number, String],
    default: 0,
  },
  chatList: {
    type: Array,
    required: true,
  },
  isThinking: {
    type: Boolean,
    default: false,
  },
  scrollTopId: {
    type: String,
    default: '',
  },
})

const scrollStyle = computed(() => ({
  paddingBottom: typeof props.bottomPadding === 'number' ? `${props.bottomPadding}px` : props.bottomPadding,
}))

defineEmits(['retry'])
</script>

<style lang="scss" scoped>
.chat-scroll {
  flex: 1;
  min-height: 0;
  position: relative;
  z-index: 1;
  width: 100%;
}

.message-list {
  padding: 4rpx 24rpx 0;
  display: flex;
  flex-direction: column;
  gap: 18rpx;
}

.scroll-bottom {
  height: 20rpx;
}

.message-item {
  display: flex;
  width: 100%;
}

.message-item.is-user {
  justify-content: flex-end;
  align-items: flex-end;
  gap: 14rpx;
}

.message-item.is-assistant {
  flex-direction: column;
  align-items: flex-start;
  gap: 6rpx;
}

.message-item.is-system {
  justify-content: center;
}

.avatar {
  width: 64rpx;
  height: 64rpx;
  border-radius: 22rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-weight: 700;
  box-shadow: 0 10rpx 18rpx rgba(58, 69, 98, 0.08);
}

.avatar-user {
  background: linear-gradient(135deg, #ffd7c8 0%, #ffc3cd 100%);
  color: #854b3d;
}

.avatar-ai {
  background: linear-gradient(135deg, #d6eef2 0%, #dff6e6 100%);
  color: #245d4c;
}

.avatar-icon {
  font-size: 22rpx;
}

.bubble-wrap {
  max-width: 78%;
  display: flex;
  flex-direction: column;
  gap: 6rpx;
}

.message-item.is-user .bubble-wrap {
  align-items: flex-end;
}

.message-item.is-assistant .bubble-wrap {
  max-width: 88%;
  margin-left: 0;
}

.bubble {
  padding: 18rpx 20rpx;
  border-radius: 24rpx;
  font-size: 28rpx;
  line-height: 1.5;
  color: #273043;
  background: rgba(255, 255, 255, 0.9);
  border: 1rpx solid rgba(255, 255, 255, 0.92);
  box-shadow: 0 12rpx 28rpx rgba(53, 57, 81, 0.08);
  word-break: break-word;
}

.message-item.is-user .bubble {
  background: linear-gradient(135deg, #ffd9cb 0%, #ffc8cf 100%);
  border-bottom-right-radius: 10rpx;
}

.message-item.is-assistant .bubble {
  border-top-left-radius: 10rpx;
}

.message-item.is-system .bubble {
  background: rgba(255, 255, 255, 0.72);
  border: 1rpx dashed #d3d9e6;
  color: #596276;
  box-shadow: none;
}

.bubble.failed {
  border: 1rpx solid #ffc1c1;
  background: #fff6f6;
}

.failed-row {
  margin-top: 12rpx;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.failed-tip {
  font-size: 22rpx;
  color: #b25d5d;
}

.retry-btn {
  font-size: 24rpx;
  color: #2f67d8;
}

.time {
  font-size: 20rpx;
  color: #8c93a2;
  line-height: 1;
}

.thinking-text {
  font-size: 26rpx;
  color: #5f6a7e;
}

.streaming-placeholder {
  display: flex;
  align-items: center;
  gap: 8rpx;
  min-height: 32rpx;
}

.dot {
  width: 10rpx;
  height: 10rpx;
  border-radius: 50%;
  background-color: #97a2b6;
  animation: bounce 1.4s infinite ease-in-out both;
}

.dot:nth-child(1) {
  animation-delay: -0.32s;
}

.dot:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes bounce {
  0%,
  80%,
  100% {
    transform: scale(0);
    opacity: 0.4;
  }

  40% {
    transform: scale(1);
    opacity: 1;
  }
}
</style>
