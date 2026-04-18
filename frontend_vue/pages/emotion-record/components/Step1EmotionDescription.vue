<template>
  <view class="emotion-description">
    <view class="card-content">
      <view class="card-title">描述你的感受</view>
      <view class="emotion-display">
        <text class="emoji">{{ selectedEmotion?.emoji }}</text>
        <text class="emotion-name">{{ selectedEmotion?.name }}</text>
      </view>
      <view class="description-input">
        <textarea 
          v-model="description" 
          placeholder="请详细描述你此刻的感受..." 
          placeholder-style="color: #888; font-size: 26rpx;"
        />
      </view>
      <view class="suggestions">
        <text class="suggestion-label">你可以这样描述：</text>
        <view class="suggestion-list">
          <view 
            v-for="(suggestion, index) in getSuggestions()" 
            :key="index"
            class="suggestion-item"
            @click="selectSuggestion(suggestion)"
          >
            <text>{{ suggestion }}</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  selectedEmotion: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['select'])

const description = ref('')

const emotionSuggestions = {
  '崩溃': [
    '我感觉自己快要承受不住了',
    '所有的事情都在同时压向我',
    '我感到非常焦虑和无助',
    '心里像有一块大石头压着',
    '我想找个地方躲起来，什么都不管'
  ],
  '迷茫': [
    '我不知道自己该往哪个方向走',
    '对未来感到不确定和害怕',
    '感觉自己好像失去了方向',
    '不知道自己到底想要什么',
    '对现状感到困惑和不安'
  ],
  '低落': [
    '感觉心情沉重，提不起精神',
    '对什么事情都没有兴趣',
    '感到孤独和无助',
    '像是被一片乌云笼罩着',
    '没有动力做任何事情'
  ],
  '平静': [
    '感觉内心很平和，没有波澜',
    '像一潭平静的湖水',
    '没有特别的情绪，只是单纯的存在',
    '感觉很放松，没有压力',
    '心情很稳定，不悲不喜'
  ],
  '轻松': [
    '感觉浑身都很放松',
    '像是卸下了沉重的包袱',
    '心情很愉快，没有压力',
    '整个人都很轻盈',
    '感觉自由自在，无拘无束'
  ],
  '愉快': [
    '心里充满了喜悦和满足',
    '感觉生活很美好',
    '忍不住想笑，心情特别好',
    '对未来充满期待',
    '周围的一切都变得很可爱'
  ],
  '极好': [
    '感觉自己充满了能量',
    '像是站在世界的顶端',
    '内心充满了感激和幸福',
    '觉得自己无所不能',
    '这种感觉太棒了，希望能一直保持'
  ]
}

const getSuggestions = () => {
  if (!props.selectedEmotion) return []
  return emotionSuggestions[props.selectedEmotion.name] || []
}

const selectSuggestion = (suggestion) => {
  description.value = suggestion
  emitSelection()
}

const emitSelection = () => {
  emit('select', description.value)
}
</script>

<style lang="scss" scoped>
.emotion-description {
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

.emotion-display {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 40rpx;
}

.emoji {
  font-size: 80rpx;
  margin-bottom: 20rpx;
}

.emotion-name {
  font-size: 36rpx;
  font-weight: 600;
  color: #6B5B47;
}

.description-input {
  margin-bottom: 40rpx;
}

.description-input textarea {
  width: 100%;
  height: 200rpx;
  padding: 20rpx;
  border: 2rpx solid #E0E0E0;
  border-radius: 16rpx;
  font-size: 26rpx;
  color: #6B5B47;
  background: #F9F9F9;
  resize: none;
  font-family: 'SimSun', serif;
}

.suggestions {
  margin-top: 20rpx;
}

.suggestion-label {
  font-size: 26rpx;
  font-weight: 600;
  color: #6B5B47;
  margin-bottom: 20rpx;
  display: block;
}

.suggestion-list {
  display: flex;
  flex-direction: column;
  gap: 12rpx;
}

.suggestion-item {
  padding: 20rpx;
  background: #F5F5DC;
  border-radius: 16rpx;
  font-size: 24rpx;
  color: #6B5B47;
  transition: all 0.3s ease;
  border: 2rpx solid transparent;
}

.suggestion-item:hover {
  background: #E8E8C0;
  border-color: rgba(152, 216, 200, 0.3);
  transform: translateY(-2rpx);
}

.suggestion-item:active {
  transform: scale(0.98);
}
</style>