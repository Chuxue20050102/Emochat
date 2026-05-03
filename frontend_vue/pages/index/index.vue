<template>
  <view class="home-page">
    <view class="backdrop"></view>

    <scroll-view class="page-scroll" scroll-y>
      <view class="content-wrapper">
        <view class="topbar">
          <view class="brand-pill">EmoChat</view>
          <view class="date-pill">{{ todayLabel }}</view>
        </view>

        <GreetingCard />
        <TodayActionCard />
        <ChatEntryCard />

        <view class="ios-padding-bottom"></view>
      </view>
    </scroll-view>

    <FloatingTabBar currentTab="index" />
  </view>
</template>

<script setup>
import { computed } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import FloatingTabBar from '@/components/FloatingTabBar.vue'
import GreetingCard from './components/GreetingCard.vue'
import TodayActionCard from './components/TodayActionCard.vue'
import ChatEntryCard from './components/ChatEntryCard.vue'

const todayLabel = computed(() => {
  const d = new Date()
  const m = `${d.getMonth() + 1}`.padStart(2, '0')
  const day = `${d.getDate()}`.padStart(2, '0')
  return `${m}.${day}`
})

onShow(() => {
  uni.hideTabBar({ animation: false })
  showFirstHomeTip()
})

const showFirstHomeTip = () => {
  const key = 'home_first_tip_seen'
  if (uni.getStorageSync(key)) return
  uni.setStorageSync(key, true)
  setTimeout(() => {
    uni.showModal({
      title: '可以这样开始',
      content: '先选一个大概的状态，后面可以慢慢补充；想说说时，也可以直接找我聊聊。',
      confirmText: '知道了',
      showCancel: false,
    })
  }, 450)
}
</script>

<style lang="scss" scoped>
.home-page {
  min-height: 100vh;
  position: relative;
  overflow: hidden;
  background: $emo-page-bg;
}

.backdrop {
  position: absolute;
  inset: -14%;
  z-index: 0;
  filter: blur(72rpx);
  background: $emo-page-glow;
}

.page-scroll {
  position: relative;
  z-index: 1;
  height: 100vh;
}

.content-wrapper {
  padding: 94rpx 28rpx 24rpx;
  display: flex;
  flex-direction: column;
  gap: 20rpx;
  box-sizing: border-box;
}

.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rpx;
}

.brand-pill,
.date-pill {
  height: 52rpx;
  padding: 0 20rpx;
  border-radius: 999rpx;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.72);
  border: 1rpx solid rgba(255, 255, 255, 0.9);
  box-shadow: 0 8rpx 24rpx rgba(74, 54, 40, 0.08);
  color: $emo-text-sub;
}

.brand-pill {
  font-size: 19rpx;
  letter-spacing: 0;
  font-weight: 700;
}

.date-pill {
  font-size: 21rpx;
  font-weight: 600;
}

.ios-padding-bottom {
  height: 210rpx;
}
</style>
