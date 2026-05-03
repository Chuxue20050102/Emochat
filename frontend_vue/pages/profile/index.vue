<template>
  <view class="profile-container">
    <view class="hero-gradient"></view>

    <view class="profile-content">
      <ProfileHeader :nickname="userName" :streakDays="streakDays" @editNickname="handleEditNickname" />
      <AIProfileInsightCard
        :summaryText="aiProfileSummaryText"
        :suggestion="profileSuggestion"
        :overviewItems="profileInsights"
        :statusLabel="aiProfileStatusLabel"
        @chat="chatWithInsight"
      />
      <EmotionCalendar
        :mockRecords="mockRecords"
        :emotionRules="emotionRules"
        @dayClick="handleDayClick"
        @monthChange="handleMonthChange"
      />
      <RecentRecordList
        :records="recentRecords"
        :limit="RECENT_RECORD_LIMIT"
        @detail="goRecentDetail"
        @chat="chatWithRecord"
      />
    </view>

    <view class="ios-padding-bottom"></view>
    <FloatingTabBar currentTab="profile" />
  </view>
</template>

<script setup>
import { computed, ref } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import FloatingTabBar from '@/components/FloatingTabBar.vue'

import {
  getCalendarApi,
  getEmotionHistoryApi,
  getEmotionInsightsApi,
  getUserProfileApi,
  updateNicknameApi,
} from '@/api/index.js'
import { emotionRules as defaultEmotionRules, fetchEmotionConfig } from '@/config/emotionConfig.js'

const emotionRules = ref(defaultEmotionRules)
import AIProfileInsightCard from './components/AIProfileInsightCard.vue'
import EmotionCalendar from './components/EmotionCalendar.vue'
import ProfileHeader from './components/ProfileHeader.vue'
import RecentRecordList from './components/RecentRecordList.vue'

const streakDays = ref(0)
const userName = ref(uni.getStorageSync('nickname') || '用户')
const mockRecords = ref({})
const insightData = ref(null)
const recentRecords = ref([])

const displayedYear = ref(new Date().getFullYear())
const displayedMonth = ref(new Date().getMonth() + 1)

const RECENT_RECORD_LIMIT = 5

onShow(async () => {
  uni.hideTabBar({ animation: false })
  const config = await fetchEmotionConfig()
  emotionRules.value = config.emotionRules
  fetchProfileData()
  fetchCalendarData()
  fetchInsightData()
  fetchRecentRecords()
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
    uni.showToast({ title: '档案信息加载失败', icon: 'none' })
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
      }))
    }
    mockRecords.value = formattedRecords
  } catch (e) {
    uni.showToast({ title: '日历记录加载失败', icon: 'none' })
  }
}

const fetchInsightData = async () => {
  const userId = uni.getStorageSync('user_id')
  if (!userId) return
  try {
    insightData.value = await getEmotionInsightsApi({
      user_id: userId,
      year: displayedYear.value,
      month: displayedMonth.value,
    })
  } catch (e) {
    insightData.value = null
  }
}

const fetchRecentRecords = async () => {
  const userId = uni.getStorageSync('user_id')
  if (!userId) return
  try {
    const res = await getEmotionHistoryApi({
      user_id: userId,
      page: 1,
      page_size: RECENT_RECORD_LIMIT,
    })
    recentRecords.value = Array.isArray(res?.records) ? res.records : []
  } catch (e) {
    recentRecords.value = []
  }
}

const handleDayClick = (day) => {
  if (!day?.fullDate) return
  uni.navigateTo({ url: `/pages/profile/detail?date=${encodeURIComponent(day.fullDate)}` })
}

const handleMonthChange = ({ year, month }) => {
  displayedYear.value = year
  displayedMonth.value = month
  fetchCalendarData()
  fetchInsightData()
}

const goRecentDetail = (record) => {
  const date = record?.record_date || String(record?.created_at || '').slice(0, 10)
  if (!date) return
  const recordQuery = record?.id ? `&record_id=${encodeURIComponent(record.id)}` : ''
  uni.navigateTo({ url: `/pages/profile/detail?date=${encodeURIComponent(date)}${recordQuery}` })
}

const chatWithRecord = (record) => {
  if (!record) return
  const context = {
    emotion: record.mood || '',
    tags: String(record.tags || '')
      .split(',')
      .map((item) => item.trim())
      .filter(Boolean),
    detail: [],
    content: record.description || '',
    recordDate: record.record_date || String(record.created_at || '').slice(0, 10),
  }
  uni.setStorageSync('pendingChatContext', context)
  uni.switchTab({ url: '/pages/chat/index' })
}

const chatWithInsight = () => {
  const summary = insightData.value?.summary || {}
  const labelSafeMap = { '本月记录': '本月写下', '记录天数': '写下天数', '近 7 天': '最近一周' }
  const overviewText = profileInsights.value
    .map((item) => `${labelSafeMap[item.label] || item.label}：${item.value}`)
    .join('，')
  const context = {
    type: 'profile_insight',
    skip_emotion_review: true,
    title: `${displayedMonth.value} 月档案总结`,
    summary: aiProfileSummaryText.value,
    suggestion: profileSuggestion.value,
    overview: overviewText,
    emotion: summary.top_mood || '',
    tags: [summary.top_tag, summary.top_time].filter(Boolean),
    recordDate: `${displayedYear.value}-${String(displayedMonth.value).padStart(2, '0')}`,
  }
  uni.setStorageSync('pendingChatContext', context)
  uni.switchTab({ url: '/pages/chat/index' })
}

const handleEditNickname = () => {
  uni.showModal({
    title: '修改昵称',
    editable: true,
    placeholderText: '请输入1-20个字符',
    content: userName.value || '',
    success: async (res) => {
      if (!res.confirm) return
      const nextNickname = String(res.content || '').trim()
      if (!nextNickname) {
        uni.showToast({ title: '昵称不能为空', icon: 'none' })
        return
      }
      if (nextNickname.length > 20) {
        uni.showToast({ title: '昵称不能超过20个字符', icon: 'none' })
        return
      }

      const userId = uni.getStorageSync('user_id')
      if (!userId) return

      uni.showLoading({ title: '保存中...' })
      try {
        const result = await updateNicknameApi({ user_id: userId, nickname: nextNickname })
        const saved = result?.nickname || nextNickname
        userName.value = saved
        uni.setStorageSync('nickname', saved)
        if (typeof uni.$emit === 'function') {
          uni.$emit('nicknameUpdated', saved)
        }
        uni.showToast({ title: '昵称已更新', icon: 'success' })
      } catch (e) {
        if (e && e.isBizError) return
        uni.showToast({ title: '昵称保存失败', icon: 'none' })
      } finally {
        uni.hideLoading()
      }
    },
  })
}

const profileInsights = computed(() => {
  if (Array.isArray(insightData.value?.insights) && insightData.value.insights.length > 0) {
    return insightData.value.insights.slice(0, 3)
  }

  const currentMonthPrefix = `${displayedYear.value}-${String(displayedMonth.value).padStart(2, '0')}`
  const counts = {}
  const activeDays = new Set()
  let totalRecords = 0

  for (const [dateStr, records] of Object.entries(mockRecords.value)) {
    if (!dateStr.startsWith(currentMonthPrefix)) continue
    activeDays.add(dateStr)
    records.forEach((r) => {
      counts[r.emotionName] = (counts[r.emotionName] || 0) + 1
      totalRecords += 1
    })
  }

  if (totalRecords === 0) {
    return [
      { label: '本月记录', value: '还没有开始' },
      { label: '下一步', value: '先留下今天的一小段感受' },
    ]
  }

  let maxEmotion = '中性'
  let maxCount = 0
  for (const [name, count] of Object.entries(counts)) {
    if (count > maxCount) {
      maxCount = count
      maxEmotion = name
    }
  }

  return [
    { label: '本月记录', value: `${totalRecords} 次` },
    { label: '最常出现', value: maxEmotion },
    { label: '记录天数', value: `${activeDays.size} 天` },
  ]
})

const profileSuggestion = computed(() => insightData.value?.suggestion || '')

const aiProfileSummaryText = computed(() => {
  const text = String(insightData.value?.ai_insight || insightData.value?.trend_text || '').trim()
  if (text) return text
  if (recentRecords.value.length > 0) return '我已经看到你留下一些情绪线索，继续记录后，这里会形成更完整的近况总结。'
  return '记录几次后，我会在这里帮你整理最近的情绪线索，让档案页慢慢长出你的情绪地图。'
})

const aiProfileStatusLabel = computed(() => `${displayedMonth.value} 月档案`)
</script>

<style lang="scss" scoped>
.profile-container {
  min-height: 100vh;
  position: relative;
  padding: 104rpx 28rpx 30rpx;
  box-sizing: border-box;
  overflow: hidden;
  background: $emo-page-bg;
}

.hero-gradient {
  position: absolute;
  inset: -10%;
  z-index: 0;
  filter: blur(72rpx);
  background: $emo-page-glow;
}

.profile-content {
  position: relative;
  z-index: 1;
}

.ios-padding-bottom {
  height: 190rpx;
}
</style>
