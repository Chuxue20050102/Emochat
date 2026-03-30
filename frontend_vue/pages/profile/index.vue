<template>
  <view class="profile-container">
    <ProfileHeader :nickname="userName" :streakDays="streakDays" />
    <TrendSummary :trendText="currentTrendText" />
    <EmotionCalendar 
      :mockRecords="mockRecords" 
      :emotionRules="emotionRules" 
      :selectedDate="selectedDate"
      @dayClick="handleDayClick" 
      @monthChange="handleMonthChange" 
    />
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
import { ref, computed, onMounted } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import FloatingTabBar from '@/components/FloatingTabBar.vue'

import ProfileHeader from './components/ProfileHeader.vue'
import TrendSummary from './components/TrendSummary.vue'
import EmotionCalendar from './components/EmotionCalendar.vue'
import CalendarBottomSheet from './components/CalendarBottomSheet.vue'

import { getUserProfileApi, getCalendarApi, getEmotionDetailApi } from '@/api/index.js'

onShow(() => { 
  uni.hideTabBar({ animation: false })
  fetchProfileData()
  fetchCalendarData()
})

const streakDays = ref(0)
const userName = ref(uni.getStorageSync('nickname') || '用户')
const mockRecords = ref({})

const fetchProfileData = async () => {
  const userId = uni.getStorageSync('user_id')
  if (!userId) return
  try {
    const res = await getUserProfileApi({ user_id: userId })
    if (res.nickname) {
      userName.value = res.nickname
      uni.setStorageSync('nickname', res.nickname)
    }
    streakDays.value = res.total_records || 0 // 用总条数勉强替代连续天数
  } catch(e) {}
}

const fetchCalendarData = async () => {
  const userId = uni.getStorageSync('user_id')
  if (!userId) return
  try {
    const res = await getCalendarApi({ 
      user_id: userId,
      year: displayedYear.value,
      month: displayedMonth.value
    })
    
    // 把后端的 {"2026-03-10": "崩溃"} 转成我们需要的数据结构
    const formattedRecords = {}
    for (const [dateStr, emotionName] of Object.entries(res)) {
      formattedRecords[dateStr] = [
        { emotionName, emoji: emotionRules[emotionName]?.emoji || '😐', content: '' }
      ]
    }
    mockRecords.value = formattedRecords
  } catch(e) {}
}

const emotionRules = {
  '崩溃': { color: '#3A0CA3', emoji: '😣', trend: '这个月，你有些辛苦' },
  '迷茫': { color: '#4361EE', emoji: '😕', trend: '最近有点低落' },
  '低落': { color: '#4895EF', emoji: '🙁', trend: '最近有点低落' },
  '平静': { color: '#4CC9A6', emoji: '😐', trend: '大多数时候是平静的 🌿' },
  '轻松': { color: '#52B788', emoji: '🙂', trend: '你在慢慢恢复' },
  '愉快': { color: '#FFD60A', emoji: '😊', trend: '这个月有不少温暖时刻' },
  '极好': { color: '#FB8500', emoji: '😄', trend: '这个月充满能量 ✨' }
}

const selectedDate = ref('')
const selectedDayData = ref(null)
const showBottomSheet = ref(false)

const handleDayClick = async (day) => {
  selectedDate.value = day.fullDate
  showBottomSheet.value = true
  // 先用日历里已有的基础数据展示，再去后端拉取详情覆盖
  selectedDayData.value = day

  try {
    const userId = uni.getStorageSync('user_id')
    const details = await getEmotionDetailApi({ user_id: userId, date_str: day.fullDate })
    if (details && details.length > 0) {
      // 把详情数据中的 description、tags 合并进去
      const enrichedRecords = details.map(d => ({
        emotionName: d.mood,
        emoji: emotionRules[d.mood]?.emoji || '😐',
        content: d.description || '',
        tags: d.tags || ''
      }))
      selectedDayData.value = { ...day, records: enrichedRecords }
    }
  } catch(e) {
    // 详情加载失败时继续显示基础数据
  }
}

const closeBottomSheet = () => {
  showBottomSheet.value = false
  setTimeout(() => { selectedDate.value = '' }, 300)
}

// 模拟状态，保存子组件选定的月份来算 Trend
const displayedYear = ref(new Date().getFullYear())
const displayedMonth = ref(new Date().getMonth() + 1)

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
      records.forEach(r => {
        counts[r.emotionName] = (counts[r.emotionName] || 0) + 1
        totalRecords++
      })
    }
  }
  if (totalRecords === 0) return '这个月还没有记录哦，去写点什么吧 🌱'
  let maxEmotion = '平静'
  let maxCount = 0
  for (const [name, count] of Object.entries(counts)) {
    if (count > maxCount) {
      maxCount = count
      maxEmotion = name
    }
  }
  return emotionRules[maxEmotion]?.trend || '大多数时候是平静的 🌿'
})
</script>

<style lang="scss" scoped>
.profile-container {
  min-height: 100vh;
  background-color: #FAFCFF;
  padding: 120rpx 40rpx 40rpx;
  box-sizing: border-box;
}
.ios-padding-bottom {
  height: 200rpx;
}
</style>
