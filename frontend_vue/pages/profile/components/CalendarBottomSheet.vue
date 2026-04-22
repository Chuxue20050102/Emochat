<template>
  <view>
    <view class="bottom-sheet-mask" :class="{ show: show }" @click="close"></view>
    <view class="bottom-sheet" :class="{ show: show }">
      <view class="sheet-handler"></view>
      <view class="sheet-content" v-if="dayData">
        <view class="sheet-header">
          <text class="sheet-date">{{ formatDateWithMonth(dayData.fullDate) }}</text>
          <text class="sheet-emotion" :style="{ color: getEmotionColor(dayData.records[0].emotionName) }">
            {{ dayData.records[0].emoji }} {{ dayData.records[0].emotionName }}
          </text>
        </view>

        <view class="sheet-body">
          <text class="record-content">{{ dayData.records[0].content || '这一天你有记录情绪，但没有填写文字。' }}</text>
          <view class="multi-hint" v-if="dayData.records.length > 1">还有 {{ dayData.records.length - 1 }} 条记录未展示</view>
        </view>

        <view class="sheet-footer">
          <button class="view-detail-btn" @click="goToDetail">查看完整记录</button>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
const props = defineProps({
  show: Boolean,
  dayData: Object,
  emotionRules: Object,
})

const emit = defineEmits(['close', 'detail'])

const close = () => emit('close')

const goToDetail = () => {
  // 当前先给提示，后续可扩展独立详情页
  uni.showToast({ title: '详细日志功能开发中', icon: 'none' })
  close()
}

const getEmotionColor = (name) => props.emotionRules[name]?.color || '#8c95ab'

const formatDateWithMonth = (dateStr) => {
  if (!dateStr) return ''
  const [, month, day] = dateStr.split('-')
  return `${parseInt(month, 10)}月${parseInt(day, 10)}日`
}
</script>

<style lang="scss" scoped>
.bottom-sheet-mask {
  position: fixed;
  inset: 0;
  background: rgba(19, 24, 40, 0.35);
  z-index: 900;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.24s ease;
}

.bottom-sheet-mask.show {
  opacity: 1;
  pointer-events: auto;
}

.bottom-sheet {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.94);
  border-radius: 34rpx 34rpx 0 0;
  z-index: 901;
  padding: 24rpx 30rpx 80rpx;
  transform: translateY(100%);
  transition: transform 0.34s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 -10rpx 34rpx rgba(32, 43, 71, 0.14);
}

.bottom-sheet.show {
  transform: translateY(0);
}

.sheet-handler {
  width: 76rpx;
  height: 8rpx;
  border-radius: 999rpx;
  background: #d6dced;
  margin: 0 auto 20rpx;
}

.sheet-header {
  display: flex;
  align-items: center;
  gap: 14rpx;
}

.sheet-date {
  font-size: 30rpx;
  font-weight: 700;
  color: #202a42;
}

.sheet-emotion {
  font-size: 26rpx;
  font-weight: 600;
}

.sheet-body {
  margin-top: 16rpx;
}

.record-content {
  font-size: 27rpx;
  color: #445271;
  line-height: 1.55;
}

.multi-hint {
  margin-top: 10rpx;
  font-size: 22rpx;
  color: #7a859f;
}

.sheet-footer {
  margin-top: 20rpx;
}

.view-detail-btn {
  width: 100%;
  border: none;
  height: 86rpx;
  border-radius: 999rpx;
  font-size: 26rpx;
  color: #2d436c;
  background: rgba(141, 187, 255, 0.2);
}

.view-detail-btn::after {
  border: none;
}
</style>
