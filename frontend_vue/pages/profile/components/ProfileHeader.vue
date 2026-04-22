<template>
  <view class="header-section">
    <view class="user-info">
      <view class="avatar">{{ nickname.slice(0, 1) }}</view>
      <view class="info-text">
        <view class="nickname">{{ nickname }}</view>
        <view class="streak-badge">已记录 {{ streakDays }} 次</view>
      </view>
    </view>
    <view class="action-btn" @click="logout">退出</view>
  </view>
</template>

<script setup>
defineProps({
  nickname: { type: String, default: '用户' },
  streakDays: { type: Number, default: 0 },
})

const logout = () => {
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
  background: linear-gradient(135deg, rgba(255, 157, 147, 0.92), rgba(140, 186, 255, 0.95));
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
  color: #1f2942;
}

.streak-badge {
  margin-top: 6rpx;
  display: inline-block;
  padding: 6rpx 14rpx;
  border-radius: 999rpx;
  font-size: 22rpx;
  color: #3e557f;
  background: rgba(141, 187, 255, 0.24);
}

.action-btn {
  padding: 12rpx 22rpx;
  border-radius: 999rpx;
  font-size: 24rpx;
  color: #69738b;
  background: rgba(255, 255, 255, 0.65);
  border: 2rpx solid rgba(223, 230, 246, 0.9);
}
</style>
