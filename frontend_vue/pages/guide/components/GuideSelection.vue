<template>
  <view class="page-content selection-page">
    <view class="header-section">
      <view class="skip-btn" @click="$emit('skip')">Skip</view>
      <view class="title-main">开始前，先了解你的此刻需求</view>
      <view class="subtitle-main">选择一条最接近你的方向</view>
    </view>

    <view class="options-container">
      <view class="option-card green-card" :class="{ selected: selectedNeed === 'record' }" @click="$emit('select', 'record')">
        <view class="option-title">情绪整理</view>
        <view class="option-desc">把今天的状态记录下来</view>
      </view>

      <view class="option-card peach-card" :class="{ selected: selectedNeed === 'chat' }" @click="$emit('select', 'chat')">
        <view class="option-title">放松陪聊</view>
        <view class="option-desc">想找个温柔的倾听者</view>
      </view>

      <view class="option-card blue-card" :class="{ selected: selectedNeed === 'understand' }" @click="$emit('select', 'understand')">
        <view class="option-title">了解自己</view>
        <view class="option-desc">看到情绪背后的规律</view>
      </view>
    </view>
  </view>
</template>

<script setup>
defineProps({
  selectedNeed: { type: String, default: 'record' },
})
defineEmits(['select', 'skip'])
</script>

<style lang="scss" scoped>
.page-content {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding-top: 90rpx;
}

.header-section {
  padding: 0 46rpx;
  position: relative;
}

.skip-btn {
  position: absolute;
  top: 0;
  right: 46rpx;
  font-size: 24rpx;
  color: #8690a7;
}

.title-main {
  margin-top: 58rpx;
  font-size: 48rpx;
  font-weight: 700;
  line-height: 1.28;
  color: #1f2943;
}

.subtitle-main {
  margin-top: 14rpx;
  font-size: 28rpx;
  color: #5f6a85;
}

.options-container {
  margin-top: 50rpx;
  padding: 0 40rpx;
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.option-card {
  min-height: 130rpx;
  border-radius: 28rpx;
  border: 2rpx solid transparent;
  padding: 28rpx 30rpx;
}

.option-title {
  font-size: 34rpx;
  font-weight: 700;
  color: #1f2840;
}

.option-desc {
  margin-top: 6rpx;
  font-size: 24rpx;
  color: #5e6780;
}

.green-card {
  background: linear-gradient(130deg, rgba(144, 224, 196, 0.35), rgba(205, 244, 229, 0.8));
}

.peach-card {
  background: linear-gradient(130deg, rgba(255, 177, 167, 0.34), rgba(255, 236, 220, 0.88));
}

.blue-card {
  background: linear-gradient(130deg, rgba(152, 195, 255, 0.35), rgba(224, 239, 255, 0.9));
}

.option-card.selected {
  border-color: rgba(55, 82, 133, 0.4);
  box-shadow: 0 14rpx 30rpx rgba(42, 55, 90, 0.12);
}
</style>
