<template>
  <view class="step-content">
    <view class="step-title">
      这份情绪，可能和这些有关
      <text class="sub-title-mark">（可多选）</text>
    </view>

    <view class="custom-row">
      <input
        v-model.trim="customTagInput"
        class="custom-input"
        placeholder="添加自定义原因（如：生理期、天气变化）"
        maxlength="20"
      />
      <view class="add-btn" @click="handleAddCustomTag">添加</view>
    </view>

    <view class="tags-grid">
      <view
        v-for="tag in reasonTags"
        :key="tag"
        class="tag-item"
        :class="{ selected: selectedReasons.includes(tag) }"
        @click="$emit('toggle', tag)"
      >
        {{ tag }}
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  reasonTags: {
    type: Array,
    default: () => [],
  },
  selectedReasons: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits(['toggle', 'add-custom'])
const customTagInput = ref('')

const handleAddCustomTag = () => {
  const value = customTagInput.value.trim()
  if (!value) return
  emit('add-custom', value)
  customTagInput.value = ''
}
</script>

<style lang="scss" scoped>
.step-content {
  padding: 0 36rpx;
}

.step-title {
  font-size: 34rpx;
  font-weight: 700;
  color: $emo-text-main;
  margin-bottom: 20rpx;
}

.sub-title-mark {
  font-size: 24rpx;
  font-weight: 400;
  color: $emo-text-disabled;
  margin-left: 8rpx;
}

.custom-row {
  display: flex;
  gap: 12rpx;
  margin-bottom: 18rpx;
}

.custom-input {
  flex: 1;
  height: 78rpx;
  border-radius: 18rpx;
  background: rgba(255, 255, 255, 0.9);
  padding: 0 18rpx;
  font-size: 24rpx;
  color: $emo-text-main;
  border: 1rpx solid rgba(232, 219, 207, 0.8);
}

.add-btn {
  width: 100rpx;
  height: 78rpx;
  border-radius: 18rpx;
  background: linear-gradient(135deg, #5c836f, #3f6d59);
  color: #fff;
  font-size: 24rpx;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tags-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 14rpx;
}

.tag-item {
  height: 88rpx;
  border-radius: 999rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.86);
  color: $emo-text-main;
  font-size: 26rpx;
}

.tag-item.selected {
  background: linear-gradient(135deg, rgba(255, 220, 181, 0.48), rgba(188, 226, 205, 0.5));
  color: $emo-sage-text;
  font-weight: 600;
}
</style>
