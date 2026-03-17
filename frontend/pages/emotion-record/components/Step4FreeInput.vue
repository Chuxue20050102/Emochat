<template>
  <view class="step-content">
    <view class="step-title">想说点什么吗？<br/><text class="sub-title-mark">(可选)</text></view>
    <textarea 
      class="free-input" 
      :value="modelValue"
      @input="$emit('update:modelValue', $event.detail.value)"
      placeholder="可以写下刚刚发生的事，或者只是一些零碎的感受..."
      maxlength="500"
    />
  </view>
</template>

<script setup>
defineProps({
  modelValue: String
})
defineEmits(['update:modelValue'])
</script>

<style lang="scss" scoped>
.step-content {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 0 50rpx;
}
.step-title {
  font-size: 40rpx;
  line-height: 1.5;
  font-weight: 600;
  color: #1A1A1A;
  margin-bottom: 50rpx;
}
.sub-title-mark {
  font-size: 26rpx;
  color: #999;
  font-weight: normal;
  margin-left: 10rpx;
}
.free-input {
  width: 100%;
  flex: 1;
  max-height: 480rpx;
  background: rgba(255, 255, 255, 0.7);
  border: 2rpx solid transparent;
  border-radius: 30rpx;
  padding: 30rpx;
  box-sizing: border-box;
  font-size: 30rpx;
  color: #1A1A1A;
  line-height: 1.6;
}
.free-input:focus {
  background: #FFFFFF;
  border-color: rgba(255, 155, 140, 0.3);
  box-shadow: 0 10rpx 30rpx rgba(255, 155, 140, 0.05);
}
</style>
