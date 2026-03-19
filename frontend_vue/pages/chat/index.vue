<template>
  <view class="container">
    <text class="placeholder">这里是聊天模块，待楚雪开发</text>
    <FloatingTabBar currentTab="chat" />
  </view>
</template>

<script setup>
import { onShow } from '@dcloudio/uni-app'
import FloatingTabBar from '@/components/FloatingTabBar.vue'

onShow(() => {
  uni.hideTabBar({ animation: false })
})
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
.placeholder {
  color: #999;
}
</style>
