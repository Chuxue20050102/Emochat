<template>
  <view class="form-card">
    <view class="tab-header">
      <view class="tab-item" :class="{ active: currentTab === 'login' }" @click="switchTab('login')">登录</view>
      <view class="tab-item" :class="{ active: currentTab === 'register' }" @click="switchTab('register')">注册</view>
    </view>
    
    <view class="form-content">
      <view class="form-title" v-if="currentTab === 'login'">欢迎回来</view>
      <view class="form-title" v-else>创建账号</view>

      <view class="input-group">
        <input class="emo-input" v-model="formData.account" placeholder-class="input-placeholder" placeholder="[ 手机号 / 邮箱 ]" />
      </view>

      <view class="input-group">
        <input class="emo-input" v-model="formData.password" placeholder-class="input-placeholder" placeholder="[ 密码 ]" password />
      </view>

      <view class="input-group" v-if="currentTab === 'register'">
        <input class="emo-input" v-model="formData.confirmPassword" placeholder-class="input-placeholder" placeholder="[ 确认密码 ]" password />
      </view>

      <button class="primary-btn" @click="handleSubmit">
        {{ currentTab === 'login' ? '登录' : '注册账号' }}
      </button>

      <view class="form-footer" v-if="currentTab === 'login'">
        <text class="footer-link" @click="switchTab('register')">注册账号</text>
        <text class="divider">|</text>
        <text class="footer-link">忘记密码</text>
      </view>
      <view class="form-footer" v-if="currentTab === 'register'">
        <text class="footer-link" @click="switchTab('login')">已有账号？返回登录</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'

const currentTab = ref('login')
const formData = ref({ account: '', password: '', confirmPassword: '' })

const emit = defineEmits(['success'])

const switchTab = (tab) => {
  currentTab.value = tab
  formData.value = { account: '', password: '', confirmPassword: '' }
}

const validateForm = () => {
  const account = formData.value.account.trim()
  const password = formData.value.password
  const confirmPassword = formData.value.confirmPassword

  if (!account) { uni.showToast({ title: '请输入账号', icon: 'none' }); return false }
  if (!password) { uni.showToast({ title: '请输入密码', icon: 'none' }); return false }

  if (currentTab.value === 'register' && password !== confirmPassword) {
    uni.showToast({ title: '两次输入密码不一致', icon: 'none' }); return false
  }
  return true
}

const handleSubmit = () => {
  if (!validateForm()) return
  emit('success', { type: currentTab.value, data: formData.value })
}
</script>

<style lang="scss" scoped>
.form-card {
  width: 630rpx;
  background-color: #FFFFFF;
  border-radius: 36rpx;
  box-shadow: 0 16rpx 40rpx rgba(0, 0, 0, 0.04);
  padding: 40rpx;
  z-index: 1;
  position: relative;
  margin-top: 60rpx;
}
.tab-header {
  display: flex;
  justify-content: space-around;
  margin-bottom: 50rpx;
  border-bottom: 2rpx solid #F0F0F0;
}
.tab-item {
  font-size: 32rpx;
  color: #888;
  font-weight: 400;
  padding-bottom: 24rpx;
  position: relative;
  flex: 1;
  text-align: center;
  transition: all 0.3s;
}
.tab-item.active {
  color: #1A1A1A;
  font-weight: 600;
}
.tab-item.active::after {
  content: '';
  position: absolute;
  bottom: -2rpx;
  left: 50%;
  transform: translateX(-50%);
  width: 48rpx;
  height: 6rpx;
  background: linear-gradient(90deg, #FF9B8C, #FFB0A4);
  border-radius: 4rpx;
}
.form-title {
  font-size: 32rpx;
  font-weight: 600;
  color: #1A1A1A;
  margin-bottom: 30rpx;
}
.input-group {
  margin-bottom: 30rpx;
}
.emo-input {
  width: 100%;
  height: 90rpx;
  border: 2rpx solid #EAEAEA;
  border-radius: 16rpx;
  padding: 0 30rpx;
  font-size: 28rpx;
  color: #1A1A1A;
  box-sizing: border-box;
  background-color: #FAFAFC;
  transition: border-color 0.3s;
}
.emo-input:focus {
  border-color: #FF9B8C;
  background-color: #FFFFFF;
}
:deep(.input-placeholder) {
  color: #BDBDBD;
  letter-spacing: 2rpx;
}
.primary-btn {
  width: 100%;
  height: 96rpx;
  border-radius: 48rpx;
  background: linear-gradient(135deg, #FF9B8C, #FFB0A4);
  color: #FFF;
  font-size: 32rpx;
  font-weight: 600;
  letter-spacing: 2rpx;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 50rpx;
  box-shadow: 0 12rpx 30rpx rgba(255, 155, 140, 0.35);
  border: none;
  transition: transform 0.2s ease;
}
.primary-btn::after {
  border: none;
}
.primary-btn:active {
  transform: scale(0.97);
}
.form-footer {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 36rpx;
}
.footer-link {
  font-size: 26rpx;
  color: #666;
  padding: 10rpx;
}
.divider {
  margin: 0 16rpx;
  color: #D8D8D8;
  font-size: 24rpx;
}
</style>
