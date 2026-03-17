<template>
  <view>
    <view class="bottom-sheet-mask" :class="{ 'show': show }" @click="close"></view>
    <view class="bottom-sheet" :class="{ 'show': show }">
      <view class="sheet-handler"></view>
      <view class="sheet-content" v-if="dayData">
        <view class="sheet-header">
          <text class="sheet-date">{{ formatDateWithMonth(dayData.fullDate) }}</text>
          <text class="sheet-emotion" :style="{ color: getEmotionColor(dayData.records[0].emotionName) }">
            {{ dayData.records[0].emoji }} {{ dayData.records[0].emotionName }}
          </text>
        </view>
        <view class="sheet-body">
          <text class="record-content">{{ dayData.records[0].content || '这一天你留下了情绪脚印，但没有写下具体文字。' }}</text>
          <view class="multi-hint" v-if="dayData.records.length > 1">
            还有 {{ dayData.records.length - 1 }} 条记录未显示...
          </view>
        </view>
        <view class="sheet-footer">
          <button class="view-detail-btn" @click="goToDetail">查看完整记录 →</button>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
const props = defineProps({
  show: Boolean,
  dayData: Object,
  emotionRules: Object
})
const emit = defineEmits(['close', 'detail'])

const close = () => emit('close')
const goToDetail = () => {
  uni.showToast({ title: '加载具体日志中...', icon: 'none' })
  close()
}

const getEmotionColor = (name) => props.emotionRules[name]?.color || '#E0E0E0'

const formatDateWithMonth = (dateStr) => {
  if (!dateStr) return ''
  const [, month, day] = dateStr.split('-')
  return `${parseInt(month)}月${parseInt(day)}日`
}
</script>

<style lang="scss" scoped>
.bottom-sheet-mask {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.4);
  z-index: 900;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s ease;
}
.bottom-sheet-mask.show {
  opacity: 1;
  pointer-events: auto;
}
.bottom-sheet {
  position: fixed;
  left: 0; right: 0; bottom: 0;
  background: #FFF;
  border-radius: 40rpx 40rpx 0 0;
  z-index: 901;
  padding: 30rpx 50rpx 100rpx;
  transform: translateY(100%);
  transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 -10rpx 40rpx rgba(0,0,0,0.05);
}
.bottom-sheet.show {
  transform: translateY(0);
}
.sheet-handler {
  width: 80rpx;
  height: 8rpx;
  background: #E0E0E0;
  border-radius: 4rpx;
  margin: 0 auto 40rpx;
}
.sheet-header {
  display: flex;
  align-items: center;
  gap: 20rpx;
  margin-bottom: 30rpx;
}
.sheet-date {
  font-size: 34rpx;
  color: #1A1A1A;
  font-weight: 600;
}
.sheet-emotion {
  font-size: 30rpx;
  font-weight: 500;
}
.sheet-body {
  margin-bottom: 50rpx;
}
.record-content {
  font-size: 32rpx;
  color: #333;
  line-height: 1.6;
}
.multi-hint {
  font-size: 26rpx;
  color: #999;
  margin-top: 16rpx;
}
.sheet-footer {
  width: 100%;
}
.view-detail-btn {
  background: #F7F8FC;
  color: #666;
  border-radius: 99rpx;
  font-size: 28rpx;
  border: none;
  width: 100%;
}
.view-detail-btn::after {
  border: none;
}
</style>
