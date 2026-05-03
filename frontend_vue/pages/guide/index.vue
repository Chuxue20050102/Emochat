<template>
  <view class="guide-container">
    <view class="hero-gradient"></view>

    <view class="top-bar">
      <text class="brand">EmoChat</text>
      <text class="skip-btn" @click="finishGuide">跳过</text>
    </view>

    <swiper class="swiper" :current="currentIndex" @change="onSwiperChange" :indicator-dots="false" :autoplay="false">
      <swiper-item v-for="(item, index) in slides" :key="item.title">
        <view class="page-content">
          <view v-if="item.image" class="illustration-card">
            <image :src="item.image" mode="aspectFill" class="illustration-image"></image>
          </view>

          <view v-else class="intent-card">
            <text class="intent-eyebrow">先从你现在需要的开始</text>
            <view
              v-for="option in intentOptions"
              :key="option.value"
              class="intent-option"
              :class="{ active: selectedIntent === option.value }"
              @click="selectIntent(option.value)"
            >
              <view>
                <text class="intent-title">{{ option.title }}</text>
                <text class="intent-desc">{{ option.desc }}</text>
              </view>
              <text class="intent-mark">{{ selectedIntent === option.value ? '已选' : '选择' }}</text>
            </view>
          </view>

          <view class="text-section" :class="{ 'is-intent': index === slides.length - 1 }">
            <text class="step-label">{{ item.label }}</text>
            <view class="title">{{ item.title }}</view>
            <view class="subtitle">{{ item.subtitle }}</view>
          </view>
        </view>
      </swiper-item>
    </swiper>

    <view class="bottom-controls">
      <view class="progress-track">
        <view class="progress-fill" :style="{ width: progressWidth }"></view>
      </view>

      <view class="bottom-row">
        <view class="action-btn" @click="handleNext">
          <text class="btn-text">{{ buttonText }}</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { computed, ref } from 'vue'

const ONBOARDING_INTENT_KEY = 'onboarding_intent'

const currentIndex = ref(0)
const selectedIntent = ref('record')

const slides = [
  {
    label: '01 理念',
    title: '有些感受，不一定要马上说清楚。',
    subtitle: '你可以慢一点，先把自己放下来。这里不是要求你立刻变好，而是陪你先看见自己。',
    image: '/static/images/thinking-by-window.jpg',
  },
  {
    label: '02 记录',
    title: '记录每天的心情，也可以只写一句话。',
    subtitle: '开心、低落、焦虑、平静，都可以被温柔地留下来。它们不是负担，是你生活里的线索。',
    image: '/static/images/record-emotion.jpg',
  },
  {
    label: '03 陪聊',
    title: '想说的时候，就和我慢慢聊。',
    subtitle: '当你有点乱、说不清，EmoChat 会陪你整理感受，也会帮你回看最近的状态。',
    image: '/static/images/ai-chat-conversation.jpg',
  },
  {
    label: '04 开始',
    title: '今天你更想从哪里开始？',
    subtitle: '选一个最接近此刻状态的入口。之后也可以随时切换，不用一次选对。',
    image: '',
  },
]

const intentOptions = [
  {
    value: 'record',
    title: '记录一下',
    desc: '把今天的心情先放下来',
  },
  {
    value: 'chat',
    title: '找人聊聊',
    desc: '让陪聊帮你慢慢理一理',
  },
  {
    value: 'profile',
    title: '看看状态',
    desc: '回看最近留下的情绪线索',
  },
]

const buttonText = computed(() => (currentIndex.value === slides.length - 1 ? '开始使用' : '下一步'))
const progressWidth = computed(() => `${((currentIndex.value + 1) / slides.length) * 100}%`)

const onSwiperChange = (e) => {
  currentIndex.value = e.detail.current
}

const selectIntent = (value) => {
  selectedIntent.value = value
}

const finishGuide = () => {
  uni.setStorageSync(ONBOARDING_INTENT_KEY, selectedIntent.value)
  uni.reLaunch({ url: '/pages/login/index' })
}

const handleNext = () => {
  if (currentIndex.value < slides.length - 1) {
    currentIndex.value += 1
    return
  }
  finishGuide()
}
</script>

<style lang="scss" scoped>
.guide-container {
  height: 100vh;
  width: 100vw;
  position: relative;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: $emo-page-bg;
}

.hero-gradient {
  position: absolute;
  top: -160rpx;
  left: -120rpx;
  right: -120rpx;
  height: 760rpx;
  filter: blur(72rpx);
  z-index: 0;
  opacity: 0.9;
  background: $emo-page-glow;
  pointer-events: none;
}

.top-bar {
  position: relative;
  z-index: 2;
  padding: calc(env(safe-area-inset-top) + 34rpx) 38rpx 8rpx;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.brand {
  font-size: 28rpx;
  font-weight: 800;
  letter-spacing: 0.04em;
  color: #365f4d;
}

.skip-btn {
  padding: 10rpx 18rpx;
  border-radius: 999rpx;
  font-size: 24rpx;
  color: #7a6b62;
  background: rgba(255, 255, 255, 0.52);
  border: 1rpx solid rgba(255, 255, 255, 0.76);
}

.swiper {
  flex: 1;
  min-height: 0;
  position: relative;
  z-index: 1;
}

.page-content {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 34rpx 38rpx 260rpx;
  box-sizing: border-box;
}

.illustration-card {
  height: 500rpx;
  border-radius: 42rpx;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.58);
  border: 1rpx solid rgba(255, 255, 255, 0.82);
  box-shadow: 0 28rpx 58rpx rgba(74, 54, 40, 0.14);
}

.illustration-image {
  width: 100%;
  height: 100%;
}

.intent-card {
  padding: 24rpx;
  border-radius: 42rpx;
  background:
    linear-gradient(150deg, rgba(255, 255, 255, 0.82), rgba(255, 249, 242, 0.66)),
    radial-gradient(circle at 100% 0%, rgba(143, 184, 160, 0.18), transparent 45%);
  border: 1rpx solid rgba(255, 255, 255, 0.86);
  box-shadow: 0 28rpx 58rpx rgba(74, 54, 40, 0.12);
}

.intent-eyebrow {
  display: block;
  margin-bottom: 18rpx;
  font-size: 23rpx;
  color: #8a766a;
}

.intent-option {
  min-height: 112rpx;
  margin-top: 14rpx;
  padding: 20rpx;
  border-radius: 28rpx;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18rpx;
  background: rgba(255, 255, 255, 0.72);
  border: 1rpx solid rgba(230, 219, 208, 0.76);
  transition: all 0.22s ease;
}

.intent-option.active {
  background: rgba(237, 250, 243, 0.92);
  border-color: rgba(143, 184, 160, 0.72);
  box-shadow: 0 14rpx 30rpx rgba(72, 108, 88, 0.12);
}

.intent-title {
  display: block;
  font-size: 25rpx;
  font-weight: 800;
  color: #2f2925;
}

.intent-desc {
  display: block;
  margin-top: 8rpx;
  font-size: 23rpx;
  line-height: 1.4;
  color: #7a6b62;
}

.intent-mark {
  flex-shrink: 0;
  padding: 8rpx 14rpx;
  border-radius: 999rpx;
  font-size: 21rpx;
  color: #4f7665;
  background: rgba(255, 255, 255, 0.72);
}

.text-section {
  margin-top: 46rpx;
}

.text-section.is-intent {
  margin-top: 34rpx;
}

.step-label {
  display: inline-flex;
  padding: 8rpx 16rpx;
  border-radius: 999rpx;
  font-size: 21rpx;
  font-weight: 700;
  color: #5d6f62;
  background: rgba(237, 250, 243, 0.74);
  border: 1rpx solid rgba(183, 226, 203, 0.7);
}

.title {
  margin-top: 24rpx;
  font-size: 46rpx;
  font-weight: 900;
  line-height: 1.28;
  color: #2f2925;
}

.subtitle {
  margin-top: 18rpx;
  font-size: 28rpx;
  line-height: 1.62;
  color: #6e625b;
}

.bottom-controls {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 3;
  padding: 22rpx 38rpx calc(env(safe-area-inset-bottom) + 44rpx);
  background: linear-gradient(180deg, rgba(247, 239, 232, 0), #f7efe8 38%, #f7efe8 100%);
}

.progress-track {
  height: 8rpx;
  border-radius: 999rpx;
  background: rgba(180, 163, 151, 0.24);
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 999rpx;
  background: linear-gradient(120deg, #6f957e, #d7a379);
  transition: width 0.24s ease;
}

.bottom-row {
  margin-top: 26rpx;
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.action-btn {
  min-width: 218rpx;
  height: 88rpx;
  padding: 0 34rpx;
  border-radius: 999rpx;
  background: linear-gradient(135deg, #4f7665 0%, #2f5d50 100%);
  box-shadow: 0 18rpx 34rpx rgba(47, 93, 80, 0.25);
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-text {
  font-size: 28rpx;
  font-weight: 800;
  color: #ffffff;
}
</style>
