<template>
  <view class="record-page" :style="{ background: currentBgColor }">
    <!-- 顶部进度条与导航 (前4步显示) -->
    <view class="header" v-if="currentStep < 5">
      <text class="back-btn" @click="handleBack">{{ currentStep === 1 ? '关闭' : '返回' }}</text>
      <view class="progress-box">
        <text class="step-text">{{ currentStep }} <text class="step-total">/ 4</text></text>
        <view class="progress-bar">
          <view class="progress-inner" :style="{ width: (currentStep / 4) * 100 + '%' }"></view>
        </view>
      </view>
      <text class="placeholder-text"></text>
    </view>

    <!-- 主体滑动卡片区域 -->
    <view class="card-container" v-if="currentStep < 5">
      <swiper class="swiper" :current="currentStep - 1" @change="onSwiperChange" :indicator-dots="false" :autoplay="false">
        
        <!-- Step 1: 心情选择 (感受) -->
        <swiper-item>
          <Step1Mood 
            :emotionList="emotionList" 
            :selectedEmotion="selectedEmotion" 
            @select="selectEmotion" 
          />
        </swiper-item>

        <!-- Step 2: 原因标签 (理解) -->
        <swiper-item>
          <Step2Reason 
            :reasonTags="reasonTags" 
            :selectedReasons="selectedReasons" 
            @toggle="toggleReason" 
          />
        </swiper-item>

        <!-- Step 3: 情绪细化 (命名) -->
        <swiper-item>
          <Step3SubTags 
            :currentSubTags="currentSubTags" 
            :selectedSubTags="selectedSubTags" 
            :selectedEmotion="selectedEmotion"
            @toggle="toggleSubTag" 
          />
        </swiper-item>

        <!-- Step 4: 自由表达 (核心) -->
        <swiper-item>
          <Step4FreeInput v-model="textContent" />
        </swiper-item>
      </swiper>

      <!-- 底部控制按钮区 -->
      <view class="footer-controls">
        <template v-if="currentStep === 4">
          <button class="primary-btn" @click="submitRecord">保存这一刻</button>
        </template>
        <template v-else-if="currentStep > 1">
          <button class="primary-btn" @click="nextStep">下一步</button>
          <text class="skip-btn" @click="nextStep">（小字）跳过</text>
        </template>
      </view>
    </view>

    <!-- Step 5: 完成反馈 (承接页) -->
    <Step5Feedback 
      v-if="currentStep === 5" 
      @goChat="goChatWithContext" 
      @goHome="goToHome" 
    />
    
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

import { recordEmotionApi } from '@/api/index.js'
import { emotionList, reasonTags } from '@/config/emotionConfig.js'

const currentStep = ref(1)
const selectedEmotion = ref(null)
const selectedReasons = ref([])
const selectedSubTags = ref([])
const textContent = ref('')

// emotionList 和 reasonTags 已从 @/config/emotionConfig.js 导入

onShow(() => {
  uni.hideTabBar({ animation: false })

  // 每次进入都重置所有状态，防止上次残留脏数据
  currentStep.value = 1
  selectedEmotion.value = null
  selectedReasons.value = []
  selectedSubTags.value = []
  textContent.value = ''

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
  if (currentStep.value === 5) return 'linear-gradient(to bottom, #FAFCFF, #EBF0FF)' // 承接页略带紫罗兰底色
  if (selectedEmotion.value) return selectedEmotion.value.bgColor
  return '#FAFCFF' // 初始干净浅底色
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
  if (currentStep.value === 5) return
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
  if (currentStep.value < 4) {
    currentStep.value += 1
  }
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
    
    // 成功后流转至 Step 5
    currentStep.value = 5 
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
}

/* 顶部进度导航 */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 120rpx 40rpx 40rpx;
}
.back-btn {
  font-size: 32rpx;
  color: #333;
  width: 80rpx; 
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
  width: 100%;
  height: 100rpx;
  border-radius: 50rpx;
  background: linear-gradient(135deg, #FF9B8C, #FFB0A4);
  color: #FFF;
  font-size: 32rpx;
  font-weight: 600;
  letter-spacing: 2rpx;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 12rpx 30rpx rgba(255, 176, 164, 0.35);
  border: none;
  transition: transform 0.2s ease;
}
.primary-btn::after {
  border: none;
}
.primary-btn:active {
  transform: scale(0.97);
}
.skip-btn {
  font-size: 26rpx;
  color: #BDBDBD;
  padding: 30rpx 20rpx 10rpx;
}
</style>
