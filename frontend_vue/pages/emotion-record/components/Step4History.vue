<template>
  <view class="history-preview">
    <view class="card-content">
      <view class="card-header">
        <view class="card-title">最近记录</view>
        <view class="more-link" @click="goToHistory">查看全部</view>
      </view>
      
      <view class="history-list" v-if="records.length > 0">
        <view 
          v-for="(record, index) in records" 
          :key="index"
          class="history-item"
        >
          <view class="history-emotion">
            <image 
              v-if="getEmotionImage(record.mood)" 
              :src="getEmotionImage(record.mood)" 
              class="emotion-icon"
              mode="aspectFit"
            />
            <text v-else class="emotion-emoji">{{ getEmotionEmoji(record.mood) }}</text>
          </view>
          <view class="history-info">
            <view class="history-mood">{{ record.mood }}</view>
            <view class="history-time">{{ formatTime(record.created_at) }}</view>
          </view>
          <view class="history-tags">
            <text 
              v-for="(tag, tagIndex) in record.tags ? record.tags.split(',').slice(0, 2) : []" 
              :key="tagIndex"
              class="tag"
            >
              {{ tag }}
            </text>
          </view>
        </view>
      </view>
      
      <view class="empty-state" v-else>
        <text class="empty-text">暂无记录</text>
        <text class="empty-hint">开始记录你的情绪吧</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const records = ref([])

const emotionEmojis = {
  '崩溃': '😣',
  '迷茫': '😕',
  '低落': '🙁',
  '平静': '😐',
  '轻松': '🙂',
  '愉快': '😊',
  '极好': '😄'
}

const emotionImages = {
  '崩溃': '/static/images/emotion-crash.png',
  '迷茫': '/static/images/emotion-confused.png',
  '低落': '/static/images/emotion-down.png',
  '平静': '/static/images/emotion-calm.png',
  '轻松': '/static/images/emotion-relaxed.png',
  '愉快': '/static/images/emotion-happy.png',
  '极好': '/static/images/emotion-excellent.png'
}

const getEmotionEmoji = (mood) => {
  return emotionEmojis[mood] || '😐'
}

const getEmotionImage = (mood) => {
  return emotionImages[mood] || ''
}

const formatTime = (time) => {
  if (!time) return ''
  const date = new Date(time)
  const month = date.getMonth() + 1
  const day = date.getDate()
  const hours = date.getHours()
  const minutes = date.getMinutes().toString().padStart(2, '0')
  return `${month}/${day} ${hours}:${minutes}`
}

const goToHistory = () => {
  uni.navigateTo({ url: '/pages/emotion-record/history' })
}

onMounted(() => {
  // 模拟加载历史记录
  const storedRecords = uni.getStorageSync('emotionRecords')
  if (storedRecords) {
    records.value = JSON.parse(storedRecords).slice(0, 3)
  }
})
</script>

<style lang="scss" scoped>
.history-preview {
  width: 100%;
  padding: 20rpx 40rpx;
}

.card-content {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 32rpx;
  padding: 40rpx;
  box-shadow: 0 8rpx 24rpx rgba(107, 91, 71, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30rpx;
}

.card-title {
  font-size: 32rpx;
  font-weight: 700;
  color: #6B5B47;
}

.more-link {
  font-size: 24rpx;
  color: #98D8C8;
  font-weight: 500;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.history-item {
  display: flex;
  align-items: center;
  padding: 20rpx;
  background: #F5F5DC;
  border-radius: 20rpx;
}

.history-emotion {
  width: 60rpx;
  height: 60rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 20rpx;
}

.emotion-icon {
  width: 50rpx;
  height: 50rpx;
}

.emotion-emoji {
  font-size: 40rpx;
}

.history-info {
  flex: 1;
}

.history-mood {
  font-size: 28rpx;
  font-weight: 600;
  color: #6B5B47;
  margin-bottom: 4rpx;
}

.history-time {
  font-size: 22rpx;
  color: #888;
}

.history-tags {
  display: flex;
  gap: 8rpx;
}

.tag {
  padding: 4rpx 12rpx;
  background: rgba(152, 216, 200, 0.3);
  border-radius: 12rpx;
  font-size: 20rpx;
  color: #6B5B47;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40rpx;
}

.empty-text {
  font-size: 28rpx;
  color: #888;
  margin-bottom: 8rpx;
}

.empty-hint {
  font-size: 24rpx;
  color: #AAA;
}
</style>
