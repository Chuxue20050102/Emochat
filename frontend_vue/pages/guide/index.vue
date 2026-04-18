<template>
  <view class="guide-container">
    <swiper class="swiper" :current="currentIndex" @change="onSwiperChange" :indicator-dots="false" :autoplay="false">
      <!-- 第1页: 情绪共鸣 -->
      <swiper-item>
        <view class="page-content">
          <view class="hero-gradient page1-bg"></view>
          <view class="illustration-container">
            <image src="../../static/images/thinking-by-window.jpg" mode="aspectFit" class="illustration-image"></image>
          </view>
          <view class="text-section">
            <view class="title">你的每一种情绪都值得被温柔看见</view>
            <view class="subtitle">那些未说出口的话，那些藏在心底的感受</view>
            <view class="subtitle">在这个快节奏的世界里</view>
            <view class="subtitle">给自己一点时间，倾听内心的声音</view>
          </view>
        </view>
      </swiper-item>

      <!-- 第2页: 解决方式 -->
      <swiper-item>
        <view class="page-content">
          <view class="hero-gradient page2-bg"></view>
          <view class="illustration-container">
            <image src="../../static/images/journal-emotion-record.jpg.jpg" mode="aspectFit" class="illustration-image"></image>
          </view>
          <view class="text-section">
            <view class="title">记录是与自己对话的最好方式</view>
            <view class="subtitle">当你写下每一份感受</view>
            <view class="subtitle">那些混乱的情绪会逐渐变得清晰</view>
            <view class="subtitle">时间会告诉你，记录的力量有多强大</view>
          </view>
        </view>
      </swiper-item>

      <!-- 第3页: 产品能力 -->
      <swiper-item>
        <view class="page-content">
          <view class="hero-gradient page3-bg"></view>
          <view class="illustration-container">
            <image src="../../static/images/ai-chat-conversation.jpg" mode="aspectFit" class="illustration-image"></image>
          </view>
          <view class="text-section">
            <view class="title">当你需要倾听时，AI 一直都在</view>
            <view class="subtitle">有时候，我们只是需要一个倾听者</view>
            <view class="subtitle">不需要评判，不需要建议</view>
            <view class="subtitle">只是静静地听你把话说完</view>
          </view>
        </view>
      </swiper-item>

      <!-- 第4页: 用户需求选择 (核心) -->
      <swiper-item>
        <GuideSelection :selectedNeed="selectedNeed" @select="selectNeed" @skip="skipGuide" />
      </swiper-item>

      <!-- 第5页: 动态结果页 -->
      <swiper-item>
        <GuideDynamic :dynamicContent="dynamicContent" />
      </swiper-item>
    </swiper>

    <!-- 底部导航控制区 -->
    <view class="bottom-controls">
      <!-- 分页指示器 (前4页显示) -->
      <view class="dots-container" v-if="currentIndex < 4">
        <view class="dot" :class="{'active': currentIndex === 0}"></view>
        <view class="dot" :class="{'active': currentIndex === 1}"></view>
        <view class="dot" :class="{'active': currentIndex === 2}"></view>
        <view class="dot" :class="{'active': currentIndex === 3}"></view>
      </view>
      <!-- 如果有更多组件要遮挡，可以保持这层级 -->
      <view class="dots-container" v-else>
        <view class="dot active"></view><view class="dot active"></view><view class="dot active"></view><view class="dot active"></view>
      </view>

      <!-- 右侧/底部按钮 -->
      <view class="action-btn" :class="{'full-width': currentIndex >= 3}" @click="handleNext">
        <text class="btn-text">{{ buttonText }}</text>
        <text class="arrow" v-if="currentIndex < 3">→</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed } from 'vue'
import GuideSelection from './components/GuideSelection.vue'
import GuideDynamic from './components/GuideDynamic.vue'

const currentIndex = ref(0)
const selectedNeed = ref('record') // 默认选择

const dynamicContentMap = {
  'record': {
    hint: '今天想整理一下自己的情绪',
    title: '用记录与情绪对话',
    subtitle: '把每天的感受简单记录下来<br>慢慢看见自己的情绪变化轨迹',
    description: '记录不仅仅是文字的堆砌，更是与自己内心的对话。通过每天的记录，你会逐渐发现情绪的变化规律，学会更好地理解和管理自己的情绪。',
    image: '/static/images/record-emotion.jpg',
    features: [
      { icon: '📝', text: '简单记录，轻松上手' },
      { icon: '📊', text: '情绪趋势一目了然' },
      { icon: '🔒', text: '隐私保护，安全可靠' }
    ],
    btn: '开始记录 →',
    path: '/pages/login/index'
  },
  'chat': {
    hint: '想找个地方聊聊天',
    title: 'AI 陪你聊聊心里话',
    subtitle: '如果有想说的话<br>可以和 AI 慢慢聊一聊，释放内心压力',
    description: '有时候，我们只是需要一个倾听者，不需要评判，不需要建议。AI 会耐心倾听你的每一句话，给你最温暖的回应，让你感受到被理解和被关心。',
    image: '/static/images/ai-chat.jpg',
    features: [
      { icon: '💬', text: '随时随地，想聊就聊' },
      { icon: '🤖', text: '智能回应，贴心陪伴' },
      { icon: '🌙', text: '深夜倾听，温暖守护' }
    ],
    btn: '进入聊天 →',
    path: '/pages/login/index'
  },
  'understand': {
    hint: '想更了解自己的情绪',
    title: '探索情绪背后的秘密',
    subtitle: '通过自我观察和反思<br>发现情绪波动的规律和深层原因',
    description: '情绪不是无缘无故产生的，每一种情绪背后都有其原因和规律。通过探索和分析，你会更了解自己，找到情绪的触发点，从而更好地掌控自己的情绪。',
    image: '/static/images/emotion-exploration.jpg',
    features: [
      { icon: '🔍', text: '深入了解情绪模式' },
      { icon: '💡', text: '发现情绪触发点' },
      { icon: '🚀', text: '基于洞察持续成长' }
    ],
    btn: '开始探索 →',
    path: '/pages/login/index'
  }
}

const dynamicContent = computed(() => dynamicContentMap[selectedNeed.value])

const buttonText = computed(() => {
  if (currentIndex.value < 3) return ''
  if (currentIndex.value === 3) return '继续 →'
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
  background-color: #FFFFFF;
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
  padding-top: 120rpx; 
}

/* 渐变背景的基础配置 */
.hero-gradient {
  position: absolute;
  top: -150rpx;
  left: -50rpx;
  width: 130%;
  height: 800rpx;
  filter: blur(50px);
  z-index: 0;
  opacity: 0.85;
}

/* 每页不同的极光色调，贴合图示 */
.page1-bg {
  background: radial-gradient(circle at 30% 50%, #B4E6DB 0%, transparent 60%),
              radial-gradient(circle at 70% 80%, #FFB6A3 0%, transparent 50%);
}
.page2-bg {
  background: radial-gradient(circle at 20% 40%, #FFF3D6 0%, transparent 50%),
              radial-gradient(circle at 80% 60%, #E6E8FA 0%, transparent 50%);
}
.page3-bg {
  background: radial-gradient(circle at 30% 60%, #E8D6FC 0%, transparent 60%),
              radial-gradient(circle at 70% 30%, #D6E8F6 0%, transparent 50%);
}

/* 插图容器 */
.illustration-container {
  position: relative;
  z-index: 1;
  height: 500rpx;
  margin: 40rpx 60rpx;
  border-radius: 40rpx;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  background: transparent;
}
.illustration-image {
  width: 100%;
  height: 100%;
  border-radius: 40rpx;
  opacity: 0.9;
  filter: saturate(0.9) brightness(1.05);
  transition: all 0.3s ease;
  background: transparent;
  mix-blend-mode: soft-light;
}

/* 插图占位符（保留其他页面使用） */
.illustration-placeholder {
  position: relative;
  z-index: 1;
  height: 500rpx;
  margin: 40rpx 60rpx;
  background-color: rgba(255,255,255,0.4);
  border-radius: 40rpx;
  display: flex;
  justify-content: center;
  align-items: center;
}
.placeholder-text {
  color: #888;
  font-size: 28rpx;
}

/* 底部文案区 */
.text-section {
  position: relative;
  z-index: 1;
  padding: 0 60rpx;
  margin-top: auto;
  margin-bottom: 220rpx; /* 为底部按钮留空间 */
  text-align: center;
}
.title {
  font-size: 58rpx;
  font-weight: 600;
  color: #1A1A1A;
  line-height: 1.3;
  margin-bottom: 32rpx;
  letter-spacing: 2rpx;
}
.subtitle {
  font-size: 34rpx;
  color: #666;
  line-height: 1.7;
  letter-spacing: 1rpx;
}

/* --- 底部统控台 --- */
.bottom-controls {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 200rpx;
  padding: 0 60rpx;
  box-sizing: border-box;
  display: flex;
  justify-content: space-between;
  align-items: center;
  pointer-events: none; /* 让事件穿透到内部按钮 */
}

/* 指示点 */
.dots-container {
  display: flex;
  gap: 12rpx;
}
.dot {
  width: 16rpx;
  height: 16rpx;
  border-radius: 50%;
  background-color: #E5E5EA;
  transition: all 0.3s ease;
}
.dot.active {
  background-color: #FF9B8C;
  width: 36rpx;
  border-radius: 8rpx; /* 拉长变成小胶囊 */
}

/* 操作按钮 */
.action-btn {
  pointer-events: auto; /* 恢复点击 */
  width: 120rpx;
  height: 120rpx;
  border-radius: 50%;
  background: linear-gradient(135deg, #FF9B8C, #FFB0A4);
  box-shadow: 0 10rpx 30rpx rgba(255, 155, 140, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
  transition: all 0.3s ease;
}
.action-btn:active {
  transform: scale(0.95);
}
.arrow {
  font-size: 48rpx;
  font-weight: 300;
}

/* 第4页、第5页变成大药丸长按钮 */
.action-btn.full-width {
  width: 100%;
  border-radius: 99rpx;
  height: 110rpx;
}
.action-btn.full-width .btn-text {
  font-size: 34rpx;
  font-weight: 500;
  letter-spacing: 2rpx;
}

/* 防止最后两页的指示器被满宽按钮遮挡，将满宽按钮定位到下方 */
.bottom-controls:has(.full-width) {
  flex-direction: column;
  justify-content: flex-end;
  padding-bottom: 60rpx;
}
.bottom-controls:has(.full-width) .dots-container {
  display: none; 
}
</style>
