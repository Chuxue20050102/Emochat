<template>
  <view>
    <view class="floating-tabbar">
      <view class="tab-item" :class="{ active: currentTab === 'index' }" @click="switchTab('index')">
        <text class="tab-icon">⌂</text>
        <text class="tab-text">今天</text>
      </view>
      <view class="tab-item" :class="{ active: currentTab === 'record' }" @click="switchTab('record')">
        <text class="tab-icon">+</text>
        <text class="tab-text">记录</text>
      </view>
      <view class="tab-item" :class="{ active: currentTab === 'chat' }" @click="switchTab('chat')">
        <text class="tab-icon">~</text>
        <text class="tab-text">陪聊</text>
      </view>
      <view class="tab-item" :class="{ active: currentTab === 'profile' }" @click="switchTab('profile')">
        <text class="tab-icon">◎</text>
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
    record: '/pages/emotion-record/index',
    chat: '/pages/chat/index',
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
  height: 116rpx;
  padding: 0 14rpx;
  border-radius: 999rpx;
  background: rgba(255, 252, 247, 0.82);
  border: 2rpx solid rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(24rpx);
  box-shadow: 0 18rpx 46rpx rgba(74, 54, 40, 0.14);
  display: flex;
  align-items: center;
  justify-content: space-between;
  z-index: 999;
}

.tab-item {
  width: 24%;
  height: 88rpx;
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
  font-size: 25rpx;
  line-height: 1;
  color: #9a897d;
}

.tab-text {
  font-size: 20rpx;
  color: #9a897d;
}

.tab-item.active {
  background: linear-gradient(135deg, rgba(237, 250, 243, 0.94), rgba(255, 244, 232, 0.9));
}

.tab-item.active .tab-icon,
.tab-item.active .tab-text {
  color: #365f4d;
  font-weight: 700;
}
</style>
