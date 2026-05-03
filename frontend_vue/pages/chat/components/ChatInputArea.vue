<template>
  <view class="input-area" :style="areaStyle">
    <view class="input-panel">
      <view v-if="showArchiveAction" class="tool-row">
        <text class="tool-hint">如果这段对你重要，可以轻轻留下来</text>
        <view class="tool-action" :class="{ disabled: archiveDisabled }" @click="handleArchive">
          {{ archiveDisabled ? '正在留下' : '把这段留下来' }}
        </view>
      </view>

      <view class="input-wrapper">
        <textarea
          class="chat-input"
          v-model="localText"
          :placeholder="isStreaming ? '我正在认真回应...' : placeholder"
          :disabled="disabled"
          auto-height
          :adjust-position="false"
          :cursor-spacing="cursorSpacing"
          :show-confirm-bar="false"
          :disable-default-padding="true"
          maxlength="300"
          @focus="handleFocus"
          @blur="handleBlur"
        />
        <view v-if="showCounter" class="counter">{{ localText.length }}/300</view>
        <view class="send-btn" :class="buttonClass" @click="handleButtonClick">
          {{ buttonText }}
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { computed, ref, watch } from 'vue'

const props = defineProps({
  archiveDisabled: {
    type: Boolean,
    default: false,
  },
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
    default: '说说此刻的想法',
  },
  showArchiveAction: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['archive', 'blur', 'focus', 'send', 'stop'])
const localText = ref('')

const canSend = computed(() => !props.disabled && localText.value.trim().length > 0)
const showCounter = computed(() => localText.value.length >= 240)
const buttonText = computed(() => (props.isStreaming ? '停' : '说'))
const buttonClass = computed(() => ({
  'is-active': canSend.value,
  'is-stop': props.isStreaming,
}))
const areaStyle = computed(() => ({
  transform: props.bottomOffset > 0 ? `translateY(-${props.bottomOffset}px)` : 'translateY(0)',
}))

const handleArchive = () => {
  if (props.archiveDisabled) return
  emit('archive')
}

const handleSend = () => {
  if (!canSend.value) return
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
  padding: 8rpx 20rpx calc(env(safe-area-inset-bottom) + 16rpx);
  background:
    linear-gradient(180deg, rgba(247, 239, 232, 0), rgba(247, 239, 232, 0.88) 28%, #f7efe8 100%);
  transition: transform 0.22s ease;
}

.input-panel {
  padding: 10rpx;
  border-radius: 34rpx;
  background: rgba(255, 255, 255, 0.58);
  border: 1rpx solid rgba(255, 255, 255, 0.82);
  box-shadow: 0 24rpx 52rpx rgba(69, 50, 38, 0.12);
  backdrop-filter: blur(24rpx);
}

.tool-row {
  min-height: 46rpx;
  padding: 0 8rpx 8rpx 12rpx;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 14rpx;
}

.tool-hint {
  min-width: 0;
  font-size: 20rpx;
  color: #8a766a;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.tool-action {
  flex-shrink: 0;
  padding: 7rpx 14rpx;
  border-radius: 999rpx;
  font-size: 20rpx;
  font-weight: 700;
  color: #365f4d;
  background: rgba(237, 250, 243, 0.9);
  border: 1rpx solid rgba(183, 226, 203, 0.82);
}

.tool-action.disabled {
  opacity: 0.5;
}

.input-wrapper {
  min-height: 82rpx;
  display: flex;
  align-items: center;
  gap: 12rpx;
  background: rgba(255, 255, 255, 0.94);
  border: 1rpx solid rgba(230, 219, 208, 0.8);
  border-radius: 26rpx;
  padding: 8rpx 10rpx 8rpx 24rpx;
}

.chat-input {
  flex: 1;
  min-height: 68rpx;
  max-height: 220rpx;
  padding: 14rpx 0;
  font-size: 28rpx;
  line-height: 40rpx;
  color: #2f2925;
  overflow-y: auto;
}

.counter {
  margin-bottom: 18rpx;
  font-size: 19rpx;
  color: #a4958b;
  min-width: 72rpx;
  text-align: right;
}

.send-btn {
  flex-shrink: 0;
  width: 66rpx;
  height: 66rpx;
  border-radius: 22rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24rpx;
  font-weight: 800;
  color: #a4958b;
  background-color: #f5eee6;
}

.send-btn.is-active {
  color: #ffffff;
  background: linear-gradient(135deg, #4f7665 0%, #2f5d50 100%);
  box-shadow: 0 12rpx 26rpx rgba(47, 93, 80, 0.25);
}

.send-btn.is-stop {
  color: #ffffff;
  background: linear-gradient(135deg, #c08a63 0%, #9e6749 100%);
  box-shadow: 0 12rpx 26rpx rgba(158, 103, 73, 0.22);
}
</style>
