<template>
  <view class="guide-container">
    <swiper class="swiper" :current="currentIndex" @change="onSwiperChange" :indicator-dots="false" :autoplay="false">
      <!-- 第1页: 情绪共鸣 -->
      <swiper-item>
        <view class="page-content">
          <view class="hero-gradient page1-bg"></view>
          <view class="illustration-placeholder">
            <view class="placeholder-text">一个人坐着思考 / 夜晚窗边</view>
          </view>
          <view class="text-section">
            <view class="title">有时候<br>情绪很难表达</view>
            <view class="subtitle">忙碌的生活中<br>很多感受来不及被认真看见</view>
          </view>
        </view>
      </swiper-item>

      <!-- 第2页: 解决方式 -->
      <swiper-item>
        <view class="page-content">
          <view class="hero-gradient page2-bg"></view>
          <view class="illustration-placeholder">
            <view class="placeholder-text">日记本 / 情绪记录</view>
          </view>
          <view class="text-section">
            <view class="title">记录<br>可以帮助整理情绪</view>
            <view class="subtitle">把每天的感受记录下来<br>慢慢看见自己的变化</view>
          </view>
        </view>
      </swiper-item>

      <!-- 第3页: 产品能力 -->
      <swiper-item>
        <view class="page-content">
          <view class="hero-gradient page3-bg"></view>
          <view class="illustration-placeholder">
            <view class="placeholder-text">聊天气泡 / 温暖的AI形象</view>
          </view>
          <view class="text-section">
            <view class="title">当你想要倾听时<br>AI 可以陪你聊一聊</view>
            <view class="subtitle">表达想法<br>也许会让心情轻松一点</view>
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
    title: '开始记录你的情绪',
    subtitle: '把今天的感受简单记录下来<br>慢慢看见自己的情绪变化',
    illus: '插图: 在爱心板上写字',
    btn: '开始记录 →',
    path: '/pages/login/index'
  },
  'chat': {
    hint: '想找个地方聊聊天',
    title: '找个地方聊聊天',
    subtitle: '如果有想说的话<br>可以和 AI 慢慢聊一聊',
    illus: '插图: 和小幽灵聊天喝咖啡',
    btn: '进入聊天 →',
    path: '/pages/login/index'
  },
  'understand': {
    hint: '想更了解自己的情绪',
    title: '慢慢了解自己的情绪',
    subtitle: '通过记录和回顾<br>慢慢发现自己的情绪变化',
    illus: '插图: 看情绪折线趋势图',
    btn: '开始体验 →',
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

/* 插图占位符 */
.illustration-placeholder {
  position: relative;
  z-index: 1;
  height: 500rpx;
  margin: 40rpx 60rpx;
  background-color: rgba(255,255,255,0.4);
  border: 2rpx dashed #C7C7CC;
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
  font-size: 52rpx;
  font-weight: 600;
  color: #1A1A1A;
  line-height: 1.4;
  margin-bottom: 24rpx;
}
.subtitle {
  font-size: 30rpx;
  color: #666;
  line-height: 1.6;
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
