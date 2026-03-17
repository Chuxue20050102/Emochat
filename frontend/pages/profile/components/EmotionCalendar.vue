<template>
  <view class="calendar-card">
    <view class="calendar-header">
      <view class="arrow left" @click="changeMonth(-1)">
        <text class="arrow-icon">〈</text>
      </view>
      <view class="current-month">{{ currentYear }}年 {{ currentMonth }}月</view>
      <view class="arrow right" @click="changeMonth(1)" :class="{ disabled: isCurrentMonth }">
        <text class="arrow-icon">〉</text>
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
        :class="{ 'empty-cell': !day.date, 'today': day.isToday, 'selected': selectedDate === day.fullDate }"
        @click="handleDayClick(day)"
      >
        <text class="day-number" v-if="day.date">{{ day.date }}</text>
        
        <view v-if="day.records && day.records.length > 0" class="dot-container">
          <view 
            class="emotion-dot" 
            :class="{ 'multi-record': day.records.length > 1 }"
            :style="{ 
              backgroundColor: getEmotionColor(day.records[0].emotionName),
              borderColor: day.records.length > 1 ? getEmotionColor(day.records[0].emotionName) : 'transparent'
            }"
          ></view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  mockRecords: { type: Object, default: () => ({}) },
  emotionRules: { type: Object, default: () => ({}) },
  selectedDate: { type: String, default: '' }
})

const emit = defineEmits(['dayClick', 'monthChange'])

const today = new Date('2026-03-17')
const realTodayStr = '2026-03-17' 
const currentDate = ref(new Date('2026-03-17'))
const isChangingMonth = ref(false)
const weeks = ['日', '一', '二', '三', '四', '五', '六']

const currentYear = computed(() => currentDate.value.getFullYear())
const currentMonth = computed(() => currentDate.value.getMonth() + 1)
const isCurrentMonth = computed(() => currentYear.value === today.getFullYear() && currentMonth.value === today.getMonth() + 1)

const getEmotionColor = (name) => props.emotionRules[name]?.color || '#E0E0E0'

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
      records: props.mockRecords[fullDate] || []
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
  }, 150)
}

const handleDayClick = (day) => {
  if (!day.date || !day.records.length) return
  emit('dayClick', day)
}
</script>

<style lang="scss" scoped>
.calendar-card {
  background: #FFFFFF;
  border-radius: 40rpx;
  padding: 40rpx;
  box-shadow: 0 10rpx 40rpx rgba(0,0,0,0.03);
}
.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40rpx;
}
.current-month {
  font-size: 34rpx;
  font-weight: 600;
  color: #1A1A1A;
}
.arrow {
  padding: 10rpx 30rpx;
}
.arrow.disabled {
  opacity: 0.2;
}
.arrow-icon {
  font-size: 30rpx;
  color: #666;
}
.week-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 30rpx;
}
.week-item {
  width: calc(100% / 7);
  text-align: center;
  font-size: 26rpx;
  color: #999;
}
.days-grid {
  display: flex;
  flex-wrap: wrap;
  transition: opacity 0.15s ease-in-out;
}
.days-grid.fade-transition {
  opacity: 0;
}
.day-cell {
  width: calc(100% / 7);
  height: 80rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  margin-bottom: 20rpx;
  position: relative;
  transition: transform 0.15s;
}
.day-cell:active {
  transform: scale(0.9);
}
.day-number {
  font-size: 30rpx;
  color: #333;
  width: 50rpx;
  height: 50rpx;
  text-align: center;
  line-height: 50rpx;
  z-index: 2;
}
.day-cell.today .day-number {
  font-weight: 600;
  color: #FF7B54;
  background: rgba(255, 123, 84, 0.1);
  border-radius: 50%;
}
.day-cell.selected .emotion-dot {
  transform: scale(1.4);
}
.dot-container {
  height: 20rpx;
  display: flex;
  justify-content: center;
  align-items: center;
}
.emotion-dot {
  width: 12rpx;
  height: 12rpx;
  border-radius: 50%;
  transition: all 0.2s cubic-bezier(0.18, 0.89, 0.32, 1.28);
  box-shadow: 0 2rpx 6rpx rgba(0,0,0,0.08);
}
.emotion-dot.multi-record {
  background-color: transparent !important;
  border: 4rpx solid;
  box-sizing: border-box;
}
</style>
