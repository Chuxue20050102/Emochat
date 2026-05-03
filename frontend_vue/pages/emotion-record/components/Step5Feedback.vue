<template>
  <view class="feedback-page">
    <view class="feedback-card">
      <text class="feedback-icon">🍵</text>
      <view class="feedback-title">这条感受已经可以留下了</view>
      <view class="feedback-desc">保存后会进入情绪档案。也可以带着它聊一会儿，把没说完的部分慢慢说清楚。</view>

      <view class="summary-box">
        <view class="summary-line">心情：{{ summaryMood || '未选择' }}</view>
        <view class="summary-line">原因：{{ summaryReasons || '未填写' }}</view>
        <view class="summary-line">标签：{{ summarySubTags || '未填写' }}</view>
      </view>

      <view class="action-buttons">
        <button class="primary-btn action-btn" :disabled="saving" @click="$emit('save-and-chat')">
          {{ saving ? '保存中...' : '带着这条记录聊聊' }}
        </button>
        <button class="secondary-btn action-btn" :disabled="saving" @click="$emit('save-and-home')">
          先保存起来
        </button>
        <view class="text-back" @click="$emit('back')">返回上一步修改</view>
      </view>
    </view>
  </view>
</template>

<script setup>
defineProps({
  summaryMood: {
    type: String,
    default: '',
  },
  summaryReasons: {
    type: String,
    default: '',
  },
  summarySubTags: {
    type: String,
    default: '',
  },
  saving: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['save-and-chat', 'save-and-home', 'back'])
</script>

<style lang="scss" scoped>
.feedback-page {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 36rpx;
}

.feedback-card {
  width: 100%;
  background: rgba(255, 255, 255, 0.92);
  border-radius: 32rpx;
  padding: 56rpx 30rpx 36rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  border: 1rpx solid rgba(255, 255, 255, 0.9);
}

.feedback-icon {
  font-size: 84rpx;
  margin-bottom: 16rpx;
}

.feedback-title {
  font-size: 36rpx;
  font-weight: 700;
  color: $emo-text-main;
  margin-bottom: 10rpx;
}

.feedback-desc {
  font-size: 25rpx;
  color: $emo-text-sub;
  margin-bottom: 24rpx;
  line-height: 1.6;
}

.summary-box {
  width: 100%;
  border-radius: 20rpx;
  background: rgba(255, 252, 247, 0.78);
  border: 1rpx solid rgba(232, 219, 207, 0.8);
  padding: 18rpx 20rpx;
  margin-bottom: 24rpx;
  text-align: left;
}

.summary-line {
  font-size: 24rpx;
  color: $emo-text-main;
  line-height: 1.7;
}

.action-buttons {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 12rpx;
}

.action-btn {
  width: 100%;
}

.primary-btn {
  height: 92rpx;
  border-radius: 46rpx;
  background: linear-gradient(135deg, #5c836f, #3f6d59);
  color: #fff;
  font-size: 29rpx;
  font-weight: 600;
}

.secondary-btn {
  height: 90rpx;
  border-radius: 45rpx;
  background: rgba(255, 255, 255, 0.86);
  color: $emo-sage-text;
  border: 1rpx solid rgba(232, 219, 207, 0.8);
  font-size: 27rpx;
}

.text-back {
  margin-top: 6rpx;
  font-size: 24rpx;
  color: $emo-text-sub;
}
</style>
