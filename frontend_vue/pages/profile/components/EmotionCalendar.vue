<template>
  <view class="calendar-card">
    <view class="calendar-header">
      <view class="arrow left" @click="changeMonth(-1)">
        <text class="arrow-icon">‹</text>
      </view>
      <view class="current-month">{{ currentYear }}年 {{ currentMonth }}月</view>
      <view class="arrow right" @click="changeMonth(1)" :class="{ disabled: isCurrentMonth }">
        <text class="arrow-icon">›</text>
      </view>
    </view>

    <view class="week-header">
      <text v-for="w in weeks" :key="w" class="week-item">{{ w }}</text>
    </view>

    <view class="days-grid" :class="{ 'fade-transition': isChangingMonth }">
      <view
        v-for="(day, index) in calendarDays"
        :key="index"
        class="day-cell"
        :class="{ 'empty-cell': !day.date, today: day.isToday, selected: selectedDate === day.fullDate }"
        @click="handleDayClick(day)"
      >
        <text class="day-number" v-if="day.date">{{ day.date }}</text>

        <view v-if="day.records && day.records.length > 0" class="dot-container">
          <view
            class="emotion-dot"
            :class="{ 'multi-record': day.records.length > 1 }"
            :style="{
              backgroundColor: getEmotionColor(day.records[0].emotionName),
              borderColor: day.records.length > 1 ? getEmotionColor(day.records[0].emotionName) : 'transparent',
            }"
          ></view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  mockRecords: { type: Object, default: () => ({}) },
  emotionRules: { type: Object, default: () => ({}) },
  selectedDate: { type: String, default: '' },
})

const emit = defineEmits(['dayClick', 'monthChange'])

const today = new Date()
const realTodayStr = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`
const currentDate = ref(new Date())
const isChangingMonth = ref(false)
const weeks = ['日', '一', '二', '三', '四', '五', '六']

const currentYear = computed(() => currentDate.value.getFullYear())
const currentMonth = computed(() => currentDate.value.getMonth() + 1)
const isCurrentMonth = computed(() => currentYear.value === today.getFullYear() && currentMonth.value === today.getMonth() + 1)

const getEmotionColor = (name) => props.emotionRules[name]?.color || '#d6dceb'

const calendarDays = computed(() => {
  const year = currentYear.value
  const month = currentMonth.value - 1
  const firstDay = new Date(year, month, 1)
  const lastDay = new Date(year, month + 1, 0)

  const days = []
  for (let i = 0; i < firstDay.getDay(); i++) days.push({ date: null })

  for (let i = 1; i <= lastDay.getDate(); i++) {
    const fullDate = `${year}-${String(month + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`
    days.push({
      date: i,
      fullDate,
      isToday: fullDate === realTodayStr,
      records: props.mockRecords[fullDate] || [],
    })
  }

  const remaining = (7 - (days.length % 7)) % 7
  for (let i = 0; i < remaining; i++) days.push({ date: null })

  return days
})

const changeMonth = (delta) => {
  if (delta === 1 && isCurrentMonth.value) return
  isChangingMonth.value = true
  setTimeout(() => {
    const newDate = new Date(currentDate.value)
    newDate.setMonth(newDate.getMonth() + delta)
    currentDate.value = newDate
    isChangingMonth.value = false
    emit('monthChange', { year: currentYear.value, month: currentMonth.value })
  }, 140)
}

const handleDayClick = (day) => {
  if (!day.date || !day.records.length) return
  emit('dayClick', day)
}
</script>

<style lang="scss" scoped>
.calendar-card {
  background: rgba(255, 255, 255, 0.78);
  border: 2rpx solid rgba(255, 255, 255, 0.88);
  border-radius: 34rpx;
  padding: 26rpx;
  box-shadow: 0 18rpx 44rpx rgba(45, 57, 94, 0.14);
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 18rpx;
}

.current-month {
  font-size: 30rpx;
  font-weight: 700;
  color: #202a43;
}

.arrow {
  width: 56rpx;
  height: 56rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(246, 249, 255, 0.95);
  border: 2rpx solid #dce3f4;
}

.arrow.disabled {
  opacity: 0.3;
}

.arrow-icon {
  font-size: 28rpx;
  color: #64708c;
  line-height: 1;
}

.week-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 14rpx;
}

.week-item {
  width: calc(100% / 7);
  text-align: center;
  font-size: 22rpx;
  color: #8390ab;
}

.days-grid {
  display: flex;
  flex-wrap: wrap;
  transition: opacity 0.15s ease;
}

.days-grid.fade-transition {
  opacity: 0;
}

.day-cell {
  width: calc(100% / 7);
  height: 74rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  margin-bottom: 12rpx;
  border-radius: 16rpx;
}

.day-number {
  width: 46rpx;
  height: 46rpx;
  line-height: 46rpx;
  text-align: center;
  font-size: 24rpx;
  color: #33415f;
}

.day-cell.today .day-number {
  background: rgba(141, 187, 255, 0.24);
  border-radius: 50%;
  color: #2f4f86;
  font-weight: 700;
}

.dot-container {
  margin-top: 4rpx;
  height: 16rpx;
  display: flex;
  justify-content: center;
}

.emotion-dot {
  width: 10rpx;
  height: 10rpx;
  border-radius: 50%;
}

.emotion-dot.multi-record {
  background-color: transparent !important;
  border: 3rpx solid;
  box-sizing: border-box;
}

.day-cell.selected .emotion-dot {
  transform: scale(1.3);
}
</style>
