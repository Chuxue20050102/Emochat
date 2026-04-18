<template>
  <view class="time-selector">
    <view class="card-content">
      <view class="card-title">记录时间</view>
      
      <!-- 日期选择 -->
      <view class="time-row">
        <view class="time-label">日期</view>
        <view class="date-input">
          <input 
            type="date" 
            v-model="selectedDate" 
            @change="emitTime"
            class="date-input-field"
            :max="maxDate"
          />
        </view>
      </view>
      
      <!-- 时间段选择 -->
      <view class="time-row">
        <view class="time-label">时段</view>
        <view class="time-options">
          <view 
            v-for="time in timeOptions" 
            :key="time.value"
            :class="['time-option', { active: selectedTime === time.value }]"
            @click="selectTime(time.value)"
          >
            {{ time.label }}
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'

const emit = defineEmits(['select'])

const selectedDate = ref('')
const selectedTime = ref('morning')

const timeOptions = [
  { label: '早上', value: 'morning' },
  { label: '下午', value: 'afternoon' },
  { label: '晚上', value: 'evening' },
  { label: '深夜', value: 'night' }
]

const maxDate = computed(() => {
  const today = new Date()
  const year = today.getFullYear()
  const month = (today.getMonth() + 1).toString().padStart(2, '0')
  const day = today.getDate().toString().padStart(2, '0')
  return `${year}-${month}-${day}`
})

onMounted(() => {
  // 设置默认日期为今天
  const today = new Date()
  const year = today.getFullYear()
  const month = (today.getMonth() + 1).toString().padStart(2, '0')
  const day = today.getDate().toString().padStart(2, '0')
  selectedDate.value = `${year}-${month}-${day}`
  emitTime()
})

const selectTime = (time) => {
  selectedTime.value = time
  emitTime()
}

const emitTime = () => {
  emit('select', {
    date: selectedDate.value,
    time: selectedTime.value
  })
}
</script>

<style lang="scss" scoped>
.time-selector {
  width: 100%;
  padding: 20rpx 40rpx;
}

.card-content {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 32rpx;
  padding: 40rpx;
  box-shadow: 0 8rpx 24rpx rgba(107, 91, 71, 0.1);
}

.card-title {
  font-size: 32rpx;
  font-weight: 700;
  color: #6B5B47;
  margin-bottom: 30rpx;
  white-space: nowrap;
}

.time-row {
  margin-bottom: 24rpx;
}

.time-row:last-child {
  margin-bottom: 0;
}

.time-label {
  font-size: 26rpx;
  font-weight: 600;
  color: #6B5B47;
  margin-bottom: 16rpx;
}

.date-input {
  padding: 0;
  background: #F5F5DC;
  border-radius: 24rpx;
  border: 2rpx solid transparent;
  transition: all 0.3s ease;
}

.date-input-field {
  width: 100%;
  padding: 20rpx 24rpx;
  background: transparent;
  border: none;
  font-size: 28rpx;
  font-weight: 500;
  color: #6B5B47;
  font-family: 'SimSun', serif;
}

.date-input-field::-webkit-calendar-picker-indicator {
  filter: invert(40%) sepia(0%) saturate(0%) hue-rotate(0deg) brightness(100%) contrast(100%);
  cursor: pointer;
}

.date-input:active {
  transform: scale(0.98);
}

.time-options {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;
}

.time-option {
  padding: 16rpx 28rpx;
  background: #F5F5DC;
  border-radius: 24rpx;
  font-size: 26rpx;
  font-weight: 500;
  color: #6B5B47;
  transition: all 0.3s ease;
  border: 2rpx solid transparent;
}

.time-option.active {
  background: linear-gradient(135deg, #98D8C8, #74C7B8);
  color: #FFF;
  border-color: rgba(120, 200, 180, 0.3);
  box-shadow: 0 4rpx 12rpx rgba(120, 200, 180, 0.25);
}

.time-option:active {
  transform: scale(0.95);
}
</style>
