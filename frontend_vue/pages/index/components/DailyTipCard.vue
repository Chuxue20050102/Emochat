<template>
  <view class="module-card tip-card">
    <view class="tip-header">
      <view class="tip-icon">💡</view>
      <view class="tip-title">今日情绪小贴士</view>
    </view>
    <view class="tip-content">{{ dailyTip }}</view>
  </view>
</template>

<script setup>
const tips = [
  '深呼吸是缓解情绪的有效方法，试着慢慢吸气4秒，屏息2秒，再慢慢呼气6秒',
  '写下你的感受可以帮助你理清思绪，试试每天花10分钟记录你的情绪',
  '适当的运动可以释放内啡肽，改善心情，即使只是简单的散步也有帮助',
  '给自己一个微笑，研究表明微笑可以减轻压力，改善情绪',
  '与朋友或家人分享你的感受，倾诉也是一种有效的情绪管理方式',
  '尝试冥想或正念练习，专注于当下可以帮助你缓解焦虑',
  '充足的睡眠对情绪管理至关重要，尽量保持规律的作息时间',
  '做一些你喜欢的事情，哪怕只是一小会儿，也能提升你的心情'
]

const getRandomTip = () => {
  const randomIndex = Math.floor(Math.random() * tips.length)
  return tips[randomIndex]
}

const dailyTip = getRandomTip()
</script>

<style lang="scss" scoped>
.tip-card {
  padding: 46rpx 40rpx 36rpx;
  background: rgba(255, 255, 255, 0.6);
  border: 1rpx solid rgba(255, 255, 255, 0.7);
  transition: all 0.3s ease;
  text-align: center;
}

.tip-card:hover {
  transform: translateY(-4rpx);
  box-shadow: 0 20rpx 48rpx rgba(0, 0, 0, 0.06);
  background: rgba(255, 255, 255, 0.7);
  border-color: rgba(255, 255, 255, 0.8);
}

.tip-header {
  display: flex;
  align-items: center;
  gap: 16rpx;
  margin-bottom: 20rpx;
  justify-content: center;
}

.tip-icon {
  font-size: 40rpx;
  flex-shrink: 0;
}

.tip-title {
  font-size: 32rpx;
  font-weight: 600;
  color: #333;
}

.tip-content {
  font-size: 26rpx;
  color: #666;
  line-height: 1.6;
  white-space: pre-line;
  text-align: center;
  padding: 0 20rpx;
}
</style>