<template>
  <view class="recent-card">
    <view class="card-head">
      <view>
        <text class="eyebrow">最近记录</text>
        <text class="title">这些感受已经被你留下来了</text>
      </view>
      <text class="meta">最近 {{ limit }} 条</text>
    </view>

    <view v-if="records.length === 0" class="empty-state">
      <text class="empty-title">这里会慢慢出现你最近留下的内容</text>
      <text class="empty-desc">先记录一次心情，或在陪聊里保存一段感受，都可以在这里看到。</text>
    </view>

    <view v-else class="record-list">
      <view v-for="item in records" :key="item.id" class="record-item">
        <view class="record-main" @click="emit('detail', item)">
          <view class="record-top">
            <text class="record-mood">{{ item.mood || '中性' }}</text>
            <text class="record-time">{{ item.created_at || item.record_date }}</text>
          </view>
          <view class="record-meta">
            <text class="source-chip">{{ sourceLabelMap[item.source] || '手动记录' }}</text>
            <text v-if="item.tags" class="record-tags">{{ item.tags }}</text>
          </view>
          <text class="record-desc">{{ item.description || '这次记录里没有写更多文字。' }}</text>
        </view>
        <view class="record-action" @click="emit('chat', item)">聊聊这条</view>
      </view>
    </view>
  </view>
</template>

<script setup>
const sourceLabelMap = {
  manual: '手动记录',
  chat: '聊天保存',
}

const emit = defineEmits(['chat', 'detail'])

defineProps({
  limit: {
    type: Number,
    default: 5,
  },
  records: {
    type: Array,
    default: () => [],
  },
})
</script>

<style lang="scss" scoped>
.recent-card {
  margin-top: 18rpx;
  margin-bottom: 18rpx;
  padding: 24rpx;
  border-radius: 28rpx;
  background: rgba(255, 255, 255, 0.76);
  border: 2rpx solid rgba(255, 255, 255, 0.88);
  box-shadow: $emo-shadow-card;
}

.card-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16rpx;
}

.eyebrow {
  display: inline-flex;
  padding: 4rpx 12rpx;
  border-radius: 999rpx;
  font-size: 18rpx;
  color: $emo-sage-text;
  background: rgba(237, 250, 243, 0.86);
}

.title {
  display: block;
  margin-top: 10rpx;
  font-size: 28rpx;
  line-height: 1.45;
  color: $emo-text-main;
  font-weight: 700;
}

.meta {
  flex-shrink: 0;
  padding-top: 10rpx;
  font-size: 21rpx;
  color: $emo-text-sub;
}

.empty-state {
  margin-top: 18rpx;
  padding: 20rpx;
  border-radius: 22rpx;
  background: rgba(250, 246, 239, 0.72);
}

.empty-title {
  display: block;
  font-size: 25rpx;
  font-weight: 700;
  color: $emo-text-main;
}

.empty-desc {
  display: block;
  margin-top: 10rpx;
  font-size: 22rpx;
  line-height: 1.5;
  color: $emo-text-sub;
}

.record-list {
  margin-top: 18rpx;
  display: flex;
  flex-direction: column;
  gap: 14rpx;
}

.record-item {
  padding: 18rpx;
  border-radius: 22rpx;
  background: rgba(250, 246, 239, 0.72);
  border: 1rpx solid rgba(255, 255, 255, 0.88);
}

.record-main {
  min-width: 0;
}

.record-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12rpx;
}

.record-mood {
  font-size: 26rpx;
  font-weight: 800;
  color: $emo-text-main;
}

.record-time {
  font-size: 20rpx;
  color: $emo-text-sub;
}

.record-meta {
  margin-top: 10rpx;
  display: flex;
  align-items: center;
  gap: 10rpx;
  flex-wrap: wrap;
}

.source-chip {
  display: inline-flex;
  padding: 4rpx 12rpx;
  border-radius: 999rpx;
  font-size: 20rpx;
  color: $emo-sage-text;
  background: rgba(237, 250, 243, 0.86);
}

.record-tags {
  font-size: 20rpx;
  color: $emo-text-sub;
}

.record-desc {
  display: block;
  margin-top: 10rpx;
  font-size: 23rpx;
  line-height: 1.55;
  color: $emo-text-main;
}

.record-action {
  width: fit-content;
  margin-top: 14rpx;
  padding: 8rpx 16rpx;
  border-radius: 999rpx;
  font-size: 21rpx;
  font-weight: 700;
  color: #ffffff;
  background: linear-gradient(135deg, #5c836f, #3f6d59);
}
</style>
