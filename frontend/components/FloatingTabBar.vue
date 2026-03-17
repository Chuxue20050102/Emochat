<template>
  <view>
    <!-- 底部安全留白，避免内容被浮动导航栏遮挡 -->
    <view class="ios-padding-bottom"></view>

    <!-- 模拟真实 iOS 圆角浮动导航栏 -->
    <view class="floating-tabbar">
      <view class="tab-item" :class="{ active: currentTab === 'index' }" @click="switchTab('index')">
        <text class="tab-icon">🏠</text>
        <text class="tab-text">首页</text>
      </view>
      <view class="tab-item" :class="{ active: currentTab === 'record' }" @click="switchTab('record')">
        <text class="tab-icon">📝</text>
        <text class="tab-text">记录</text>
      </view>
      <view class="tab-item" :class="{ active: currentTab === 'chat' }" @click="switchTab('chat')">
        <text class="tab-icon">💬</text>
        <text class="tab-text">AI 聊天</text>
      </view>
      <view class="tab-item" :class="{ active: currentTab === 'profile' }" @click="switchTab('profile')">
        <text class="tab-icon">👤</text>
        <text class="tab-text">档案</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  currentTab: {
    type: String,
    default: 'index'
  }
})

const switchTab = (tab) => {
  if (props.currentTab === tab) return
  
  const pathMap = {
    'index': '/pages/index/index',
    'chat': '/pages/chat/index',
    'record': '/pages/emotion-record/index',
    'profile': '/pages/profile/index'
  }
  
  uni.switchTab({
    url: pathMap[tab]
  })
}
</script>

<style scoped>
/* --- 自定义浮动底部导航栏 (iOS Rounded Floating TabBar) --- */
.ios-padding-bottom {
  height: 180rpx;
  width: 100%;
}

.floating-tabbar {
  position: fixed;
  bottom: 50rpx;
  left: 40rpx;
  right: 40rpx;
  height: 120rpx;
  background: rgba(255, 255, 255, 0.85); /* 毛玻璃主体 */
  backdrop-filter: blur(30px);
  border-radius: 60rpx; /* 超大圆柱体药丸边界 */
  box-shadow: 0 16rpx 50rpx rgba(0, 0, 0, 0.06); /* 底部空间立体的弥散透光 */
  display: flex;
  justify-content: space-around;
  align-items: center;
  z-index: 999;
  padding: 0 20rpx;
}
.tab-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8rpx;
  padding: 10rpx 20rpx;
  transition: transform 0.2s;
}
.tab-item:active {
  transform: scale(0.9);
}
.tab-icon {
  font-size: 42rpx;
  opacity: 0.5;
  filter: grayscale(1);
  transition: all 0.3s;
}
.tab-text {
  font-size: 20rpx;
  color: #999;
  transition: all 0.3s;
}
.tab-item.active .tab-icon {
  opacity: 1;
  filter: grayscale(0);
}
.tab-item.active .tab-text {
  color: #1A1A1A;
  font-weight: 600;
}
</style>
