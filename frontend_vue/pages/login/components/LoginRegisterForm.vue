<template>
  <view class="form-card">
    <view class="tab-header">
      <view class="tab-item" :class="{ active: currentTab === 'login' }" @click="switchTab('login')">登录</view>
      <view class="tab-item" :class="{ active: currentTab === 'register' }" @click="switchTab('register')">注册</view>
    </view>

    <view class="form-content">
      <view class="form-title">{{ currentTab === 'login' ? '欢迎回来' : '创建账号' }}</view>
      <view class="form-subtitle">{{ formSubtitle }}</view>

      <view class="input-group" v-if="currentTab === 'register'">
        <input
          class="emo-input"
          v-model="formData.nickname"
          placeholder-class="input-placeholder"
          placeholder="昵称"
          :adjust-position="false"
          :cursor-spacing="120"
          maxlength="20"
          @focus="emit('focus')"
          @blur="emit('blur')"
        />
      </view>

      <view class="input-group">
        <input
          class="emo-input"
          v-model="formData.account"
          placeholder-class="input-placeholder"
          placeholder="手机号 / 邮箱"
          :adjust-position="false"
          :cursor-spacing="120"
          @focus="emit('focus')"
          @blur="emit('blur')"
        />
      </view>

      <view class="input-group">
        <input
          class="emo-input"
          v-model="formData.password"
          placeholder-class="input-placeholder"
          placeholder="密码"
          password
          :adjust-position="false"
          :cursor-spacing="120"
          @focus="emit('focus')"
          @blur="emit('blur')"
        />
      </view>

      <view class="input-group" v-if="currentTab === 'register'">
        <input
          class="emo-input"
          v-model="formData.confirmPassword"
          placeholder-class="input-placeholder"
          placeholder="确认密码"
          password
          :adjust-position="false"
          :cursor-spacing="120"
          @focus="emit('focus')"
          @blur="emit('blur')"
        />
      </view>

      <button class="emo-btn-primary primary-btn" @click="handleSubmit">
        {{ currentTab === 'login' ? '登录' : '创建账号' }}
      </button>

      <view class="form-footer" v-if="currentTab === 'login'">
        <text class="footer-link" @click="switchTab('register')">快速注册</text>
        <text class="divider">|</text>
        <text class="footer-link">忘记密码</text>
      </view>
      <view class="form-footer" v-else>
        <text class="footer-link" @click="switchTab('login')">已有账号，返回登录</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { computed, ref } from 'vue'

const currentTab = ref('login')
const formData = ref({ account: '', password: '', confirmPassword: '', nickname: '' })
const formSubtitle = computed(() =>
  currentTab.value === 'login'
    ? '继续查看之前留下的记录和陪聊'
    : '创建账号后，你的记录会保存在自己的档案里',
)

const emit = defineEmits(['blur', 'focus', 'success'])

const switchTab = (tab) => {
  currentTab.value = tab
  formData.value = { account: '', password: '', confirmPassword: '', nickname: '' }
}

const validateForm = () => {
  const account = formData.value.account.trim()
  const nickname = formData.value.nickname.trim()
  const password = formData.value.password
  const confirmPassword = formData.value.confirmPassword

  if (currentTab.value === 'register' && !nickname) {
    uni.showToast({ title: '请输入昵称', icon: 'none' })
    return false
  }
  if (currentTab.value === 'register' && nickname.length > 20) {
    uni.showToast({ title: '昵称不能超过20个字符', icon: 'none' })
    return false
  }
  if (!account) {
    uni.showToast({ title: '请输入账号', icon: 'none' })
    return false
  }
  if (!password) {
    uni.showToast({ title: '请输入密码', icon: 'none' })
    return false
  }
  if (currentTab.value === 'register' && password !== confirmPassword) {
    uni.showToast({ title: '两次密码不一致', icon: 'none' })
    return false
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
  margin-top: 44rpx;
  padding: 34rpx;
  border-radius: 36rpx;
  background: rgba(255, 255, 255, 0.78);
  border: 2rpx solid rgba(255, 255, 255, 0.88);
  box-shadow: 0 20rpx 56rpx rgba(43, 55, 93, 0.14);
  backdrop-filter: blur(22rpx);
  z-index: 2;
  box-sizing: border-box;
}

.tab-header {
  display: flex;
  margin-bottom: 34rpx;
  padding: 8rpx;
  border-radius: 999rpx;
  background: rgba(243, 247, 255, 0.84);
}

.tab-item {
  flex: 1;
  height: 62rpx;
  border-radius: 999rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28rpx;
  color: #6f7890;
  transition: all 0.24s ease;
}

.tab-item.active {
  color: #25314f;
  font-weight: 700;
  background: #fff;
  box-shadow: 0 6rpx 16rpx rgba(62, 77, 120, 0.14);
}

.form-title {
  font-size: 34rpx;
  font-weight: 700;
  color: #202a45;
}

.form-subtitle {
  margin-top: 8rpx;
  margin-bottom: 22rpx;
  font-size: 23rpx;
  line-height: 1.45;
  color: #7f8aa0;
}

.input-group {
  margin-bottom: 18rpx;
}

.emo-input {
  width: 100%;
  height: 92rpx;
  border-radius: 18rpx;
  border: 2rpx solid #e0e6f3;
  background: rgba(248, 250, 255, 0.94);
  padding: 0 24rpx;
  box-sizing: border-box;
  font-size: 28rpx;
  color: #25304a;
}

:deep(.input-placeholder) {
  color: #98a2b8;
}

.primary-btn {
  margin-top: 18rpx;
}

.form-footer {
  margin-top: 20rpx;
  display: flex;
  justify-content: center;
  align-items: center;
}

.footer-link {
  font-size: 24rpx;
  color: #667291;
}

.divider {
  margin: 0 12rpx;
  color: #b4bbcd;
  font-size: 22rpx;
}
</style>
