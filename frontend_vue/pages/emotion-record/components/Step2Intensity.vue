<template>
  <view class="intensity-selector">
    <view class="card-content">
      <view class="card-title">情绪强度</view>
      <view class="slider-container">
        <text class="slider-label">轻微</text>
        <view class="slider-wrapper">
          <slider 
            :value="intensity" 
            :min="1" 
            :max="10" 
            :step="1"
            :selected-color="'#98D8C8'"
            :block-size="24"
            @change="onSliderChange"
          />
        </view>
        <text class="slider-label">强烈</text>
      </view>
      <view class="intensity-value">
        <text class="value-number">{{ intensity }}</text>
        <text class="value-text">分</text>
      </view>
      <view class="intensity-description">
        {{ getIntensityDescription() }}
      </view>
      
      <!-- 环境场景 -->
      <view class="section-divider"></view>
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
      

    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['select'])

const intensity = ref(5)
const selectedWeather = ref('')

const intensityDescriptions = {
  1: '几乎感觉不到',
  2: '非常微弱',
  3: '比较轻微',
  4: '有些明显',
  5: '中等程度',
  6: '比较强烈',
  7: '很强烈',
  8: '非常强烈',
  9: '极其强烈',
  10: '无法承受'
}

const weatherOptions = [
  { label: '晴天', value: 'sunny', icon: '☀️' },
  { label: '阴天', value: 'cloudy', icon: '☁️' },
  { label: '雨天', value: 'rainy', icon: '🌧️' },
  { label: '雪天', value: 'snowy', icon: '❄️' }
]



const getIntensityDescription = () => {
  return intensityDescriptions[intensity.value] || ''
}

const onSliderChange = (e) => {
  intensity.value = e.detail.value
  emitSelection()
}

const selectWeather = (weather) => {
  selectedWeather.value = weather
  emitSelection()
}



const emitSelection = () => {
  emit('select', {
    intensity: intensity.value,
    weather: selectedWeather.value
  })
}
</script>

<style lang="scss" scoped>
.intensity-selector {
  width: 100%;
  padding: 20rpx 40rpx;
  overflow-y: auto;
  max-height: 80vh;
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
  margin-bottom: 40rpx;
  white-space: nowrap;
}

.slider-container {
  display: flex;
  align-items: center;
  gap: 20rpx;
  margin-bottom: 30rpx;
}

.slider-label {
  font-size: 24rpx;
  color: #888;
  width: 60rpx;
  text-align: center;
}

.slider-wrapper {
  flex: 1;
}

.slider-wrapper slider {
  width: 100%;
}

.intensity-value {
  display: flex;
  justify-content: center;
  align-items: baseline;
  margin-bottom: 20rpx;
}

.value-number {
  font-size: 64rpx;
  font-weight: 700;
  color: #98D8C8;
}

.value-text {
  font-size: 28rpx;
  color: #6B5B47;
  margin-left: 8rpx;
}

.intensity-description {
  text-align: center;
  font-size: 26rpx;
  color: #888;
  margin-bottom: 30rpx;
}

.section-divider {
  height: 2rpx;
  background: linear-gradient(90deg, transparent, #E0E0E0, transparent);
  margin: 20rpx 0 30rpx;
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
