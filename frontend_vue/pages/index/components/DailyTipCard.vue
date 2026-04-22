<template>
  <view class="tip-card">
    <view class="tip-head">
      <text class="tip-tag">Daily Note</text>
      <text class="tip-title">情绪小贴士</text>
    </view>
    <text class="tip-content">{{ dailyTip }}</text>
  </view>
</template>

<script setup>
const tips = [
  '先描述感受，再谈解决方法，心会更稳。',
  '今天允许自己慢一点，情绪也需要呼吸。',
  '当你说出“我现在很累”，其实已经在照顾自己。',
  '记录一次真实感受，比假装没事更有力量。',
]

const dailyTip = tips[Math.floor(Math.random() * tips.length)]
</script>

<style lang="scss" scoped>
.tip-card {
  padding: 28rpx 30rpx;
  border-radius: 30rpx;
  background: rgba(255, 255, 255, 0.72);
  border: 2rpx solid rgba(255, 255, 255, 0.84);
  box-shadow: 0 14rpx 36rpx rgba(42, 54, 88, 0.12);
}

.tip-head {
  display: flex;
  align-items: center;
  gap: 12rpx;
  margin-bottom: 12rpx;
}

.tip-tag {
  padding: 4rpx 12rpx;
  border-radius: 999rpx;
  background: rgba(141, 187, 255, 0.23);
  color: #365a95;
  font-size: 18rpx;
}

.tip-title {
  font-size: 30rpx;
  font-weight: 600;
  color: #212b45;
}

.tip-content {
  font-size: 26rpx;
  color: #61708a;
  line-height: 1.6;
}
</style>
