<template>
  <view class="record-page" :style="{ background: currentBgColor }">
    <!-- 顶部进度条与导航 (前8步显示) -->
    <view class="header" v-if="currentStep < 9">
      <text class="back-btn" @click="handleBack">{{ currentStep === 1 ? '返回' : '返回' }}</text>
      <view class="progress-box">
        <text class="step-text">{{ currentStep }} <text class="step-total">/ 8</text></text>
        <view class="progress-bar">
          <view class="progress-inner" :style="{ width: (currentStep / 8) * 100 + '%' }"></view>
        </view>
      </view>
      <text class="placeholder-text"></text>
    </view>

    <!-- 主体滑动卡片区域 -->
    <view class="card-container" v-if="currentStep < 9">
      <swiper class="swiper" :current="currentStep - 1" @change="onSwiperChange" :indicator-dots="false" :autoplay="false">
        
        <!-- Step 1: 心情选择 (感受) -->
        <swiper-item>
          <Step1Mood 
            :emotionList="emotionList" 
            :selectedEmotion="selectedEmotion" 
            @select="selectEmotion" 
          />
        </swiper-item>

        <!-- Step 2: 时间选择 -->
        <swiper-item>
          <Step1TimeSelector @select="onTimeSelect" />
        </swiper-item>

        <!-- Step 3: 原因标签 (理解) -->
        <swiper-item>
          <Step2Reason 
            :reasonTags="reasonTags" 
            :selectedReasons="selectedReasons" 
            :selectedEmotion="selectedEmotion"
            @toggle="toggleReason" 
          />
        </swiper-item>

        <!-- Step 4: 情绪细化 (命名) -->
        <swiper-item>
          <Step3SubTags 
            :currentSubTags="currentSubTags" 
            :selectedSubTags="selectedSubTags" 
            :selectedEmotion="selectedEmotion"
            @toggle="toggleSubTag" 
          />
        </swiper-item>

        <!-- Step 5: 情绪强度与环境 -->
        <swiper-item>
          <Step2Intensity @select="onIntensitySelect" />
        </swiper-item>

        <!-- Step 6: 自由表达 (核心) -->
        <swiper-item>
          <Step4FreeInput v-model="textContent" />
        </swiper-item>

        <!-- Step 7: 完成反馈 -->
        <swiper-item>
          <Step5Feedback 
            @goChat="goChatWithContext" 
            @goHome="goToHome" 
          />
        </swiper-item>

        <!-- Step 8: 历史记录预览 -->
        <swiper-item>
          <Step4History />
        </swiper-item>
      </swiper>

      <!-- 底部控制按钮区 -->
      <view class="footer-controls">
        <template v-if="currentStep === 8">
          <button class="primary-btn" @click="submitRecord">保存这一刻</button>
        </template>
        <template v-else-if="currentStep > 1">
          <button class="primary-btn" @click="nextStep">下一步</button>
          <button class="secondary-btn" @click="nextStep">跳过</button>
        </template>
      </view>
    </view>


    
    <FloatingTabBar currentTab="record" />
  </view>
</template>

<script setup>
import { ref, computed } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import FloatingTabBar from '@/components/FloatingTabBar.vue'

// 导入拆分好的私有组件
import Step1Mood from './components/Step1Mood.vue'
import Step2Reason from './components/Step2Reason.vue'
import Step3SubTags from './components/Step3SubTags.vue'
import Step4FreeInput from './components/Step4FreeInput.vue'
import Step5Feedback from './components/Step5Feedback.vue'
import Step1TimeSelector from './components/Step1TimeSelector.vue'
import Step2Intensity from './components/Step2Intensity.vue'
import Step3Environment from './components/Step3Environment.vue'
import Step4History from './components/Step4History.vue'

import { recordEmotionApi } from '@/api/index.js'
import { emotionList, reasonTags } from '@/config/emotionConfig.js'

const currentStep = ref(1)
const selectedEmotion = ref(null)
const selectedReasons = ref([])
const selectedSubTags = ref([])
const textContent = ref('')
const selectedTime = ref({ date: 'today', time: 'morning' })
const intensity = ref(5)
const weather = ref('')
const environment = ref('')

// emotionList 和 reasonTags 已从 @/config/emotionConfig.js 导入

onShow(() => {
  uni.hideTabBar({ animation: false })

  // 每次进入都重置所有状态，防止上次残留脏数据
  currentStep.value = 1
  selectedEmotion.value = null
  selectedReasons.value = []
  selectedSubTags.value = []
  textContent.value = ''
  selectedTime.value = { date: 'today', time: 'morning' }
  intensity.value = 5
  weather.value = ''
  environment.value = ''

  // 检查是否从首页模块2带着预选情绪过来
  const preSelected = uni.getStorageSync('preSelectedEmotion')
  if (preSelected) {
    uni.removeStorageSync('preSelectedEmotion') // 用完即删
    const match = emotionList.find(e => e.name === preSelected)
    if (match) {
      selectedEmotion.value = match
      // 自动跳到第2步（原因标签页）
      setTimeout(() => {
        currentStep.value = 2
      }, 300)
    }
  }
})

const currentBgColor = computed(() => {
  if (currentStep.value === 7) return '#F5F5DC' // 承接页使用米白色
  if (selectedEmotion.value) return selectedEmotion.value.bgColor
  return '#F5F5DC' // 初始使用米白色
})

const currentSubTags = computed(() => {
  return selectedEmotion.value ? selectedEmotion.value.subTags : []
})

const selectEmotion = (item) => {
  selectedEmotion.value = item
  // 清零后面的自选项，防止脏数据
  selectedSubTags.value = []
  setTimeout(() => {
    nextStep()
  }, 400)
}

const toggleReason = (tag) => {
  const index = selectedReasons.value.indexOf(tag)
  if (index > -1) {
    selectedReasons.value.splice(index, 1)
  } else {
    selectedReasons.value.push(tag)
  }
}

const toggleSubTag = (tag) => {
  const index = selectedSubTags.value.indexOf(tag)
  if (index > -1) {
    selectedSubTags.value.splice(index, 1)
  } else {
    selectedSubTags.value.push(tag)
  }
}

const onSwiperChange = (e) => {
  currentStep.value = e.detail.current + 1
}

const handleBack = () => {
  // 如果不小心切到了最后一步则不让回退卡片布局
  if (currentStep.value === 9) return
  if (currentStep.value > 1) {
    currentStep.value -= 1
  } else {
    uni.switchTab({ url: '/pages/index/index' })
  }
}

const nextStep = () => {
  if (currentStep.value === 1 && !selectedEmotion.value) {
    uni.showToast({ title: '请先选择一种感受', icon: 'none' })
    return
  }
  if (currentStep.value < 8) {
    currentStep.value += 1
  }
}

const onTimeSelect = (timeData) => {
  selectedTime.value = timeData
}

const onIntensitySelect = (data) => {
  intensity.value = data.intensity
  weather.value = data.weather
  environment.value = ''
}

const submitRecord = async () => {
  uni.showLoading({ title: '记录中...' })
  try {
    const userId = uni.getStorageSync('user_id')
    if (!userId) {
      uni.showToast({ title: '请先登录', icon: 'none' })
      return
    }

    const payload = {
      user_id: userId,
      mood: selectedEmotion.value.name,
      tags: [...selectedReasons.value, ...selectedSubTags.value].join(','),
      description: textContent.value
    }

    await recordEmotionApi(payload)
    
    // 成功后流转至 Step 7
    currentStep.value = 7 
  } catch(e) {
    uni.showToast({ title: '保存失败，请检查网络或后端是否启动', icon: 'none' })
  } finally {
    uni.hideLoading()
  }
}

const goChatWithContext = () => {
  const recordData = {
    emotion: selectedEmotion.value?.name || '',
    tags: selectedReasons.value,
    detail: selectedSubTags.value,
    content: textContent.value
  }
  uni.setStorageSync('pendingChatContext', recordData)
  uni.switchTab({ url: '/pages/chat/index' })
}

const goToHome = () => {
  uni.switchTab({ url: '/pages/index/index' })
}
</script>

<style lang="scss" scoped>
.record-page {
  height: 100vh;
  transition: background 0.5s ease;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  background-color: #F5F5DC;
  font-family: 'SimSun', serif;
  color: #6B5B47;
  font-weight: 500;
  font-size: 28rpx;
}

/* 顶部进度导航 */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 120rpx 40rpx 40rpx;
}
.back-btn {
  font-size: 30rpx;
  color: #6B5B47;
  width: 120rpx;
  height: 64rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(245, 245, 220, 0.9));
  border-radius: 32rpx;
  border: 2rpx solid rgba(107, 91, 71, 0.3);
  box-shadow: 0 4rpx 12rpx rgba(107, 91, 71, 0.15);
  transition: all 0.3s ease;
  font-weight: 600;
}
.back-btn:hover {
  background: linear-gradient(135deg, #98D8C8, #74C7B8);
  color: #FFF;
  box-shadow: 0 6rpx 16rpx rgba(120, 200, 180, 0.3);
  transform: translateY(-3rpx) scale(1.02);
}
.placeholder-text {
  width: 80rpx;
}
.progress-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12rpx;
}
.step-text {
  font-size: 32rpx;
  font-weight: 500;
  color: #1A1A1A;
}
.step-total {
  color: #999;
  font-size: 28rpx;
  margin-left: 4rpx;
}
.progress-bar {
  width: 160rpx;
  height: 8rpx;
  background-color: rgba(0,0,0,0.06);
  border-radius: 4rpx;
  overflow: hidden;
}
.progress-inner {
  height: 100%;
  background: linear-gradient(90deg, #FF9B8C, #FFB0A4);
  border-radius: 4rpx;
  transition: width 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

/* 主容器 */
.card-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding-top: 40rpx;
  overflow: hidden;
}
.swiper {
  flex: 1;
  height: 100%;
  min-height: 600rpx;
}

/* 底部操作区控制 */
.footer-controls {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20rpx 60rpx 180rpx; /* safe area for tabbar */
  background: transparent;
}
.primary-btn {
  width: 80%;
  height: 90rpx;
  border-radius: 45rpx;
  background: linear-gradient(135deg, #98D8C8, #74C7B8);
  color: #FFF;
  font-size: 32rpx;
  font-weight: 600;
  letter-spacing: 2rpx;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 8rpx 20rpx rgba(120, 200, 180, 0.25);
  border: none;
  transition: all 0.3s ease;
  margin: 0 auto;
}
.primary-btn::after {
  border: none;
}
.primary-btn:hover {
  background: linear-gradient(135deg, #85C7B7, #61B6A6);
  box-shadow: 0 10rpx 24rpx rgba(120, 200, 180, 0.35);
  transform: translateY(-2rpx);
}
.primary-btn:active {
  transform: scale(0.97);
}
.skip-btn {
  font-size: 28rpx;
  color: #6B5B47;
  padding: 30rpx 20rpx 10rpx;
  transition: all 0.3s ease;
  font-weight: 500;
}
.skip-btn:hover {
  color: #5A4A37;
  transform: translateY(-2rpx);
}

.secondary-btn {
  width: 80%;
  height: 90rpx;
  border-radius: 45rpx;
  background: #F5F5DC;
  color: #6B5B47;
  font-size: 32rpx;
  font-weight: 600;
  letter-spacing: 2rpx;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 8rpx 20rpx rgba(107, 91, 71, 0.15);
  border: 2rpx solid rgba(107, 91, 71, 0.3);
  transition: all 0.3s ease;
  margin: 20rpx auto 0;
}
.secondary-btn::after {
  border: none;
}
.secondary-btn:hover {
  background: #C8E6D8;
  box-shadow: 0 10rpx 24rpx rgba(120, 200, 180, 0.25);
  transform: translateY(-2rpx);
}
.secondary-btn:active {
  transform: scale(0.97);
}
</style>
