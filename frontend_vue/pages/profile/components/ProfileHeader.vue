<template>
  <view class="header-section">
    <view class="user-info">
      <view class="avatar">{{ nickname.slice(0, 1) }}</view>
      <view class="info-text">
        <view class="nickname-row">
          <view class="nickname">{{ nickname }}</view>
          <view class="edit-btn" @click="emit('editNickname')">编辑</view>
        </view>
        <view class="streak-badge">已记录 {{ streakDays }} 次</view>
        <view class="status-text">{{ statusText }}</view>
      </view>
    </view>
    <view class="action-btn" @click="logout">退出</view>
  </view>
</template>

<script setup>
import { computed } from 'vue'

const emit = defineEmits(['editNickname'])

const props = defineProps({
  nickname: { type: String, default: '用户' },
  streakDays: { type: Number, default: 0 },
})

const statusText = computed(() => {
  if (props.streakDays === 0) return '这里会慢慢收集你留下的情绪线索。'
  if (props.streakDays < 5) return '你已经开始认真看见自己的感受了。'
  if (props.streakDays < 15) return '这段时间你一直在认真照顾自己。'
  return '你已经留下了不少线索，回头看会更看见自己。'
})

const logout = () => {
  uni.removeStorageSync('isLogin')
  uni.removeStorageSync('user_id')
  uni.removeStorageSync('nickname')
  if (typeof uni.$emit === 'function') {
    uni.$emit('nicknameUpdated', '')
  }
  uni.reLaunch({ url: '/pages/login/index' })
}
</script>

<style lang="scss" scoped>
.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.avatar {
  width: 90rpx;
  height: 90rpx;
  border-radius: 50%;
  background: linear-gradient(135deg, #d9a27f, #5c836f);
  border: 2rpx solid rgba(255, 255, 255, 0.85);
  color: #fff;
  font-size: 38rpx;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

.nickname {
  font-size: 36rpx;
  font-weight: 700;
  color: $emo-text-main;
}

.nickname-row {
  display: flex;
  align-items: center;
  gap: 12rpx;
}

.edit-btn {
  padding: 4rpx 12rpx;
  border-radius: 999rpx;
  font-size: 20rpx;
  color: $emo-sage-text;
  background: rgba(237, 250, 243, 0.86);
}

.streak-badge {
  margin-top: 6rpx;
  display: inline-block;
  padding: 6rpx 14rpx;
  border-radius: 999rpx;
  font-size: 22rpx;
  color: $emo-sage-text;
  background: rgba(237, 250, 243, 0.86);
}

.status-text {
  margin-top: 10rpx;
  font-size: 22rpx;
  line-height: 1.45;
  color: $emo-text-sub;
}

.action-btn {
  padding: 12rpx 22rpx;
  border-radius: 999rpx;
  font-size: 24rpx;
  color: $emo-text-sub;
  background: rgba(255, 255, 255, 0.65);
  border: 2rpx solid rgba(255, 255, 255, 0.86);
}
</style>
