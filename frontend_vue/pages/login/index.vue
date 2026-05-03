<template>
  <scroll-view
    class="login-page"
    scroll-y
    :scroll-with-animation="true"
    :style="pageStyle"
  >
    <view class="hero-gradient"></view>

    <view class="login-shell" :style="shellStyle">
      <view class="header-section">
        <view class="illus-box">
          <image src="/static/images/guide/illus-3.png" class="illus-img" mode="aspectFit" />
        </view>
        <view class="main-title">回来看看自己</view>
        <view class="sub-title">登录后继续保存你的情绪线索</view>
      </view>

      <LoginRegisterForm
        @success="handleAuthSuccess"
        @focus="handleInputFocus"
        @blur="handleInputBlur"
      />
      <GuestSection @guest="goGuest" />
    </view>
  </scroll-view>
</template>

<script setup>
import { computed, onBeforeUnmount, ref } from 'vue'
import { onHide, onShow } from '@dcloudio/uni-app'
import { guestApi, loginApi, registerApi } from '@/api/index.js'
import GuestSection from './components/GuestSection.vue'
import LoginRegisterForm from './components/LoginRegisterForm.vue'

const keyboardHeight = ref(0)
let keyboardHeightHandler = null

const pageStyle = computed(() => ({
  height: '100vh',
}))

const shellStyle = computed(() => ({
  paddingBottom: `${keyboardHeight.value + 56}px`,
}))

onShow(() => {
  bindKeyboardHeightChange()
})

onHide(() => {
  keyboardHeight.value = 0
})

onBeforeUnmount(() => {
  unbindKeyboardHeightChange()
})

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
        nickname: data.nickname,
      })
      uni.showToast({ title: '注册成功', icon: 'success' })
    }

    uni.setStorageSync('isLogin', true)
    uni.setStorageSync('user_id', resData.user_id)
    uni.setStorageSync('nickname', resData.nickname || '用户')
    if (typeof uni.$emit === 'function') {
      uni.$emit('nicknameUpdated', resData.nickname || '用户')
    }

    setTimeout(() => {
      uni.switchTab({ url: '/pages/index/index' })
    }, 700)
  } catch (e) {
    if (e && e.isBizError) return
    uni.showModal({
      title: '连接失败',
      content: '当前无法连接服务器，你可以重试，或进入离线体验模式。',
      confirmText: '离线体验',
      cancelText: '重试',
      success: (res) => {
        if (!res.confirm) return
        uni.setStorageSync('isLogin', true)
        uni.setStorageSync('user_id', Date.now())
        uni.setStorageSync('nickname', data.nickname || data.account || '测试用户')
        if (typeof uni.$emit === 'function') {
          uni.$emit('nicknameUpdated', data.nickname || data.account || '测试用户')
        }
        uni.showToast({ title: '已进入离线体验', icon: 'none' })
        setTimeout(() => {
          uni.switchTab({ url: '/pages/index/index' })
        }, 600)
      },
    })
  } finally {
    uni.hideLoading()
  }
}

const goGuest = async () => {
  uni.showLoading({ title: '登录中...' })
  try {
    const res = await guestApi()
    uni.setStorageSync('isLogin', true)
    uni.setStorageSync('user_id', res.user_id)
    uni.setStorageSync('nickname', res.nickname)
    if (typeof uni.$emit === 'function') {
      uni.$emit('nicknameUpdated', res.nickname)
    }
    uni.showToast({ title: '欢迎体验', icon: 'success' })
    setTimeout(() => {
      uni.switchTab({ url: '/pages/index/index' })
    }, 700)
  } catch (e) {
    if (e && e.isBizError) return
    uni.setStorageSync('isLogin', true)
    uni.setStorageSync('user_id', Date.now())
    uni.setStorageSync('nickname', `游客${String(Date.now()).slice(-4)}`)
    if (typeof uni.$emit === 'function') {
      uni.$emit('nicknameUpdated', uni.getStorageSync('nickname'))
    }
    uni.showToast({ title: '已进入体验模式', icon: 'none' })
    setTimeout(() => {
      uni.switchTab({ url: '/pages/index/index' })
    }, 600)
  } finally {
    uni.hideLoading()
  }
}

const bindKeyboardHeightChange = () => {
  if (typeof uni.onKeyboardHeightChange !== 'function' || keyboardHeightHandler) {
    return
  }
  keyboardHeightHandler = ({ height = 0 }) => {
    keyboardHeight.value = height
  }
  uni.onKeyboardHeightChange(keyboardHeightHandler)
}

const unbindKeyboardHeightChange = () => {
  if (typeof uni.offKeyboardHeightChange === 'function' && keyboardHeightHandler) {
    uni.offKeyboardHeightChange(keyboardHeightHandler)
  }
  keyboardHeightHandler = null
}

const handleInputFocus = () => {
  setTimeout(() => {
    if (typeof uni.pageScrollTo === 'function') {
      uni.pageScrollTo({ scrollTop: 240, duration: 180 })
    }
  }, 80)
}

const handleInputBlur = () => {
  setTimeout(() => {
    keyboardHeight.value = 0
  }, 120)
}
</script>

<style lang="scss" scoped>
.login-page {
  min-height: 100vh;
  position: relative;
  overflow: hidden;
  background: $emo-page-bg;
}

.login-shell {
  min-height: 100vh;
  padding: 70rpx 0 56rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-sizing: border-box;
  position: relative;
  z-index: 1;
}

.hero-gradient {
  position: absolute;
  inset: -12%;
  z-index: 0;
  filter: blur(80rpx);
  background: $emo-page-glow;
}

.header-section {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.illus-box {
  width: 380rpx;
  height: 280rpx;
  margin-bottom: 12rpx;
}

.illus-img {
  width: 100%;
  height: 100%;
}

.main-title {
  font-size: 46rpx;
  font-weight: 700;
  color: $emo-text-main;
}

.sub-title {
  margin-top: 8rpx;
  font-size: 27rpx;
  color: $emo-text-sub;
}
</style>
