<template>
  <view class="header-section">
    <view class="user-info">
      <view class="avatar"></view>
      <view class="info-text">
        <view class="nickname">{{ nickname }}</view>
        <view class="streak-badge">🔥 已连续记录 {{ streakDays }} 天</view>
      </view>
    </view>
    <view class="action-btn" @click="logout">退出</view>
  </view>
</template>

<script setup>
defineProps({
  nickname: { type: String, default: '孤单星星' },
  streakDays: { type: Number, default: 0 }
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
  margin-bottom: 50rpx;
}
.user-info {
  display: flex;
  align-items: center;
}
.avatar {
  width: 110rpx;
  height: 110rpx;
  border-radius: 50%;
  background: linear-gradient(135deg, #FF9B8C, #FFB0A4);
  margin-right: 24rpx;
  box-shadow: 0 10rpx 24rpx rgba(255,155,140,0.3);
  border: 4rpx solid rgba(255,255,255,0.9);
}
.nickname {
  font-size: 38rpx;
  color: #1A1A1A;
  font-weight: 600;
  margin-bottom: 8rpx;
}
.streak-badge {
  font-size: 24rpx;
  color: #FF7B54;
  background-color: rgba(255, 123, 84, 0.1);
  padding: 4rpx 16rpx;
  border-radius: 20rpx;
  display: inline-block;
}
.action-btn {
  font-size: 28rpx;
  color: #BDBDBD;
  padding: 12rpx 24rpx;
  border-radius: 30rpx;
  background: rgba(0,0,0,0.03);
  transition: all 0.2s;
}
.action-btn:active {
  background: rgba(0,0,0,0.06);
}
</style>
