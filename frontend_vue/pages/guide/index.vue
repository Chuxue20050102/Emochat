<template>
  <view class="guide-container">
    <swiper class="swiper" :current="currentIndex" @change="onSwiperChange" :indicator-dots="false" :autoplay="false">
      <swiper-item>
        <view class="page-content">
          <view class="hero-gradient page1-bg"></view>
          <view class="illustration-container">
            <image src="../../static/images/thinking-by-window.jpg" mode="aspectFill" class="illustration-image"></image>
          </view>
          <view class="text-section">
            <view class="title">每一种情绪都值得被看见</view>
            <view class="subtitle">在快节奏里，给自己留一点慢下来的空间</view>
          </view>
        </view>
      </swiper-item>

      <swiper-item>
        <view class="page-content">
          <view class="hero-gradient page2-bg"></view>
          <view class="illustration-container">
            <image src="../../static/images/journal-emotion-record.jpg.jpg" mode="aspectFill" class="illustration-image"></image>
          </view>
          <view class="text-section">
            <view class="title">记录，会让内心变清晰</view>
            <view class="subtitle">写下今天，明天你会更懂自己</view>
          </view>
        </view>
      </swiper-item>

      <swiper-item>
        <view class="page-content">
          <view class="hero-gradient page3-bg"></view>
          <view class="illustration-container">
            <image src="../../static/images/ai-chat-conversation.jpg" mode="aspectFill" class="illustration-image"></image>
          </view>
          <view class="text-section">
            <view class="title">你想聊的时候，我都在</view>
            <view class="subtitle">不评判，不催促，只是陪你慢慢说</view>
          </view>
        </view>
      </swiper-item>

      <swiper-item>
        <GuideSelection :selectedNeed="selectedNeed" @select="selectNeed" @skip="skipGuide" />
      </swiper-item>

      <swiper-item>
        <GuideDynamic :dynamicContent="dynamicContent" />
      </swiper-item>
    </swiper>

    <view class="bottom-controls">
      <view class="dots-container" v-if="currentIndex < 4">
        <view class="dot" :class="{ active: currentIndex === 0 }"></view>
        <view class="dot" :class="{ active: currentIndex === 1 }"></view>
        <view class="dot" :class="{ active: currentIndex === 2 }"></view>
        <view class="dot" :class="{ active: currentIndex === 3 }"></view>
      </view>

      <view class="action-btn" :class="{ 'full-width': currentIndex >= 3 }" @click="handleNext">
        <text class="btn-text">{{ buttonText }}</text>
        <text class="arrow" v-if="currentIndex < 3">Go</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { computed, ref } from 'vue'
import GuideDynamic from './components/GuideDynamic.vue'
import GuideSelection from './components/GuideSelection.vue'

const currentIndex = ref(0)
const selectedNeed = ref('record')

const dynamicContentMap = {
  record: {
    hint: '你想整理今天的情绪',
    title: '从记录开始',
    subtitle: '把感受落在文字里，心会慢慢变稳',
    description: '记录不是任务，而是和自己站在一起。',
    image: '/static/images/record-emotion.jpg',
    features: [
      { icon: '01', text: '轻量记录，不打扰节奏' },
      { icon: '02', text: '可视化趋势，看到变化' },
      { icon: '03', text: '专属空间，安心表达' },
    ],
    btn: '开启记录',
    path: '/pages/login/index',
  },
  chat: {
    hint: '你需要一个倾听者',
    title: '和 AI 慢慢聊',
    subtitle: '从一句“我有点累”开始也可以',
    description: '当你不想解释太多，也可以被理解。',
    image: '/static/images/ai-chat.jpg',
    features: [
      { icon: '01', text: '全天候可聊' },
      { icon: '02', text: '连续上下文陪伴' },
      { icon: '03', text: '温和、非评判' },
    ],
    btn: '进入陪聊',
    path: '/pages/login/index',
  },
  understand: {
    hint: '你想更了解自己',
    title: '看见情绪规律',
    subtitle: '理解触发点，情绪会更可控',
    description: '当你理解自己，很多焦虑会慢慢松开。',
    image: '/static/images/emotion-exploration.jpg',
    features: [
      { icon: '01', text: '追踪心情波动' },
      { icon: '02', text: '识别高频触发场景' },
      { icon: '03', text: '建立自己的节奏' },
    ],
    btn: '开始探索',
    path: '/pages/login/index',
  },
}

const dynamicContent = computed(() => dynamicContentMap[selectedNeed.value])

const buttonText = computed(() => {
  if (currentIndex.value < 3) return ''
  if (currentIndex.value === 3) return '继续'
  return dynamicContent.value.btn
})

const onSwiperChange = (e) => {
  currentIndex.value = e.detail.current
}

const selectNeed = (type) => {
  selectedNeed.value = type
}

const handleNext = () => {
  if (currentIndex.value < 4) {
    currentIndex.value += 1
  } else {
    uni.reLaunch({ url: dynamicContent.value.path })
  }
}

const skipGuide = () => {
  uni.reLaunch({ url: '/pages/login/index' })
}
</script>

<style lang="scss" scoped>
.guide-container {
  height: 100vh;
  width: 100vw;
  position: relative;
  display: flex;
  flex-direction: column;
}

.swiper {
  flex: 1;
  height: 100%;
}

.page-content {
  height: 100%;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
  padding-top: 86rpx;
}

.hero-gradient {
  position: absolute;
  top: -120rpx;
  left: -80rpx;
  width: 130%;
  height: 780rpx;
  filter: blur(70rpx);
  z-index: 0;
  opacity: 0.85;
}

.page1-bg {
  background: radial-gradient(circle at 26% 40%, rgba(141, 187, 255, 0.42) 0%, transparent 58%),
    radial-gradient(circle at 76% 72%, rgba(255, 177, 165, 0.36) 0%, transparent 52%);
}

.page2-bg {
  background: radial-gradient(circle at 20% 30%, rgba(142, 222, 195, 0.4) 0%, transparent 55%),
    radial-gradient(circle at 74% 66%, rgba(255, 213, 167, 0.34) 0%, transparent 55%);
}

.page3-bg {
  background: radial-gradient(circle at 24% 46%, rgba(210, 177, 255, 0.42) 0%, transparent 56%),
    radial-gradient(circle at 80% 66%, rgba(154, 203, 255, 0.36) 0%, transparent 54%);
}

.illustration-container {
  position: relative;
  z-index: 1;
  height: 510rpx;
  margin: 36rpx 40rpx 0;
  border-radius: 38rpx;
  overflow: hidden;
  box-shadow: 0 24rpx 40rpx rgba(43, 56, 94, 0.16);
}

.illustration-image {
  width: 100%;
  height: 100%;
}

.text-section {
  position: relative;
  z-index: 1;
  padding: 42rpx 52rpx 0;
  text-align: center;
}

.title {
  font-size: 52rpx;
  font-weight: 700;
  line-height: 1.3;
  color: #1f2943;
}

.subtitle {
  margin-top: 20rpx;
  font-size: 30rpx;
  line-height: 1.55;
  color: #5f6a84;
}

.bottom-controls {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  padding: 24rpx 44rpx 56rpx;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dots-container {
  display: flex;
  gap: 10rpx;
}

.dot {
  width: 14rpx;
  height: 14rpx;
  border-radius: 999rpx;
  background: rgba(153, 164, 188, 0.4);
  transition: all 0.24s ease;
}

.dot.active {
  width: 34rpx;
  background: linear-gradient(120deg, #8fb8ff, #7fd7b9);
}

.action-btn {
  width: 120rpx;
  height: 120rpx;
  border-radius: 50%;
  background: linear-gradient(130deg, #ff8e84 0%, #ffbd9f 100%);
  box-shadow: 0 14rpx 28rpx rgba(255, 145, 133, 0.36);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.action-btn.full-width {
  width: 100%;
  height: 102rpx;
  border-radius: 999rpx;
}

.btn-text {
  font-size: 30rpx;
  font-weight: 600;
}

.arrow {
  font-size: 24rpx;
  margin-left: 8rpx;
}
</style>
