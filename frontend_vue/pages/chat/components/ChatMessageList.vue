<template>
  <scroll-view
    class="chat-scroll"
    scroll-y="true"
    :scroll-into-view="scrollTopId"
    :style="scrollStyle"
  >
    <view class="message-list">
      <view
        v-for="(msg, index) in chatList"
        :key="msg.localId || index"
        :id="'msg-' + index"
        class="message-item"
        :class="[`is-${msg.role}`, { 'is-agent': msg.agent }]"
      >
        <view class="bubble-wrap">
          <view v-if="msg.agent" class="agent-label">我参考了你留下的线索</view>

          <view class="bubble" :class="{ failed: msg.status === 'failed' }">
            <text v-if="msg.content" class="content">{{ msg.content }}</text>
            <view v-else-if="msg.status === 'streaming'" class="streaming-placeholder">
              <text class="thinking-text">{{ msg.agent ? '正在理解你的需要' : '正在认真回应' }}</text>
              <view class="dot"></view>
              <view class="dot"></view>
              <view class="dot"></view>
            </view>
            <view v-if="msg.status === 'failed'" class="failed-row">
              <text class="failed-tip">刚刚没送出去</text>
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

defineEmits(['archive', 'retry'])
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
  padding: 14rpx 26rpx 0;
  display: flex;
  flex-direction: column;
  gap: 20rpx;
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
}

.message-item.is-assistant {
  align-items: flex-start;
}

.message-item.is-system {
  justify-content: center;
}

.bubble-wrap {
  max-width: 82%;
  display: flex;
  flex-direction: column;
  gap: 7rpx;
}

.message-item.is-user .bubble-wrap {
  align-items: flex-end;
}

.message-item.is-assistant .bubble-wrap {
  max-width: 86%;
}

.bubble {
  padding: 18rpx 22rpx;
  border-radius: 24rpx;
  font-size: 28rpx;
  line-height: 1.55;
  color: #332c27;
  background: rgba(255, 255, 255, 0.78);
  border: 1rpx solid rgba(255, 255, 255, 0.88);
  box-shadow: 0 16rpx 36rpx rgba(71, 52, 38, 0.08);
  word-break: break-word;
}

.message-item.is-user .bubble {
  color: #2f4036;
  background: linear-gradient(135deg, rgba(221, 242, 229, 0.96) 0%, rgba(199, 226, 210, 0.96) 100%);
  border-color: rgba(157, 198, 177, 0.68);
  border-bottom-right-radius: 8rpx;
  box-shadow: 0 16rpx 34rpx rgba(67, 95, 79, 0.13);
}

.message-item.is-assistant .bubble {
  border-top-left-radius: 8rpx;
}

.message-item.is-agent .bubble {
  background: rgba(255, 255, 255, 0.82);
  border-color: rgba(183, 226, 203, 0.72);
}

.message-item.is-system .bubble {
  max-width: 88%;
  padding: 14rpx 18rpx;
  color: #7d6c62;
  background: rgba(255, 255, 255, 0.58);
  border: 1rpx dashed rgba(204, 190, 178, 0.78);
  box-shadow: none;
  font-size: 24rpx;
}

.agent-label {
  display: inline-flex;
  align-self: flex-start;
  padding: 5rpx 12rpx;
  border-radius: 999rpx;
  font-size: 19rpx;
  color: #3f735d;
  background: rgba(237, 250, 243, 0.82);
  border: 1rpx solid rgba(183, 226, 203, 0.82);
}

.bubble.failed {
  border-color: #fecdd3;
  background: #fff1f2;
}

.failed-row {
  margin-top: 12rpx;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.failed-tip {
  font-size: 22rpx;
  color: #be123c;
}

.retry-btn {
  font-size: 24rpx;
  color: #2563eb;
}

.time {
  font-size: 19rpx;
  color: #a4958b;
  line-height: 1;
}

.thinking-text {
  font-size: 25rpx;
  color: #8a766a;
}

.streaming-placeholder {
  display: flex;
  align-items: center;
  gap: 8rpx;
  min-height: 34rpx;
}

.dot {
  width: 8rpx;
  height: 8rpx;
  border-radius: 50%;
  background-color: #9f8a7e;
  animation: bounce 1.4s infinite ease-in-out both;
}

.dot:nth-child(2) {
  animation-delay: 0.16s;
}

.dot:nth-child(3) {
  animation-delay: 0.32s;
}

@keyframes bounce {
  0%,
  80%,
  100% {
    opacity: 0.36;
    transform: translateY(0);
  }

  40% {
    opacity: 1;
    transform: translateY(-5rpx);
  }
}
</style>
