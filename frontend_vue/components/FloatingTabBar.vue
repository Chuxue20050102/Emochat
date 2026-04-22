<template>
  <view>
    <view class="floating-tabbar">
      <view class="tab-item" :class="{ active: currentTab === 'index' }" @click="switchTab('index')">
        <text class="tab-icon">Ho</text>
        <text class="tab-text">首页</text>
      </view>
      <view class="tab-item" :class="{ active: currentTab === 'record' }" @click="switchTab('record')">
        <text class="tab-icon">Re</text>
        <text class="tab-text">记录</text>
      </view>
      <view class="tab-item" :class="{ active: currentTab === 'chat' }" @click="switchTab('chat')">
        <text class="tab-icon">AI</text>
        <text class="tab-text">陪聊</text>
      </view>
      <view class="tab-item" :class="{ active: currentTab === 'profile' }" @click="switchTab('profile')">
        <text class="tab-icon">Me</text>
        <text class="tab-text">档案</text>
      </view>
    </view>
  </view>
</template>

<script setup>
const props = defineProps({
  currentTab: {
    type: String,
    default: 'index',
  },
})

const switchTab = (tab) => {
  if (props.currentTab === tab) return

  const pathMap = {
    index: '/pages/index/index',
    chat: '/pages/chat/index',
    record: '/pages/emotion-record/index',
    profile: '/pages/profile/index',
  }

  uni.switchTab({ url: pathMap[tab] })
}
</script>

<style scoped>
.floating-tabbar {
  position: fixed;
  left: 34rpx;
  right: 34rpx;
  bottom: 42rpx;
  height: 118rpx;
  padding: 0 14rpx;
  border-radius: 999rpx;
  background: rgba(255, 255, 255, 0.78);
  border: 2rpx solid rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(24rpx);
  box-shadow: 0 18rpx 46rpx rgba(34, 41, 71, 0.16);
  display: flex;
  align-items: center;
  justify-content: space-between;
  z-index: 999;
}

.tab-item {
  width: 24%;
  height: 90rpx;
  border-radius: 999rpx;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 4rpx;
  transition: all 0.24s ease;
}

.tab-item:active {
  transform: scale(0.96);
}

.tab-icon {
  font-size: 18rpx;
  line-height: 1;
  color: #7f889c;
  letter-spacing: 0.5rpx;
}

.tab-text {
  font-size: 20rpx;
  color: #8a92a6;
}

.tab-item.active {
  background: linear-gradient(130deg, rgba(141, 187, 255, 0.24), rgba(142, 222, 195, 0.28));
}

.tab-item.active .tab-icon {
  color: #2a3350;
  font-weight: 700;
}

.tab-item.active .tab-text {
  color: #25304b;
  font-weight: 600;
}
</style>
