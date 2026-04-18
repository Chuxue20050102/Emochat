<template>
  <view class="environment-selector">
    <view class="card-content">
      <view class="card-title">环境场景</view>
      
      <!-- 天气选择 -->
      <view class="section-label">天气</view>
      <view class="option-grid">
        <view 
          v-for="weather in weatherOptions" 
          :key="weather.value"
          :class="['option-item', { active: selectedWeather === weather.value }]"
          @click="selectWeather(weather.value)"
        >
          <text class="option-icon">{{ weather.icon }}</text>
          <text class="option-text">{{ weather.label }}</text>
        </view>
      </view>
      
      <!-- 环境选择 -->
      <view class="section-label">环境</view>
      <view class="option-grid">
        <view 
          v-for="env in envOptions" 
          :key="env.value"
          :class="['option-item', { active: selectedEnv === env.value }]"
          @click="selectEnv(env.value)"
        >
          <text class="option-icon">{{ env.icon }}</text>
          <text class="option-text">{{ env.label }}</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['select'])

const selectedWeather = ref('')
const selectedEnv = ref('')

const weatherOptions = [
  { label: '晴天', value: 'sunny', icon: '☀️' },
  { label: '阴天', value: 'cloudy', icon: '☁️' },
  { label: '雨天', value: 'rainy', icon: '🌧️' },
  { label: '雪天', value: 'snowy', icon: '❄️' },
  { label: '夜晚', value: 'night', icon: '🌙' }
]

const envOptions = [
  { label: '室内', value: 'indoor', icon: '🏠' },
  { label: '户外', value: 'outdoor', icon: '🌳' },
  { label: '公司', value: 'office', icon: '🏢' },
  { label: '学校', value: 'school', icon: '🏫' },
  { label: '家里', value: 'home', icon: '🏡' },
  { label: '其他', value: 'other', icon: '📌' }
]

const selectWeather = (weather) => {
  selectedWeather.value = weather
  emitSelection()
}

const selectEnv = (env) => {
  selectedEnv.value = env
  emitSelection()
}

const emitSelection = () => {
  emit('select', {
    weather: selectedWeather.value,
    environment: selectedEnv.value
  })
}
</script>

<style lang="scss" scoped>
.environment-selector {
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

.section-label {
  font-size: 26rpx;
  font-weight: 600;
  color: #6B5B47;
  margin-bottom: 20rpx;
}

.option-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16rpx;
  margin-bottom: 30rpx;
}

.option-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 24rpx 16rpx;
  background: #F5F5DC;
  border-radius: 20rpx;
  transition: all 0.3s ease;
  border: 2rpx solid transparent;
}

.option-item.active {
  background: linear-gradient(135deg, #98D8C8, #74C7B8);
  border-color: rgba(120, 200, 180, 0.3);
  box-shadow: 0 4rpx 12rpx rgba(120, 200, 180, 0.25);
}

.option-icon {
  font-size: 40rpx;
  margin-bottom: 8rpx;
}

.option-text {
  font-size: 24rpx;
  font-weight: 500;
  color: #6B5B47;
}

.option-item.active .option-text {
  color: #FFF;
}

.option-item:active {
  transform: scale(0.95);
}
</style>
