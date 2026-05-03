<template>
  <view class="detail-page">
    <view class="hero-gradient"></view>

    <view class="nav-row">
      <view class="back-btn" @click="goBack">回档案</view>
      <view class="title">{{ titleText }}</view>
      <view class="placeholder"></view>
    </view>

    <view class="content-card">
      <view v-if="loading" class="empty-text">加载中...</view>
      <view v-else-if="records.length === 0" class="empty-text">这一天还没有可展示的记录</view>
      <view v-else>
        <view
          class="record-item"
          :class="{ highlighted: isSelectedRecord(item) }"
          v-for="(item, idx) in records"
          :key="item.id || idx"
        >
          <view class="record-head">
            <text class="emoji">{{ getEmoji(item.mood) }}</text>
            <text class="mood">{{ item.mood || '中性' }}</text>
            <text v-if="item.created_at" class="record-time">{{ item.created_at }}</text>
          </view>
          <view class="meta-row">
            <text class="source-chip">{{ sourceLabelMap[item.source] || '手动记录' }}</text>
          </view>
          <view class="record-body">{{ item.description || '未填写文字内容' }}</view>
          <view v-if="item.tags" class="tag-line">标签：{{ item.tags }}</view>
          <button class="record-chat-btn" @click="chatWithRecord(item)">带着这段聊聊 →</button>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { computed, ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { getEmotionDetailApi } from '@/api/index.js'
import { emotionRules as defaultEmotionRules, fetchEmotionConfig } from '@/config/emotionConfig.js'

const emotionRules = ref(defaultEmotionRules)

const dateStr = ref('')
const selectedRecordId = ref('')
const loading = ref(false)
const records = ref([])
const sourceLabelMap = {
  manual: '手动记录',
  chat: '聊天保存',
}

const titleText = computed(() => {
  if (!dateStr.value) return '情绪记录详情'
  const [, month, day] = dateStr.value.split('-')
  return `${parseInt(month, 10)}月${parseInt(day, 10)}日记录`
})

const loadDetails = async () => {
  const userId = uni.getStorageSync('user_id')
  if (!userId || !dateStr.value) return

  loading.value = true
  try {
    const res = await getEmotionDetailApi({ user_id: userId, date_str: dateStr.value })
    records.value = Array.isArray(res) ? res : []
  } catch (e) {
    uni.showToast({ title: '详情加载失败', icon: 'none' })
  } finally {
    loading.value = false
  }
}

const getEmoji = (mood) => emotionRules.value[mood]?.emoji || '😐'

const isSelectedRecord = (record) => {
  if (!selectedRecordId.value) return false
  return String(record?.id || '') === selectedRecordId.value
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
    recordDate: record.record_date || dateStr.value,
  }

  uni.setStorageSync('pendingChatContext', context)
  uni.switchTab({ url: '/pages/chat/index' })
}

const goBack = () => {
  const pages = typeof getCurrentPages === 'function' ? getCurrentPages() : []
  if (pages.length > 1) {
    uni.navigateBack()
    return
  }
  uni.switchTab({ url: '/pages/profile/index' })
}

onLoad(async (query) => {
  dateStr.value = decodeURIComponent(query?.date || '')
  selectedRecordId.value = String(query?.record_id || '')
  const config = await fetchEmotionConfig()
  emotionRules.value = config.emotionRules
  loadDetails()
})
</script>

<style lang="scss" scoped>
.detail-page {
  min-height: 100vh;
  padding: 90rpx 28rpx 28rpx;
  box-sizing: border-box;
  position: relative;
  background: $emo-page-bg;
}

.hero-gradient {
  position: absolute;
  inset: -10%;
  z-index: 0;
  filter: blur(72rpx);
  background: $emo-page-glow;
}

.nav-row,
.content-card {
  position: relative;
  z-index: 1;
}

.nav-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 22rpx;
}

.back-btn,
.placeholder {
  width: 112rpx;
}

.back-btn {
  height: 56rpx;
  border-radius: 999rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22rpx;
  color: $emo-text-sub;
  background: rgba(255, 255, 255, 0.78);
}

.title {
  font-size: 32rpx;
  font-weight: 700;
  color: $emo-text-main;
}

.content-card {
  background: rgba(255, 255, 255, 0.78);
  border: 2rpx solid rgba(255, 255, 255, 0.88);
  border-radius: 30rpx;
  padding: 22rpx;
  box-shadow: $emo-shadow-card;
}

.empty-text {
  color: $emo-text-sub;
  font-size: 26rpx;
  text-align: center;
  padding: 40rpx 0;
}

.record-item {
  padding: 18rpx 6rpx;
  border-bottom: 1rpx solid rgba(232, 219, 207, 0.8);
}

.record-item.highlighted {
  margin: 0 -8rpx;
  padding: 18rpx 14rpx;
  border-radius: 22rpx;
  background: rgba(237, 250, 243, 0.72);
  border-bottom-color: transparent;
}

.record-item:last-child {
  border-bottom: none;
}

.record-head {
  display: flex;
  align-items: center;
  gap: 10rpx;
}

.emoji {
  font-size: 30rpx;
}

.mood {
  font-size: 27rpx;
  color: $emo-text-main;
  font-weight: 600;
}

.record-time {
  margin-left: auto;
  font-size: 21rpx;
  color: $emo-text-sub;
}

.record-body {
  margin-top: 10rpx;
  font-size: 26rpx;
  line-height: 1.55;
  color: $emo-text-main;
}

.meta-row {
  margin-top: 10rpx;
}

.source-chip {
  display: inline-flex;
  padding: 4rpx 12rpx;
  border-radius: 999rpx;
  font-size: 20rpx;
  color: $emo-sage-text;
  background: rgba(237, 250, 243, 0.86);
}

.tag-line {
  margin-top: 8rpx;
  font-size: 22rpx;
  color: $emo-text-sub;
}

.record-chat-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: fit-content;
  min-width: 0;
  height: 52rpx;
  margin: 16rpx 0 0;
  padding: 0 22rpx;
  border-radius: 999rpx;
  color: $emo-sage-text;
  font-size: 23rpx;
  font-weight: 700;
  line-height: 52rpx;
  background: rgba(237, 250, 243, 0.92);
  border: 1rpx solid rgba(92, 131, 111, 0.18);
  box-shadow: none;
}

.record-chat-btn::after {
  border: 0;
}
</style>
