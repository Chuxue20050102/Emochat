<template>
  <view class="record-page" :style="{ background: currentBgColor }">
    <view class="hero-gradient"></view>

    <view class="header">
      <text class="back-btn" @click="handleBack">返回</text>
      <view class="progress-box">
        <text class="step-text">{{ currentStep }} <text class="step-total">/ 5</text></text>
        <view class="progress-bar">
          <view class="progress-inner" :style="{ width: `${(currentStep / 5) * 100}%` }"></view>
        </view>
      </view>
      <text class="placeholder-text"></text>
    </view>

    <view class="content-wrap">
      <scroll-view class="step-stage" scroll-y="true" :show-scrollbar="false">
        <Step1Mood
          v-if="currentStep === 1"
          :emotionList="emotionList"
          :selectedEmotion="selectedEmotion"
          @select="selectEmotion"
        />

        <Step2Reason
          v-else-if="currentStep === 2"
          :reasonTags="allReasonTags"
          :selectedReasons="selectedReasons"
          @toggle="toggleReason"
          @add-custom="addCustomReason"
        />

        <Step3SubTags
          v-else-if="currentStep === 3"
          :currentSubTags="currentSubTags"
          :selectedSubTags="selectedSubTags"
          :selectedEmotion="selectedEmotion"
          @toggle="toggleSubTag"
        />

        <Step4FreeInput
          v-else-if="currentStep === 4"
          v-model="textContent"
          :bottomOffset="stepInputOffset"
          :cursorSpacing="Math.max(keyboardHeight, 120)"
          @focus="handleTextFocus"
          @blur="handleTextBlur"
        />

        <Step5Feedback
          v-else
          :summaryMood="selectedEmotion?.name"
          :summaryReasons="selectedReasons.join('、')"
          :summarySubTags="selectedSubTags.join('、')"
          :saving="saving"
          @save-and-chat="handleSaveAndChat"
          @save-and-home="handleSaveAndHome"
          @back="goPrevStep"
        />
      </scroll-view>

      <view v-if="shouldShowFooter" class="footer-controls" :style="footerStyle">
        <button class="emo-btn-primary full-btn" @click="nextStep">下一步</button>
        <button class="emo-btn-ghost full-btn ghost-btn" @click="skipStep">跳过</button>
      </view>
    </view>
  </view>
</template>

<script setup>
import { computed, onBeforeUnmount, ref } from 'vue'
import { onHide, onShow } from '@dcloudio/uni-app'

import { recordEmotionApi } from '@/api/index.js'
import { emotionList, reasonTags } from '@/config/emotionConfig.js'
import Step1Mood from './components/Step1Mood.vue'
import Step2Reason from './components/Step2Reason.vue'
import Step3SubTags from './components/Step3SubTags.vue'
import Step4FreeInput from './components/Step4FreeInput.vue'
import Step5Feedback from './components/Step5Feedback.vue'

const currentStep = ref(1)
const selectedEmotion = ref(null)
const selectedReasons = ref([])
const selectedSubTags = ref([])
const customReasonTags = ref([])
const textContent = ref('')
const keyboardHeight = ref(0)
const saving = ref(false)
const isTextInputFocused = ref(false)
let keyboardHeightHandler = null

onShow(() => {
  uni.hideTabBar({ animation: false })
  bindKeyboardHeightChange()
  resetForm()

  const preSelected = uni.getStorageSync('preSelectedEmotion')
  if (!preSelected) return

  uni.removeStorageSync('preSelectedEmotion')
  const match = emotionList.find((item) => item.name === preSelected)
  if (!match) return

  selectedEmotion.value = match
  currentStep.value = 2
})

onHide(() => {
  resetKeyboardState()
})

onBeforeUnmount(() => {
  unbindKeyboardHeightChange()
})

const allReasonTags = computed(() => [...reasonTags, ...customReasonTags.value])
const currentBgColor = computed(() => selectedEmotion.value?.bgColor || 'linear-gradient(180deg, #f8fbff 0%, #f3f6fd 100%)')
const currentSubTags = computed(() => selectedEmotion.value?.subTags || [])
const stepInputOffset = computed(() => (currentStep.value === 4 ? keyboardHeight.value : 0))
const shouldShowFooter = computed(
  () => currentStep.value < 5 && !(currentStep.value === 4 && (isTextInputFocused.value || keyboardHeight.value > 0))
)
const footerStyle = computed(() => ({
  paddingBottom:
    currentStep.value === 4
      ? `${Math.max(24, keyboardHeight.value + 20)}px`
      : 'calc(env(safe-area-inset-bottom) + 24rpx)',
}))

const resetForm = () => {
  currentStep.value = 1
  selectedEmotion.value = null
  selectedReasons.value = []
  selectedSubTags.value = []
  customReasonTags.value = []
  textContent.value = ''
  saving.value = false
}

const selectEmotion = (item) => {
  selectedEmotion.value = item
  selectedSubTags.value = []
}

const toggleReason = (tag) => {
  const index = selectedReasons.value.indexOf(tag)
  if (index > -1) {
    selectedReasons.value.splice(index, 1)
  } else {
    selectedReasons.value.push(tag)
  }
}

const addCustomReason = (tag) => {
  const value = String(tag || '').trim()
  if (!value) return

  if (!customReasonTags.value.includes(value)) {
    customReasonTags.value.push(value)
  }
  if (!selectedReasons.value.includes(value)) {
    selectedReasons.value.push(value)
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

const handleBack = () => {
  if (currentStep.value > 1) {
    currentStep.value -= 1
    return
  }
  uni.switchTab({ url: '/pages/index/index' })
}

const goPrevStep = () => {
  if (currentStep.value > 1) currentStep.value -= 1
}

const nextStep = () => {
  if (currentStep.value === 1 && !selectedEmotion.value) {
    uni.showToast({ title: '请先选择一个心情', icon: 'none' })
    return
  }
  if (currentStep.value < 5) {
    currentStep.value += 1
  }
}

const skipStep = () => {
  if (currentStep.value === 1) {
    uni.showToast({ title: '第一步不能跳过', icon: 'none' })
    return
  }
  if (currentStep.value < 5) {
    currentStep.value += 1
  }
}

const toLocalDate = () => {
  const d = new Date()
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}-${m}-${day}`
}

const saveRecord = async () => {
  if (saving.value) return false

  const userId = uni.getStorageSync('user_id')
  if (!userId) {
    uni.showToast({ title: '请先登录', icon: 'none' })
    return false
  }

  saving.value = true
  uni.showLoading({ title: '保存中...' })

  try {
    const payload = {
      user_id: userId,
      mood: selectedEmotion.value?.name || '中性',
      tags: [...selectedReasons.value, ...selectedSubTags.value].join(','),
      description: textContent.value || '',
      record_date: toLocalDate(),
    }

    await recordEmotionApi(payload)
    return true
  } catch (error) {
    uni.showToast({ title: '保存失败，请稍后再试', icon: 'none' })
    return false
  } finally {
    uni.hideLoading()
    saving.value = false
  }
}

const handleSaveAndChat = async () => {
  const ok = await saveRecord()
  if (!ok) return

  const recordData = {
    emotion: selectedEmotion.value?.name || '',
    tags: selectedReasons.value,
    detail: selectedSubTags.value,
    content: textContent.value,
    recordDate: toLocalDate(),
  }

  uni.setStorageSync('pendingChatContext', recordData)
  uni.showToast({ title: '已保存，正在跳转 AI', icon: 'none' })
  uni.switchTab({ url: '/pages/chat/index' })
}

const handleSaveAndHome = async () => {
  const ok = await saveRecord()
  if (!ok) return

  uni.showToast({ title: '记录已保存', icon: 'none' })
  uni.switchTab({ url: '/pages/index/index' })
}

const handleTextFocus = () => {
  isTextInputFocused.value = true
}

const handleTextBlur = () => {
  isTextInputFocused.value = false
}

const bindKeyboardHeightChange = () => {
  if (typeof uni.onKeyboardHeightChange !== 'function' || keyboardHeightHandler) return

  keyboardHeightHandler = ({ height = 0 }) => {
    keyboardHeight.value = height
  }

  uni.onKeyboardHeightChange(keyboardHeightHandler)
}

const unbindKeyboardHeightChange = () => {
  if (typeof uni.offKeyboardHeightChange === 'function' && keyboardHeightHandler) {
    uni.offKeyboardHeightChange(keyboardHeightHandler)
  }
  keyboardHeightHandler = null
}

const resetKeyboardState = () => {
  keyboardHeight.value = 0
  isTextInputFocused.value = false
}
</script>

<style lang="scss" scoped>
.record-page {
  height: 100vh;
  position: relative;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.hero-gradient {
  position: absolute;
  inset: -10%;
  z-index: 0;
  filter: blur(70rpx);
  background:
    radial-gradient(circle at 14% 20%, rgba(141, 187, 255, 0.22) 0%, transparent 36%),
    radial-gradient(circle at 82% 22%, rgba(255, 174, 161, 0.23) 0%, transparent 34%),
    radial-gradient(circle at 25% 84%, rgba(142, 222, 195, 0.2) 0%, transparent 34%);
}

.header {
  position: relative;
  z-index: 2;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 104rpx 24rpx 14rpx;
}

.back-btn {
  width: 96rpx;
  height: 58rpx;
  border-radius: 999rpx;
  background: rgba(255, 255, 255, 0.66);
  border: 2rpx solid rgba(255, 255, 255, 0.88);
  color: #5f6b86;
  font-size: 24rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.placeholder-text {
  width: 96rpx;
}

.progress-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8rpx;
}

.step-text {
  font-size: 30rpx;
  font-weight: 700;
  color: #24304e;
}

.step-total {
  color: #8f99b1;
  font-size: 24rpx;
}

.progress-bar {
  width: 170rpx;
  height: 8rpx;
  border-radius: 999rpx;
  background: rgba(136, 149, 176, 0.22);
}

.progress-inner {
  height: 100%;
  border-radius: 999rpx;
  background: linear-gradient(90deg, #8eb9ff, #82d9bb);
}

.content-wrap {
  position: relative;
  z-index: 2;
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
}

.step-stage {
  flex: 1;
  min-height: 0;
}

.footer-controls {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12rpx;
  padding: 8rpx 30rpx calc(env(safe-area-inset-bottom) + 24rpx);
  background: linear-gradient(180deg, rgba(255, 255, 255, 0), rgba(255, 255, 255, 0.22) 42%, rgba(255, 255, 255, 0.4) 100%);
}

.full-btn {
  width: 100%;
}

.ghost-btn {
  color: #607290;
}
</style>
