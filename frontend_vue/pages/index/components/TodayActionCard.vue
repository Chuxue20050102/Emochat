<template>
  <view class="today-action-card">
    <view class="card-copy">
      <text class="title">{{ cardTitle }}</text>
    </view>

    <view class="emotion-grid">
      <button
        v-for="item in emotionList"
        :key="item.name"
        class="emotion-item"
        :class="{ selected: selectedEmotionName === item.name }"
        @click="startRecordWithEmotion(item)"
      >
        <text class="emotion-emoji">{{ item.emoji }}</text>
        <text class="emotion-name">{{ item.name }}</text>
      </button>
    </view>
  </view>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { getEmotionHistoryApi } from '@/api/index'
import { emotionList as defaultEmotionList, fetchEmotionConfig } from '@/config/emotionConfig.js'

const emotionList = ref(defaultEmotionList)

const selectedEmotionName = ref('')
const todayRecordCount = ref(0)
let jumpTimer = null

const cardTitle = computed(() => {
  if (todayRecordCount.value > 0) {
    return '今天已经记录过了，还想补充哪种感觉？'
  }
  return '今天的感觉更接近哪一个？'
})

const getTodayDate = () => {
  const d = new Date()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${d.getFullYear()}-${month}-${day}`
}

const loadTodayStatus = async () => {
  const userId = Number(uni.getStorageSync('user_id') || 0)
  if (!userId) {
    todayRecordCount.value = 0
    return
  }

  try {
    const data = await getEmotionHistoryApi({ user_id: userId, page: 1, page_size: 20 })
    const today = getTodayDate()
    const records = Array.isArray(data?.records) ? data.records : []
    todayRecordCount.value = records.filter((item) => String(item.record_date || '').slice(0, 10) === today).length
  } catch (error) {
    todayRecordCount.value = 0
  }
}

const startRecordWithEmotion = (item) => {
  selectedEmotionName.value = item.name
  uni.setStorageSync('preSelectedEmotion', item.name)
  uni.showToast({
    title: `先选了「${item.name}」`,
    icon: 'none',
    duration: 700,
  })

  if (jumpTimer) {
    clearTimeout(jumpTimer)
  }
  jumpTimer = setTimeout(() => {
    uni.switchTab({ url: '/pages/emotion-record/index' })
  }, 220)
}

onMounted(loadTodayStatus)
onShow(async () => {
  loadTodayStatus()
  const config = await fetchEmotionConfig()
  emotionList.value = config.emotionList
})
</script>

<style lang="scss" scoped>
.today-action-card {
  padding: 28rpx 0 30rpx;
  border-radius: 36rpx;
  background: rgba(255, 255, 255, 0.72);
  border: 2rpx solid rgba(255, 255, 255, 0.9);
  box-shadow: 0 22rpx 60rpx rgba(83, 62, 45, 0.1);
  overflow: hidden;
}

.card-copy {
  padding: 0 28rpx;
}

.title {
  font-size: 34rpx;
  font-weight: 800;
  line-height: 1.35;
  color: $emo-text-main;
}

.emotion-grid {
  margin-top: 22rpx;
  padding: 0 28rpx 2rpx;
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14rpx;
}

.emotion-item {
  min-width: 0;
  height: 132rpx;
  padding: 16rpx 6rpx 14rpx;
  border-radius: 28rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10rpx;
  text-align: center;
  background: linear-gradient(180deg, rgba(255, 253, 249, 0.94), rgba(250, 246, 239, 0.78));
  border: 2rpx solid rgba(255, 255, 255, 0.92);
  box-shadow: 0 14rpx 32rpx rgba(83, 62, 45, 0.08);
  transition: transform 0.16s ease, background 0.16s ease, border-color 0.16s ease;
}

.emotion-item::after {
  border: 0;
}

.emotion-item:active,
.emotion-item.selected {
  transform: scale(0.98);
  background: rgba(237, 250, 243, 0.94);
  border-color: rgba(143, 184, 160, 0.72);
}

.emotion-emoji {
  font-size: 40rpx;
  line-height: 1;
}

.emotion-name {
  font-size: 21rpx;
  font-weight: 700;
  line-height: 1.25;
  color: $emo-text-main;
  white-space: normal;
}
</style>
