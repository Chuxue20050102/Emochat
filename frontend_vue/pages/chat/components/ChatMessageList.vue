<template>
  <scroll-view 
    class="chat-scroll" 
    scroll-y="true" 
    :scroll-into-view="scrollTopId"
    scroll-with-animation
  >
    <view class="message-list">
      <view 
        v-for="(msg, index) in chatList" 
        :key="index"
        :id="'msg-' + index"
        class="message-item"
        :class="msg.role === 'user' ? 'is-user' : 'is-ai'"
      >
        <view class="avatar" :class="msg.role === 'user' ? 'avatar-user' : 'avatar-ai'">
          <text class="avatar-icon">{{ msg.role === 'user' ? '😄' : '🌿' }}</text>
        </view>
        <view class="bubble">
          <text class="content">{{ msg.content }}</text>
        </view>
      </view>

      <view v-if="isThinking" class="message-item is-ai">
         <view class="avatar avatar-ai">
           <text class="avatar-icon">🌿</text>
         </view>
         <view class="bubble thinking">
           <view class="dot"></view>
           <view class="dot"></view>
           <view class="dot"></view>
         </view>
      </view>
      <view id="scroll-bottom" class="scroll-bottom"></view>
    </view>
  </scroll-view>
</template>

<script setup>
defineProps({
  chatList: {
    type: Array,
    required: true
  },
  isThinking: {
    type: Boolean,
    default: false
  },
  scrollTopId: {
    type: String,
    default: ''
  }
})
</script>

<style lang="scss" scoped>
.chat-scroll {
  flex: 1;
  position: relative;
  z-index: 1;
  width: 100%;
}

.message-list {
  padding: 20rpx 40rpx;
  display: flex;
  flex-direction: column;
  gap: 40rpx;
}

.scroll-bottom {
  height: 20rpx;
}

.message-item {
  display: flex;
  align-items: flex-start;
  gap: 24rpx;
  width: 100%;
  
  &.is-user {
    flex-direction: row-reverse;
  }
}

.avatar {
  width: 80rpx;
  height: 80rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.06);
  flex-shrink: 0;
}

.avatar-user {
  background-color: #FFF3E0;
}

.avatar-ai {
  background-color: #E6F7F0;
}

.avatar-icon {
  font-size: 40rpx;
}

.bubble {
  max-width: 68%;
  padding: 24rpx 32rpx;
  border-radius: $emo-radius-base;
  font-size: 30rpx;
  line-height: 1.5;
  color: $emo-text-main;
  box-shadow: $emo-shadow-bubble;
  position: relative;
  word-break: break-all;
}

.is-user .bubble {
  background-color: $emo-color-primary;
  border-top-right-radius: 4rpx;
}

.is-ai .bubble {
  background-color: $emo-bubble-ai;
  border-top-left-radius: 4rpx;
}

.thinking {
  display: flex;
  align-items: center;
  gap: 8rpx;
  height: 48rpx;
  padding: 16rpx 24rpx;
}
.dot {
  width: 12rpx;
  height: 12rpx;
  border-radius: 50%;
  background-color: #A3A3B2;
  animation: bounce 1.4s infinite ease-in-out both;
}
.dot:nth-child(1) { animation-delay: -0.32s; }
.dot:nth-child(2) { animation-delay: -0.16s; }
@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); opacity: 0.4; }
  40% { transform: scale(1); opacity: 1; }
}
</style>
