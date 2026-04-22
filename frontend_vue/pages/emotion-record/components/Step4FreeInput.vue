<template>
  <view class="step-content">
    <view class="step-title">
      想说点什么吗
      <text class="sub-title-mark">（可选）</text>
    </view>
    <textarea
      class="free-input"
      :value="modelValue"
      placeholder="可以写下刚刚发生的事，或只是一些零碎的感受..."
      maxlength="500"
      :adjust-position="true"
      :cursor-spacing="cursorSpacing"
      @input="$emit('update:modelValue', $event.detail.value)"
      @focus="$emit('focus')"
      @blur="$emit('blur')"
    />
  </view>
</template>

<script setup>
defineProps({
  modelValue: {
    type: String,
    default: '',
  },
  bottomOffset: {
    type: Number,
    default: 0,
  },
  cursorSpacing: {
    type: Number,
    default: 120,
  },
})

defineEmits(['blur', 'focus', 'update:modelValue'])
</script>

<style lang="scss" scoped>
.step-content {
  display: flex;
  flex-direction: column;
  padding: 0 36rpx;
}

.step-title {
  font-size: 34rpx;
  line-height: 1.5;
  font-weight: 700;
  color: #25314a;
  margin-bottom: 20rpx;
}

.sub-title-mark {
  font-size: 24rpx;
  color: #8090ad;
  font-weight: 400;
  margin-left: 10rpx;
}

.free-input {
  width: 100%;
  min-height: 340rpx;
  max-height: 560rpx;
  background: rgba(255, 255, 255, 0.9);
  border: 1rpx solid rgba(223, 232, 247, 0.8);
  border-radius: 24rpx;
  padding: 24rpx;
  box-sizing: border-box;
  font-size: 30rpx;
  color: #1a1a1a;
  line-height: 1.6;
}

.free-input:focus {
  background: #ffffff;
  border-color: rgba(255, 155, 140, 0.35);
  box-shadow: 0 10rpx 30rpx rgba(255, 155, 140, 0.08);
}
</style>
