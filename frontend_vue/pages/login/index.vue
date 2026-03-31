<template>
  <view class="login-page">
    <view class="hero-gradient login-bg"></view>

    <!-- 顶部插画与欢迎词区域 -->
    <view class="header-section">
      <view class="illus-box">
        <image src="/static/images/guide/illus-3.png" class="illus-img" mode="aspectFit" />
      </view>
      <view class="main-title">欢迎来到 EmoChat</view>
      <view class="sub-title">一个可以安心表达情绪的地方</view>
    </view>

    <!-- 中部表单区 -->
    <LoginRegisterForm @success="handleAuthSuccess" />

    <!-- 底部体验区 -->
    <GuestSection @guest="goGuest" />
  </view>
</template>

<script setup>
import LoginRegisterForm from './components/LoginRegisterForm.vue'
import GuestSection from './components/GuestSection.vue'
import { loginApi, registerApi, guestApi } from '@/api/index.js'

const handleAuthSuccess = async ({ type, data }) => {
  uni.showLoading({ title: '处理中...' })
  try {
    let resData
    if (type === 'login') {
      resData = await loginApi({ account: data.account, password: data.password })
      uni.showToast({ title: '登录成功', icon: 'success' })
    } else {
      resData = await registerApi({ 
        account: data.account, 
        password: data.password,
        nickname: '新用户_' + data.account.substring(0,4)
      })
      uni.showToast({ title: '注册成功', icon: 'success' })
    }
    
    uni.setStorageSync('isLogin', true)
    uni.setStorageSync('user_id', resData.user_id)
    uni.setStorageSync('nickname', resData.nickname || '用户')
    
    setTimeout(() => {
      uni.switchTab({ url: '/pages/index/index' })
    }, 1000)
  } catch(e) {
    if (e && e.isBizError) {
      // 如果是业务报错（比如密码错、账号重复），就在这里停止，不进入离线模式
      return
    }
    console.warn('[网络或服务器异常，进入离线模式]', e)
    // 开发阶段：后端没启动或连不上时，用本地临时身份跳过
    uni.setStorageSync('isLogin', true)
    uni.setStorageSync('user_id', Date.now())
    uni.setStorageSync('nickname', data.account || '测试用户')
    uni.showToast({ title: '离线模式，本地体验中', icon: 'none' })
    setTimeout(() => {
      uni.switchTab({ url: '/pages/index/index' })
    }, 800)
  } finally {
    uni.hideLoading()
  }
}

const goGuest = async () => {
  uni.showLoading({ title: '游客登录中...' })
  try {
    const res = await guestApi()
    uni.setStorageSync('isLogin', true)
    uni.setStorageSync('user_id', res.user_id)
    uni.setStorageSync('nickname', res.nickname)
    uni.showToast({ title: '已分配游客通道', icon: 'success' })
    setTimeout(() => {
      uni.switchTab({ url: '/pages/index/index' })
    }, 1000)
  } catch(e) {
    if (e && e.isBizError) {
      return
    }
    console.warn('[游客登录失败，进入离线模式]', e)
    // 开发阶段：后端没启动网络连不上时才进入离线
    uni.setStorageSync('isLogin', true)
    uni.setStorageSync('user_id', Date.now())
    uni.setStorageSync('nickname', '游客' + String(Date.now()).slice(-4))
    uni.showToast({ title: '体验模式', icon: 'none' })
    setTimeout(() => {
      uni.switchTab({ url: '/pages/index/index' })
    }, 800)
  } finally {
    uni.hideLoading()
  }
}
</script>

<style lang="scss" scoped>
.login-page {
  min-height: 100vh;
  position: relative;
  background-color: #FAFCFF; /* 轻微偏蓝白的非常干净底色 */
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow: hidden;
  padding-bottom: 60rpx;
}

/* 自然柔和的极光背景 */
.hero-gradient {
  position: absolute;
  top: -10%; left: -10%; right: -10%; bottom: -10%;
  z-index: 0;
  filter: blur(60px);
  background: 
    radial-gradient(circle at 15% 30%, rgba(253, 244, 230, 0.8) 0%, transparent 50%),
    radial-gradient(circle at 85% 20%, rgba(214, 232, 246, 0.8) 0%, transparent 50%),
    radial-gradient(circle at 30% 70%, rgba(251, 235, 252, 0.8) 0%, transparent 50%),
    radial-gradient(circle at 75% 85%, rgba(255, 210, 194, 0.6) 0%, transparent 50%);
  transform: scale(1.1);
  pointer-events: none;
}

/* 顶部区域 */
.header-section {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 100rpx;
  width: 100%;
}
.illus-box {
  width: 380rpx;
  height: 280rpx;
  margin-bottom: 40rpx;
}
.illus-img {
  width: 100%;
  height: 100%;
}
.main-title {
  font-size: 48rpx;
  font-weight: 600;
  color: #1A1A1A;
  margin-bottom: 12rpx;
}
.sub-title {
  font-size: 28rpx;
  color: #666;
}
</style>
