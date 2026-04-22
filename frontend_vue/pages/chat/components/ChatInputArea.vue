<template>
  <view class="input-area" :style="areaStyle">
    <view class="input-wrapper">
      <input
        class="chat-input"
        v-model="localText"
        :placeholder="isStreaming ? 'AI 正在回复...' : placeholder"
        :disabled="disabled"
        :adjust-position="false"
        :cursor-spacing="cursorSpacing"
        confirm-type="send"
        maxlength="300"
        @confirm="handleSend"
        @focus="handleFocus"
        @blur="handleBlur"
      />
      <view class="counter">{{ localText.length }}/300</view>
      <view class="send-btn" :class="buttonClass" @click="handleButtonClick">
        {{ buttonText }}
      </view>
    </view>
  </view>
</template>

<script setup>
import { computed, ref, watch } from 'vue'

const props = defineProps({
  bottomOffset: {
    type: Number,
    default: 0,
  },
  cursorSpacing: {
    type: Number,
    default: 20,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  isStreaming: {
    type: Boolean,
    default: false,
  },
  placeholder: {
    type: String,
    default: '有什么想说的，慢慢讲给我听',
  },
})

const emit = defineEmits(['blur', 'focus', 'send', 'stop'])
const localText = ref('')

const canSend = computed(() => !props.disabled && localText.value.trim().length > 0)
const buttonText = computed(() => (props.isStreaming ? '停止' : '发送'))
const buttonClass = computed(() => ({
  'is-active': canSend.value,
  'is-stop': props.isStreaming,
}))
const areaStyle = computed(() => ({
  transform: props.bottomOffset > 0 ? `translateY(-${props.bottomOffset}px)` : 'translateY(0)',
}))

const handleSend = () => {
  if (!canSend.value) {
    return
  }
  const text = localText.value.trim()
  emit('send', text)
  localText.value = ''
}

const handleButtonClick = () => {
  if (props.isStreaming) {
    emit('stop')
    return
  }
  handleSend()
}

const handleFocus = () => {
  emit('focus')
}

const handleBlur = () => {
  emit('blur')
}

watch(
  () => props.disabled,
  (disabled) => {
    if (disabled) {
      localText.value = localText.value.trimStart()
    }
  },
)
</script>

<style lang="scss" scoped>
.input-area {
  position: relative;
  z-index: 2;
  padding: 10rpx 20rpx 14rpx;
  background: rgba(255, 255, 255, 0.68);
  backdrop-filter: blur(20px);
  border-top: 1rpx solid rgba(255, 255, 255, 0.5);
  transition: transform 0.22s ease;
}

.input-wrapper {
  display: flex;
  align-items: center;
  gap: 12rpx;
  background-color: #fff;
  border-radius: 999rpx;
  padding: 8rpx 10rpx 8rpx 22rpx;
  box-shadow: 0 4rpx 20rpx rgba(41, 41, 72, 0.08);
}

.chat-input {
  flex: 1;
  height: 72rpx;
  font-size: 30rpx;
  color: #2e3443;
}

.counter {
  font-size: 20rpx;
  color: #8b91a0;
  min-width: 76rpx;
  text-align: right;
}

.send-btn {
  padding: 0 36rpx;
  height: 72rpx;
  line-height: 72rpx;
  border-radius: 999rpx;
  font-size: 28rpx;
  font-weight: 600;
  color: #8b91a0;
  background-color: #edf0f6;
}

.send-btn.is-active {
  color: #fff;
  background: linear-gradient(135deg, #ffb7a0 0%, #ff8a8a 100%);
  box-shadow: 0 8rpx 16rpx rgba(255, 138, 138, 0.35);
}

.send-btn.is-stop {
  color: #fff;
  background: linear-gradient(135deg, #8ab9ff 0%, #5e87ff 100%);
  box-shadow: 0 8rpx 16rpx rgba(94, 135, 255, 0.25);
}
</style>
