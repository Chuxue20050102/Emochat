<template>
  <view class="profile-container">
    <view class="hero-gradient"></view>

    <view class="profile-content">
      <ProfileHeader :nickname="userName" :streakDays="streakDays" />
      <TrendSummary :trendText="currentTrendText" />
      <EmotionCalendar
        :mockRecords="mockRecords"
        :emotionRules="emotionRules"
        :selectedDate="selectedDate"
        @dayClick="handleDayClick"
        @monthChange="handleMonthChange"
      />
    </view>

    <CalendarBottomSheet
      :show="showBottomSheet"
      :dayData="selectedDayData"
      :emotionRules="emotionRules"
      @close="closeBottomSheet"
    />

    <view class="ios-padding-bottom"></view>
    <FloatingTabBar currentTab="profile" />
  </view>
</template>

<script setup>
import { computed, ref } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import FloatingTabBar from '@/components/FloatingTabBar.vue'

import { getCalendarApi, getEmotionDetailApi, getUserProfileApi } from '@/api/index.js'
import { emotionRules } from '@/config/emotionConfig.js'
import CalendarBottomSheet from './components/CalendarBottomSheet.vue'
import EmotionCalendar from './components/EmotionCalendar.vue'
import ProfileHeader from './components/ProfileHeader.vue'
import TrendSummary from './components/TrendSummary.vue'

const streakDays = ref(0)
const userName = ref(uni.getStorageSync('nickname') || '用户')
const mockRecords = ref({})

const selectedDate = ref('')
const selectedDayData = ref(null)
const showBottomSheet = ref(false)

const displayedYear = ref(new Date().getFullYear())
const displayedMonth = ref(new Date().getMonth() + 1)

onShow(() => {
  uni.hideTabBar({ animation: false })
  fetchProfileData()
  fetchCalendarData()
})

const fetchProfileData = async () => {
  const userId = uni.getStorageSync('user_id')
  if (!userId) return
  try {
    const res = await getUserProfileApi({ user_id: userId })
    if (res.nickname) {
      userName.value = res.nickname
      uni.setStorageSync('nickname', res.nickname)
    }
    streakDays.value = res.total_records || 0
  } catch (e) {
    // noop
  }
}

const fetchCalendarData = async () => {
  const userId = uni.getStorageSync('user_id')
  if (!userId) return
  try {
    const res = await getCalendarApi({
      user_id: userId,
      year: displayedYear.value,
      month: displayedMonth.value,
    })

    const formattedRecords = {}
    for (const [dateStr, value] of Object.entries(res || {})) {
      // backward compatible: old format { "2026-04-22": "愉快" }
      // new format: { "2026-04-22": { mood: "愉快", count: 3 } }
      const emotionName = typeof value === 'string' ? value : value?.mood
      const count = Math.max(1, Number(typeof value === 'object' ? value?.count : 1) || 1)
      formattedRecords[dateStr] = Array.from({ length: count }, () => ({
        emotionName: emotionName || '中性',
        emoji: emotionRules[emotionName]?.emoji || '😐',
        content: '',
      }))
    }
    mockRecords.value = formattedRecords
  } catch (e) {
    // noop
  }
}

const handleDayClick = async (day) => {
  selectedDate.value = day.fullDate
  showBottomSheet.value = true
  selectedDayData.value = day

  try {
    const userId = uni.getStorageSync('user_id')
    const details = await getEmotionDetailApi({ user_id: userId, date_str: day.fullDate })
    if (details && details.length > 0) {
      const enrichedRecords = details.map((d) => ({
        emotionName: d.mood,
        emoji: emotionRules[d.mood]?.emoji || '😐',
        content: d.description || '',
        tags: d.tags || '',
      }))
      selectedDayData.value = { ...day, records: enrichedRecords }
    }
  } catch (e) {
    // noop
  }
}

const closeBottomSheet = () => {
  showBottomSheet.value = false
  setTimeout(() => {
    selectedDate.value = ''
  }, 250)
}

const handleMonthChange = ({ year, month }) => {
  displayedYear.value = year
  displayedMonth.value = month
  fetchCalendarData()
}

const currentTrendText = computed(() => {
  const currentMonthPrefix = `${displayedYear.value}-${String(displayedMonth.value).padStart(2, '0')}`
  const counts = {}
  let totalRecords = 0
  for (const [dateStr, records] of Object.entries(mockRecords.value)) {
    if (dateStr.startsWith(currentMonthPrefix)) {
      records.forEach((r) => {
        counts[r.emotionName] = (counts[r.emotionName] || 0) + 1
        totalRecords += 1
      })
    }
  }

  if (totalRecords === 0) return '这个月还没有记录，去写下一条心情吧。'

  let maxEmotion = '中性'
  let maxCount = 0
  for (const [name, count] of Object.entries(counts)) {
    if (count > maxCount) {
      maxCount = count
      maxEmotion = name
    }
  }

  return emotionRules[maxEmotion]?.trend || '你正在慢慢变好。'
})
</script>

<style lang="scss" scoped>
.profile-container {
  min-height: 100vh;
  position: relative;
  padding: 104rpx 28rpx 30rpx;
  box-sizing: border-box;
  overflow: hidden;
}

.hero-gradient {
  position: absolute;
  inset: -10%;
  z-index: 0;
  filter: blur(72rpx);
  background:
    radial-gradient(circle at 14% 18%, rgba(141, 187, 255, 0.28) 0%, transparent 40%),
    radial-gradient(circle at 82% 20%, rgba(255, 179, 163, 0.25) 0%, transparent 38%),
    radial-gradient(circle at 24% 80%, rgba(142, 222, 195, 0.23) 0%, transparent 39%);
}

.profile-content {
  position: relative;
  z-index: 1;
}

.ios-padding-bottom {
  height: 190rpx;
}
</style>
