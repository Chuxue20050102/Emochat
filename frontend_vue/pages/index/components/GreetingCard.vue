<template>
  <view class="greeting-card emo-fade-up">
    <view class="warm-header">
      <view class="warm-mark"></view>
      <view class="title-stack">
        <text v-if="nameLabel" class="name-label">{{ nameLabel }}</text>
        <text class="hello">{{ title }}</text>
      </view>
    </view>
    <text class="affirmation">{{ affirmation }}</text>

    <view class="status-row">
      <text class="summary">{{ todaySummary }}</text>
      <text v-if="insightSummary" class="insight-chip">{{ insightSummary }}</text>
      <text v-if="intentHint" class="intent-hint">{{ intentHint }}</text>
    </view>
  </view>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { getEmotionHistoryApi, getEmotionInsightsApi, getGreetingApi, getHomeCopyApi } from '@/api/index'

const ONBOARDING_INTENT_KEY = 'onboarding_intent'

const userName = ref('')
const records = ref([])
const totalRecords = ref(0)
const onboardingIntent = ref('')
const greetingText = ref('')
const homeCopy = ref({})
const insightData = ref(null)

const cleanName = computed(() => {
  const name = String(userName.value || '').trim()
  if (!name || /^新用户\d*$/.test(name)) return ''
  return name
})
const displayName = computed(() => cleanName.value || '你')

const title = computed(() => {
  const key = getOpeningKey()
  const template = homeCopy.value[key] || homeCopy.value.opening_default || '{nickname}，今天也慢慢来'
  const text = formatCopy(template, {
    nickname: displayName.value,
  })
  if (!cleanName.value) return text
  return text.replace(new RegExp(`^${escapeRegExp(displayName.value)}[，,\\s]*`), '')
})
const nameLabel = computed(() => (cleanName.value ? `${cleanName.value}，` : ''))
const affirmation = computed(() => greetingText.value || '你不需要一下子变好，愿意靠近自己已经很重要。')
const todayRecordCount = computed(() => {
  const today = getTodayDate()
  return records.value.filter((item) => String(item.record_date || '').slice(0, 10) === today).length
})
const monthRecordCount = computed(() => Number(insightData.value?.summary?.total_records || 0))
const todaySummary = computed(() => {
  if (todayRecordCount.value > 0) {
    return formatCopy(homeCopy.value.status_today || '今天已经留下 {count} 次心情', {
      count: todayRecordCount.value,
    })
  }
  if (totalRecords.value > 0) {
    return formatCopy(homeCopy.value.status_total || '已经留下 {count} 条线索', {
      count: totalRecords.value,
    })
  }
  return homeCopy.value.status_empty || '今天还没有留下心情'
})
const insightSummary = computed(() => {
  if (monthRecordCount.value > 0) {
    const topMood = insightData.value?.summary?.top_mood || ''
    return topMood ? `本月常见：${topMood}` : `本月 ${monthRecordCount.value} 次记录`
  }
  if (totalRecords.value > 0) return '这个月还可以继续补一点'
  return ''
})
const intentHint = computed(() => {
  if (totalRecords.value > 0) return ''
  const map = {
    record: homeCopy.value.hint_newbie_record || '可以先选一个情绪',
    chat: homeCopy.value.hint_newbie_chat || '想直接聊聊也可以',
    profile: homeCopy.value.hint_newbie_profile || '记录几次后就能回看状态',
  }
  return map[onboardingIntent.value] || ''
})

const getOpeningKey = () => {
  if (todayRecordCount.value > 0) return 'opening_recorded_today'
  if (totalRecords.value > 0) return 'opening_returning'
  if (!cleanName.value) return 'opening_guest'
  return 'opening_newbie'
}

const getTodayDate = () => {
  const d = new Date()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${d.getFullYear()}-${month}-${day}`
}

const getMonthParams = () => {
  const d = new Date()
  return {
    year: d.getFullYear(),
    month: d.getMonth() + 1,
  }
}

const formatCopy = (template, params = {}) =>
  String(template || '').replace(/\{(\w+)\}/g, (_, key) => {
    const value = params[key]
    return value === undefined || value === null ? '' : String(value)
  })

const escapeRegExp = (value) => String(value).replace(/[.*+?^${}()|[\]\\]/g, '\\$&')

const safeRequest = async (request) => {
  try {
    return await request()
  } catch (error) {
    return null
  }
}

const loadGreeting = async () => {
  const userId = Number(uni.getStorageSync('user_id') || 0)
  if (!userId) {
    records.value = []
    totalRecords.value = 0
    insightData.value = null
  }

  try {
    const [history, greeting, copy, insights] = await Promise.all([
      userId ? safeRequest(() => getEmotionHistoryApi({ user_id: userId, page: 1, page_size: 20 })) : Promise.resolve(null),
      safeRequest(() => getGreetingApi()),
      safeRequest(() => getHomeCopyApi({ module: 'home_card1', state: 'default' })),
      userId ? safeRequest(() => getEmotionInsightsApi({ user_id: userId, ...getMonthParams() })) : Promise.resolve(null),
    ])
    records.value = Array.isArray(history?.records) ? history.records : []
    totalRecords.value = Number(history?.total || records.value.length || 0)
    greetingText.value = String(greeting?.content || '').trim()
    homeCopy.value = copy && typeof copy === 'object' ? copy : {}
    insightData.value = insights
  } catch (error) {
    records.value = []
    totalRecords.value = 0
    insightData.value = null
  }
}

const refreshLocalState = () => {
  userName.value = String(uni.getStorageSync('nickname') || '').trim()
  onboardingIntent.value = String(uni.getStorageSync(ONBOARDING_INTENT_KEY) || '').trim()
}

const handleNicknameUpdated = (nextNickname) => {
  userName.value = String(nextNickname || '').trim()
}

onMounted(async () => {
  refreshLocalState()
  await loadGreeting()
  if (typeof uni.$on === 'function') {
    uni.$on('nicknameUpdated', handleNicknameUpdated)
  }
})

onShow(() => {
  refreshLocalState()
  loadGreeting()
})

onBeforeUnmount(() => {
  if (typeof uni.$off === 'function') {
    uni.$off('nicknameUpdated', handleNicknameUpdated)
  }
})
</script>

<style lang="scss" scoped>
.greeting-card {
  position: relative;
  overflow: hidden;
  padding: 34rpx 32rpx 30rpx;
  border-radius: 30rpx;
  background:
    linear-gradient(145deg, rgba(255, 255, 255, 0.92) 0%, rgba(255, 249, 242, 0.86) 58%, rgba(247, 254, 250, 0.78) 100%);
  border: 1rpx solid rgba(255, 255, 255, 0.9);
  box-shadow: 0 18rpx 48rpx rgba(83, 62, 45, 0.09);
}

.warm-header {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: flex-start;
  gap: 14rpx;
}

.warm-mark {
  width: 8rpx;
  height: 76rpx;
  margin-top: 3rpx;
  flex: 0 0 8rpx;
  border-radius: 999rpx;
  background: linear-gradient(180deg, #d9a27f 0%, #8fb8a0 100%);
  opacity: 0.72;
}

.hello {
  display: block;
  font-size: 34rpx;
  line-height: 1.32;
  color: $emo-text-main;
  font-weight: 800;
}

.title-stack {
  min-width: 0;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4rpx;
}

.name-label {
  display: block;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 22rpx;
  line-height: 1.25;
  color: #8a766a;
  font-weight: 700;
}

.affirmation {
  position: relative;
  z-index: 1;
  margin-top: 16rpx;
  display: block;
  font-size: 24rpx;
  line-height: 1.55;
  color: $emo-text-sub;
}

.status-row {
  position: relative;
  z-index: 1;
  margin-top: 16rpx;
  padding-top: 14rpx;
  display: flex;
  flex-wrap: wrap;
  gap: 8rpx 14rpx;
  border-top: 1rpx solid rgba(140, 112, 92, 0.1);
}

.summary,
.insight-chip,
.intent-hint {
  display: inline-flex;
  width: fit-content;
  padding: 0;
  border-radius: 0;
  font-size: 21rpx;
  line-height: 1.35;
  box-shadow: none;
}

.summary {
  color: $emo-sage-text;
  background: transparent;
}

.insight-chip {
  color: #8a766a;
  background: transparent;
}

.intent-hint {
  color: #8a684e;
  background: transparent;
}
</style>
