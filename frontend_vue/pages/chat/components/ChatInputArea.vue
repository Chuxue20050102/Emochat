<template>
  <view class="input-area">
    <view class="input-wrapper">
      <input 
        class="chat-input" 
        v-model="localText" 
        placeholder="有什么烦心事？随时告诉我..." 
        @confirm="handleSend"
        confirm-type="send"
      />
      <view 
        class="send-btn" 
        :class="{'is-active': localText.trim().length > 0}"
        @click="handleSend"
      >
        发送
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['send'])
const localText = ref('')

const handleSend = () => {
  const text = localText.value.trim()
  if (text) {
    emit('send', text)
    localText.value = ''
  }
}
</script>

<style lang="scss" scoped>
.input-area {
  position: relative;
  z-index: 2;
  padding: 20rpx 40rpx;
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(20px);
  border-top: 1rpx solid rgba(255, 255, 255, 0.4);
}

.input-wrapper {
  display: flex;
  align-items: center;
  gap: 20rpx;
  background-color: #FFFFFF;
  border-radius: $emo-radius-pill;
  padding: 12rpx 12rpx 12rpx 32rpx;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
}

.chat-input {
  flex: 1;
  height: 72rpx;
  font-size: 30rpx;
  color: $emo-text-main;
}

.send-btn {
  padding: 0 36rpx;
  height: 72rpx;
  line-height: 72rpx;
  border-radius: $emo-radius-pill;
  font-size: 28rpx;
  font-weight: 500;
  color: $emo-text-sub;
  background-color: $emo-bg-base;
  transition: all 0.3s ease;
  
  &.is-active {
    color: #fff;
    background-color: $emo-color-secondary;
    box-shadow: 0 4px 12px rgba(255, 179, 167, 0.4);
  }
}
</style>
