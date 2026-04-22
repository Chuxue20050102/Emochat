<template>
  <view class="chat-page">
    <view class="hero-gradient page-bg"></view>

    <ChatHeader
      :useMemory="useMemory"
      :messageCount="messageCount"
      :isThinking="isThinking || isStreaming"
      @back="goHome"
      @clear="clearConversation"
      @toggle-memory="toggleMemory"
      @archive="archiveConversation"
      @history="showEmotionHistory"
    />

    <view v-if="showQuickPrompts" class="quick-prompts">
      <text class="quick-title">你也可以这样开始</text>
      <view class="quick-list">
        <view
          v-for="item in quickPrompts"
          :key="item"
          class="quick-item"
          @click="sendMessage(item)"
        >
          {{ item }}
        </view>
      </view>
    </view>

    <view class="chat-main">
      <ChatMessageList
        :chatList="chatList"
        :isThinking="isThinking"
        :scrollTopId="scrollTopId"
        :bottomPadding="messageBottomPadding"
        @retry="retryMessage"
      />

      <view class="composer-shell" :style="composerShellStyle">
        <ChatInputArea
          :bottomOffset="keyboardHeight"
          :cursorSpacing="Math.max(keyboardHeight, 20)"
          :disabled="isThinking || isStreaming"
          :isStreaming="isStreaming"
          :placeholder="useMemory ? '和我说说你现在的状态' : '当前是无记忆模式，适合一次性倾诉'"
          @send="sendMessage"
          @stop="stopGeneration"
          @focus="handleInputFocus"
          @blur="handleInputBlur"
        />
      </view>
    </view>
  </view>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, ref } from 'vue'
import { onHide, onShow } from '@dcloudio/uni-app'

import {
  archiveChatApi,
  clearChatHistoryApi,
  getChatHistoryApi,
  getEmotionHistoryFromChatApi,
  sendChatApi,
  sendChatStreamApi,
} from '@/api/index.js'
import ChatHeader from './components/ChatHeader.vue'
import ChatInputArea from './components/ChatInputArea.vue'
import ChatMessageList from './components/ChatMessageList.vue'

const CHAT_MEMORY_SWITCH_KEY = 'chat_memory_enabled'
const TYPEWRITER_TICK_MS = 22

const quickPrompts = [
  '我今天有点累，但一时说不上来为什么',
  '最近情绪有点反复，我想聊聊',
  '我想先吐槽几句，你在吗',
]

const chatList = ref([])
const isThinking = ref(false)
const isStreaming = ref(false)
const scrollTopId = ref('')
const useMemory = ref(true)
const keyboardHeight = ref(0)
const isInputFocused = ref(false)
let keyboardHeightHandler = null

const activeAssistantLocalId = ref('')
let activeStreamController = null
let typewriterTimer = null
let typewriterQueue = ''
let pendingFinalize = null
let streamStoppedByUser = false

const messageCount = computed(() => chatList.value.filter((item) => item.role !== 'system').length)
const showQuickPrompts = computed(() => messageCount.value <= 1 && !isThinking.value && !isStreaming.value)
const userId = computed(() => uni.getStorageSync('user_id') || 1001)
const isKeyboardVisible = computed(() => keyboardHeight.value > 0)
const composerShellStyle = computed(() => ({
  paddingBottom: isKeyboardVisible.value ? '0px' : 'calc(env(safe-area-inset-bottom) + 8rpx)',
}))
const messageBottomPadding = computed(() => {
  const basePadding = isKeyboardVisible.value ? 86 : 28
  return basePadding + keyboardHeight.value
})

const welcomeMessage = () => ({
  localId: createLocalId(),
  role: 'assistant',
  content: '我在这儿，慢慢说就好。今天你最想先讲哪一段？',
  time: getNowTime(),
})

onShow(async () => {
  uni.hideTabBar({ animation: false })
  bindKeyboardHeightChange()
  useMemory.value = uni.getStorageSync(CHAT_MEMORY_SWITCH_KEY) !== false
  await initChatPage()
})

onHide(() => {
  stopGeneration({ silent: true })
  resetKeyboardState()
})

onBeforeUnmount(() => {
  stopGeneration({ silent: true })
  stopTypewriterLoop()
  unbindKeyboardHeightChange()
})

const initChatPage = async () => {
  stopGeneration({ silent: true })
  chatList.value = [welcomeMessage()]

  if (useMemory.value) {
    await loadHistory()
  }

  const context = uni.getStorageSync('pendingChatContext')
  if (context) {
    uni.removeStorageSync('pendingChatContext')
    const contextMsg = buildContextMessage(context)
    if (contextMsg) {
      setTimeout(() => {
        sendMessage(contextMsg, { emotionContext: context })
      }, 250)
    }
  }

  scrollToBottom()
}

const loadHistory = async () => {
  try {
    const res = await getChatHistoryApi({
      user_id: userId.value,
      limit: 120,
    })
    const messages = Array.isArray(res?.messages) ? res.messages : []
    if (messages.length > 0) {
      chatList.value = messages.map((item) => ({
        localId: createLocalId(),
        role: item.role === 'user' ? 'user' : 'assistant',
        content: item.content || '',
        time: getNowTime(),
      }))
      scrollToBottom()
    }
  } catch (error) {
    console.error('加载聊天历史失败', error)
  }
}

const buildContextMessage = (context) => {
  if (!context || !context.emotion) return ''

  let text = `我刚记录了一次情绪：${context.emotion}`
  if (Array.isArray(context.tags) && context.tags.length > 0) {
    text += `，可能和${context.tags.join('、')}有关`
  }
  if (Array.isArray(context.detail) && context.detail.length > 0) {
    text += `，我的感受是${context.detail.join('、')}`
  }
  if (context.content) {
    text += `。我还写了：${context.content}`
  }
  return text
}

const findMessageIndex = (localId) => chatList.value.findIndex((item) => item.localId === localId)

const showCrisisHelp = (payload) => {
  if (!payload?.is_crisis) return
  uni.showModal({
    title: '心理援助提醒',
    content:
      payload?.crisis_help_message ||
      '我感觉到你现在很难受。如果你有伤害自己的想法，请立刻联系身边可信任的人，或拨打当地紧急援助电话。',
    showCancel: false,
  })
}

const getQueuedChars = () => Array.from(typewriterQueue)

const calcTypewriterBatchSize = (queueLength) => {
  if (queueLength > 80) return 6
  if (queueLength > 40) return 4
  if (queueLength > 16) return 3
  return 2
}

const stopTypewriterLoop = () => {
  if (typewriterTimer) {
    clearTimeout(typewriterTimer)
    typewriterTimer = null
  }
}

const finishStreamRender = () => {
  const assistantLocalId = activeAssistantLocalId.value
  if (!assistantLocalId || !pendingFinalize) {
    return
  }

  const idx = findMessageIndex(assistantLocalId)
  if (idx >= 0) {
    const finalContent = pendingFinalize.replyMsg || chatList.value[idx].content || '我在。'
    chatList.value[idx].content = finalContent
    chatList.value[idx].status = pendingFinalize.status || 'done'
    chatList.value[idx].time = getNowTime()
  }

  if (pendingFinalize.toast && !pendingFinalize.silent) {
    uni.showToast({ title: pendingFinalize.toast, icon: 'none' })
  }

  if (pendingFinalize.payload) {
    showCrisisHelp(pendingFinalize.payload)
  }

  pendingFinalize = null
  activeAssistantLocalId.value = ''
  scrollToBottom()
}

const pumpTypewriter = () => {
  const assistantLocalId = activeAssistantLocalId.value
  const idx = findMessageIndex(assistantLocalId)
  const chars = getQueuedChars()

  if (!assistantLocalId || idx < 0) {
    typewriterQueue = ''
    pendingFinalize = null
    stopTypewriterLoop()
    return
  }

  if (chars.length === 0) {
    stopTypewriterLoop()
    finishStreamRender()
    return
  }

  const batchSize = calcTypewriterBatchSize(chars.length)
  const nextChars = chars.slice(0, batchSize)
  typewriterQueue = chars.slice(batchSize).join('')
  chatList.value[idx].content += nextChars.join('')
  chatList.value[idx].time = getNowTime()
  scrollToBottom()
  typewriterTimer = setTimeout(pumpTypewriter, TYPEWRITER_TICK_MS)
}

const ensureTypewriterRunning = () => {
  if (!typewriterTimer) {
    typewriterTimer = setTimeout(pumpTypewriter, TYPEWRITER_TICK_MS)
  }
}

const enqueueAssistantText = (text) => {
  if (!text) return
  typewriterQueue += text
  ensureTypewriterRunning()
}

const finalizeAssistantMessage = ({ replyMsg = '', status = 'done', payload = null, toast = '', silent = false } = {}) => {
  pendingFinalize = {
    payload,
    replyMsg,
    silent,
    status,
    toast,
  }
  if (!typewriterQueue) {
    finishStreamRender()
  }
}

const resetStreamState = () => {
  isThinking.value = false
  isStreaming.value = false
  streamStoppedByUser = false
  activeStreamController = null
}

const createStreamController = () => {
  if (typeof AbortController !== 'function') {
    return null
  }
  return new AbortController()
}

const stopGeneration = ({ silent = false } = {}) => {
  if (!isStreaming.value && !isThinking.value) {
    return
  }

  streamStoppedByUser = true
  isThinking.value = false

  if (activeStreamController) {
    activeStreamController.abort()
  }

  if (activeAssistantLocalId.value) {
    const idx = findMessageIndex(activeAssistantLocalId.value)
    const partialContent = idx >= 0 ? chatList.value[idx].content : ''
    finalizeAssistantMessage({
      replyMsg: partialContent,
      silent,
      status: 'done',
      toast: silent ? '' : '已停止生成',
    })
  } else {
    resetStreamState()
  }
}

const sendMessage = async (text, options = {}) => {
  const message = (text || '').trim()
  if (!message || isThinking.value || isStreaming.value) return

  chatList.value.push({
    localId: createLocalId(),
    role: 'user',
    content: message,
    time: getNowTime(),
  })
  scrollToBottom()

  const requestPayload = {
    user_id: userId.value,
    message,
    card_record_id: options.cardRecordId || null,
    use_memory: useMemory.value,
    emotion_context: options.emotionContext || null,
  }

  const assistantLocalId = createLocalId()
  activeAssistantLocalId.value = assistantLocalId
  typewriterQueue = ''
  pendingFinalize = null
  streamStoppedByUser = false

  chatList.value.push({
    localId: assistantLocalId,
    role: 'assistant',
    content: '',
    status: 'streaming',
    time: '',
  })
  scrollToBottom()

  isThinking.value = true
  isStreaming.value = true
  activeStreamController = createStreamController()

  try {
    let streamFinished = false

    try {
      await sendChatStreamApi(requestPayload, {
        signal: activeStreamController?.signal,
        onStart: () => {
          isThinking.value = true
        },
        onDelta: (chunk) => {
          if (!chunk) return
          isThinking.value = false
          enqueueAssistantText(chunk)
        },
        onEnd: (payload) => {
          streamFinished = true
          isThinking.value = false
          finalizeAssistantMessage({
            payload,
            replyMsg: payload?.reply_msg || '',
            status: 'done',
          })
        },
      })
    } catch (streamError) {
      const isAborted = streamError?.message === 'stream_aborted'
      if (isAborted && streamStoppedByUser) {
        streamFinished = true
      } else {
        const idx = findMessageIndex(assistantLocalId)
        const hasRenderedContent = idx >= 0 && !!chatList.value[idx]?.content
        const hasPendingQueue = !!typewriterQueue

        if (hasRenderedContent || hasPendingQueue) {
          streamFinished = true
          finalizeAssistantMessage({
            replyMsg: hasRenderedContent ? chatList.value[idx].content : '',
            status: 'done',
            toast: '回复中断，已保留当前内容',
          })
        } else {
          isStreaming.value = false
          isThinking.value = true

          const res = await sendChatApi(requestPayload)
          const fallbackIdx = findMessageIndex(assistantLocalId)
          if (fallbackIdx >= 0) {
            chatList.value[fallbackIdx].content = res?.reply_msg || '我在。'
            chatList.value[fallbackIdx].status = 'done'
            chatList.value[fallbackIdx].time = getNowTime()
          } else {
            chatList.value.push({
              localId: createLocalId(),
              role: 'assistant',
              content: res?.reply_msg || '我在。',
              time: getNowTime(),
            })
          }
          showCrisisHelp(res)
          streamFinished = true
          scrollToBottom()
        }
      }
    }

    if (!streamFinished && activeAssistantLocalId.value) {
      const idx = findMessageIndex(activeAssistantLocalId.value)
      const content = idx >= 0 ? chatList.value[idx].content : ''
      finalizeAssistantMessage({
        replyMsg: content,
        status: 'done',
      })
    }
  } catch (error) {
    console.error('发送消息失败', error)
    const idx = findMessageIndex(assistantLocalId)
    if (idx >= 0) {
      chatList.value.splice(idx, 1)
    }
    chatList.value.push({
      localId: createLocalId(),
      role: 'system',
      content: '这条消息发送失败了。',
      status: 'failed',
      retryPayload: {
        message,
        options,
      },
      time: getNowTime(),
    })
    uni.showToast({ title: '网络有点波动，点击重试即可', icon: 'none' })
  } finally {
    resetStreamState()
    scrollToBottom()
  }
}

const retryMessage = async (payload) => {
  if (!payload || isThinking.value || isStreaming.value) return

  const failIndex = chatList.value.findIndex(
    (item) =>
      item.role === 'system' &&
      item.status === 'failed' &&
      item.retryPayload?.message === payload.message,
  )
  if (failIndex >= 0) {
    chatList.value.splice(failIndex, 1)
  }

  await sendMessage(payload.message, payload.options || {})
}

const clearConversation = () => {
  if (isThinking.value || isStreaming.value) return

  if (!useMemory.value) {
    chatList.value = [welcomeMessage()]
    scrollToBottom()
    return
  }

  uni.showModal({
    title: '清空聊天',
    content: '会清空当前账号的聊天记忆，确定继续吗？',
    success: async (result) => {
      if (!result.confirm) return
      try {
        await clearChatHistoryApi({ user_id: userId.value })
        chatList.value = [welcomeMessage()]
        scrollToBottom()
        uni.showToast({ title: '已清空', icon: 'none' })
      } catch (error) {
        console.error('清空聊天失败', error)
        uni.showToast({ title: '清空失败，请稍后再试', icon: 'none' })
      }
    },
  })
}

const toggleMemory = async (enabled) => {
  if (isThinking.value || isStreaming.value) return

  useMemory.value = !!enabled
  uni.setStorageSync(CHAT_MEMORY_SWITCH_KEY, useMemory.value)

  if (useMemory.value) {
    await initChatPage()
    uni.showToast({ title: '已开启记忆模式', icon: 'none' })
  } else {
    chatList.value = [welcomeMessage()]
    scrollToBottom()
    uni.showToast({ title: '已切换为无记忆模式', icon: 'none' })
  }
}

const archiveConversation = async () => {
  if (isThinking.value || isStreaming.value) return
  try {
    const res = await archiveChatApi({
      user_id: userId.value,
      max_messages: 40,
    })
    if (res?.record_id) {
      uni.showToast({ title: '已归档到情绪档案', icon: 'none' })
      chatList.value.push({
        localId: createLocalId(),
        role: 'system',
        content: `已生成情绪档案：${res.mood} · ${res.summary}`,
        time: getNowTime(),
      })
      scrollToBottom()
    } else {
      uni.showToast({ title: '暂无可归档聊天内容', icon: 'none' })
    }
  } catch (error) {
    console.error('归档失败', error)
    uni.showToast({ title: '归档失败，请稍后再试', icon: 'none' })
  }
}

const showEmotionHistory = async () => {
  if (isThinking.value || isStreaming.value) return
  try {
    const res = await getEmotionHistoryFromChatApi({
      user_id: userId.value,
      limit: 8,
    })
    const records = Array.isArray(res?.records) ? res.records : []
    if (records.length === 0) {
      uni.showToast({ title: '暂无历史情绪记录', icon: 'none' })
      return
    }
    const text = records
      .map((r) => `${r.record_date} ${r.mood}${r.tags ? `（${r.tags}）` : ''}`)
      .join('\n')
    chatList.value.push({
      localId: createLocalId(),
      role: 'system',
      content: `历史情绪记录：\n${text}`,
      time: getNowTime(),
    })
    scrollToBottom()
  } catch (error) {
    console.error('查询历史情绪失败', error)
    uni.showToast({ title: '查询失败，请稍后再试', icon: 'none' })
  }
}

const handleInputFocus = () => {
  isInputFocused.value = true
  scrollToBottom()
}

const handleInputBlur = () => {
  isInputFocused.value = false
  setTimeout(() => {
    scrollToBottom()
  }, 80)
}

const bindKeyboardHeightChange = () => {
  if (typeof uni.onKeyboardHeightChange !== 'function' || keyboardHeightHandler) {
    return
  }
  keyboardHeightHandler = ({ height = 0 }) => {
    keyboardHeight.value = height
    if (height > 0 || isInputFocused.value) {
      scrollToBottom()
    }
  }
  uni.onKeyboardHeightChange(keyboardHeightHandler)
}

const unbindKeyboardHeightChange = () => {
  if (typeof uni.offKeyboardHeightChange === 'function' && keyboardHeightHandler) {
    uni.offKeyboardHeightChange(keyboardHeightHandler)
  }
  keyboardHeightHandler = null
}

const resetKeyboardState = () => {
  keyboardHeight.value = 0
  isInputFocused.value = false
}

const goHome = () => {
  uni.switchTab({ url: '/pages/index/index' })
}

const getNowTime = () => {
  const date = new Date()
  const hh = String(date.getHours()).padStart(2, '0')
  const mm = String(date.getMinutes()).padStart(2, '0')
  return `${hh}:${mm}`
}

const createLocalId = () => `${Date.now()}_${Math.random().toString(36).slice(2, 7)}`

const scrollToBottom = async () => {
  await nextTick()
  scrollTopId.value = ''
  setTimeout(() => {
    scrollTopId.value = 'scroll-bottom'
  }, 30)
}
</script>

<style lang="scss" scoped>
.chat-page {
  height: 100vh;
  min-height: 100vh;
  position: relative;
  background-color: $emo-bg-base;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-main {
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
  position: relative;
  z-index: 1;
}

.hero-gradient {
  position: absolute;
  top: -10%;
  left: -10%;
  right: -10%;
  bottom: -10%;
  z-index: 0;
  filter: blur(60px);
  background:
    radial-gradient(circle at 14% 22%, rgba(255, 204, 162, 0.38) 0%, transparent 45%),
    radial-gradient(circle at 84% 28%, rgba(255, 170, 184, 0.35) 0%, transparent 45%),
    radial-gradient(circle at 28% 78%, rgba(198, 232, 250, 0.42) 0%, transparent 48%),
    radial-gradient(circle at 72% 86%, rgba(159, 221, 193, 0.34) 0%, transparent 48%);
  transform: scale(1.08);
  pointer-events: none;
}

.quick-prompts {
  z-index: 2;
  padding: 0 26rpx 4rpx;
}

.quick-title {
  font-size: 20rpx;
  color: #70798a;
}

.quick-list {
  margin-top: 8rpx;
  display: flex;
  gap: 8rpx;
  flex-wrap: wrap;
}

.quick-item {
  padding: 10rpx 16rpx;
  border-radius: 999rpx;
  background: rgba(255, 255, 255, 0.75);
  border: 1rpx solid rgba(255, 255, 255, 0.85);
  color: #3d4a61;
  font-size: 22rpx;
}

.composer-shell {
  position: relative;
  z-index: 2;
  transition: padding-bottom 0.22s ease;
}
</style>
