<template>
  <view class="chat-page">
    <view class="hero-gradient page-bg"></view>

    <ChatHeader
      :useMemory="useMemory"
      :messageCount="messageCount"
      :isThinking="isThinking || isStreaming"
      :isArchiving="isArchiving"
      @back="goHome"
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
        @archive="archiveConversation"
        @retry="retryMessage"
      />

      <view class="composer-shell" :style="composerShellStyle">
        <view v-if="agentInsight" class="agent-process">
          <view class="process-dot"></view>
          <text class="process-text">{{ agentInsight }}</text>
        </view>
        <ChatInputArea
          :archiveDisabled="isArchiving"
          :bottomOffset="keyboardHeight"
          :cursorSpacing="Math.max(keyboardHeight, 20)"
          :disabled="isThinking || isStreaming"
          :isStreaming="isStreaming"
          :placeholder="useMemory ? '想说多少都可以，我在' : '这次轻轻聊，不留下新记忆'"
          :showArchiveAction="showArchiveDock"
          @archive="archiveConversation"
          @send="sendMessage"
          @stop="stopGeneration"
          @focus="handleInputFocus"
          @blur="handleInputBlur"
        />
      </view>
    </view>

    <view v-if="showHistoryPanel" class="panel-mask" @click="closeHistoryPanel">
      <view class="history-panel" @click.stop>
        <view class="panel-handle"></view>
        <view class="panel-head">
          <view>
            <text class="panel-title">最近留下的线索</text>
            <text class="panel-subtitle">最近 8 条，来自聊天和手动记录</text>
          </view>
          <view class="panel-close" @click="closeHistoryPanel">关闭</view>
        </view>

        <scroll-view class="history-list" scroll-y="true">
          <view v-if="historyRecords.length === 0" class="history-empty">
            <text class="empty-title">这里会放你愿意留下的情绪线索</text>
            <text class="empty-desc">你可以先聊一会儿，或记录一次心情。之后保存下来的内容会慢慢出现在这里。</text>
          </view>
          <view v-for="item in historyRecords" :key="item.id" class="history-item">
            <view class="history-main">
              <text class="history-mood">{{ item.mood }}</text>
              <text class="history-date">{{ item.created_at || item.record_date }}</text>
            </view>
            <text v-if="item.source" class="history-source">{{ historySourceLabelMap[item.source] || '手动记录' }}</text>
            <text v-if="item.tags" class="history-tags">{{ item.tags }}</text>
            <text v-if="item.description" class="history-desc">{{ item.description }}</text>
            <view class="history-action" @click="chatWithHistoryRecord(item)">继续聊</view>
          </view>
        </scroll-view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { computed, onBeforeUnmount, ref } from 'vue'
import { onHide, onShow } from '@dcloudio/uni-app'

import {
  archiveChatApi,
  clearChatHistoryApi,
  getChatHistoryApi,
  getEmotionHistoryFromChatApi,
  runAgentApi,
} from '@/api/index.js'
import ChatHeader from './components/ChatHeader.vue'
import ChatInputArea from './components/ChatInputArea.vue'
import ChatMessageList from './components/ChatMessageList.vue'

const CHAT_MEMORY_SWITCH_KEY = 'chat_memory_enabled'

const quickPrompts = [
  '我想被听一会儿',
  '陪我慢慢理清楚',
  '看看最近的我',
]

const chatList = ref([])
const isThinking = ref(false)
const isStreaming = ref(false)
const isArchiving = ref(false)
const scrollTopId = ref('')
const useMemory = ref(true)
const keyboardHeight = ref(0)
const isInputFocused = ref(false)
const continueTopicText = ref('')
const agentInsight = ref('')
const showHistoryPanel = ref(false)
const historyRecords = ref([])
const hasSavedContextMessage = ref(false)
const historySourceLabelMap = {
  manual: '手动记录',
  chat: '聊天保存',
}
let keyboardHeightHandler = null

const messageCount = computed(() => chatList.value.filter((item) => item.role !== 'system').length)
const showQuickPrompts = computed(() => messageCount.value <= 1 && !isThinking.value && !isStreaming.value)
const userMessageCount = computed(() => chatList.value.filter((item) => item.role === 'user').length)
const unsavedUserMessageCount = computed(
  () => chatList.value.filter((item) => item.role === 'user' && !item.fromSavedRecord).length,
)
const showArchiveDock = computed(
  () =>
    unsavedUserMessageCount.value >= 1 &&
    !isThinking.value &&
    !isStreaming.value &&
    !isArchiving.value,
)
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
  content: '我在这里。你不用一下子说清楚，想到哪里就先说到哪里。',
  time: getNowTime(),
})

const promptMessageMap = {
  我想被听一会儿: '我现在有些感受想说出来，你先听我说就好。',
  陪我慢慢理清楚: '我现在有点乱，想请你陪我把事情和感受慢慢理清楚。',
  看看最近的我: '帮我看看最近的情绪状态怎么样，可以结合我的历史记录。',
}

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
  unbindKeyboardHeightChange()
})

const initChatPage = async () => {
  stopGeneration({ silent: true })
  chatList.value = [welcomeMessage()]
  continueTopicText.value = ''
  agentInsight.value = ''
  hasSavedContextMessage.value = false

  if (useMemory.value) {
    await loadHistory()
  }

  const context = uni.getStorageSync('pendingChatContext')
  if (context) {
    uni.removeStorageSync('pendingChatContext')
    const contextMsg = buildContextMessage(context)
    if (contextMsg) {
      hasSavedContextMessage.value = true
      setTimeout(() => {
        sendMessage(contextMsg, { emotionContext: context, fromSavedRecord: true })
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
      continueTopicText.value = extractLastUserTopic(messages)
      chatList.value = messages.map((item) => ({
        localId: createLocalId(),
        role: item.role === 'user' ? 'user' : 'assistant',
        content: item.content || '',
        time: formatHistoryTime(item.created_at || item.time || ''),
      }))
      scrollToBottom()
    }
  } catch (error) {
    console.error('加载聊天历史失败', error)
  }
}

const normalizeTopicText = (text) =>
  String(text || '')
    .replace(/\s+/g, ' ')
    .replace(/[。！？?，,；;]+$/g, '')
    .trim()

const extractLastUserTopic = (messages) => {
  const lastUserMessage = [...(messages || [])]
    .reverse()
    .find((item) => item?.role === 'user' && String(item?.content || '').trim().length > 3)
  if (!lastUserMessage) return ''
  return normalizeTopicText(lastUserMessage.content)
}

const buildContextMessage = (context) => {
  if (context?.type === 'profile_insight') {
    const parts = [`我想聊聊档案页里的${context.title || 'AI 近况总结'}。`]
    if (context.summary) parts.push(`总结里写到：${context.summary}`)
    if (context.suggestion) parts.push(`给我的建议是：${context.suggestion}`)
    if (context.overview) parts.push(`这个月的数字是：${context.overview}。`)
    parts.push('请你陪我一起看看，这些信息可能在提醒我什么。')
    return parts.join('')
  }

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

const stopGeneration = ({ silent = false } = {}) => {
  if (!isStreaming.value && !isThinking.value) return
  isThinking.value = false
  isStreaming.value = false
  agentInsight.value = ''
  if (!silent) {
    uni.showToast({ title: '已停止', icon: 'none' })
  }
}

const sendMessage = async (text, options = {}) => {
  const message = (promptMessageMap[text] || text || '').trim()
  if (!message || isThinking.value || isStreaming.value) return
  continueTopicText.value = normalizeTopicText(message)
  agentInsight.value = '正在陪你整理'

  chatList.value.push({
    localId: createLocalId(),
    role: 'user',
    content: message,
    fromSavedRecord: !!options.fromSavedRecord,
    time: getNowTime(),
  })
  scrollToBottom()

  isThinking.value = true
  isStreaming.value = true

  try {
    agentInsight.value = '正在认真读你说的话'
    const agentRes = await runAgentApi({
      user_id: userId.value,
      message,
      use_memory: useMemory.value,
      history_limit: 8,
      archive_max_messages: 40,
      card_record_id: options.cardRecordId || null,
      emotion_context: options.emotionContext || null,
      skip_emotion_review: !!(options.emotionContext?.skip_emotion_review),
    })

    if (agentRes?.intent === 'safety') {
      chatList.value.push({
        localId: createLocalId(),
        role: 'assistant',
        content: agentRes.reply,
        agent: false,
        status: 'done',
        time: getNowTime(),
      })
      showCrisisHelp({ is_crisis: true, crisis_help_message: agentRes.reply })
      agentInsight.value = ''
      scrollToBottom()
      return
    }

    const tools = Array.isArray(agentRes?.tool_calls) ? agentRes.tool_calls : []
    const toolNames = tools.map((item) => item.name).filter(Boolean)
    const usedHistoryContext = toolNames.includes('get_emotion_history') || !!options.fromSavedRecord
    const toolText = toolNames.map(formatToolName).filter(Boolean).join('、')
    if (toolText) {
      agentInsight.value = `正在${toolText}`
      await waitForProcessText()
    } else {
      agentInsight.value = '正在把回应说得更清楚'
      await waitForProcessText()
    }

    chatList.value.push({
      localId: createLocalId(),
      role: 'assistant',
      content: agentRes?.reply || '我在。',
      agent: usedHistoryContext,
      status: 'done',
      time: getNowTime(),
    })
    agentInsight.value = ''

    scrollToBottom()
  } catch (error) {
    console.error('发送消息失败', error)
    agentInsight.value = ''
    chatList.value.push({
      localId: createLocalId(),
      role: 'system',
      content: '这条消息刚刚没送出去。',
      status: 'failed',
      retryPayload: {
        message,
        options,
      },
      time: getNowTime(),
    })
    uni.showToast({ title: '网络有点波动，可以点重试', icon: 'none' })
  } finally {
    isThinking.value = false
    isStreaming.value = false
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
      agentInsight.value = ''
      showHistoryPanel.value = false
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
        agentInsight.value = ''
        showHistoryPanel.value = false
        scrollToBottom()
        uni.showToast({ title: '已清空', icon: 'none' })
      } catch (error) {
        console.error('清空聊天失败', error)
        uni.showToast({ title: '清空失败，请稍后再试', icon: 'none' })
      }
    },
  })
}

const formatToolName = (name) => {
  const map = {
    archive_chat_to_emotion: '把这段感受收进档案',
    get_emotion_history: '参考你留下的线索',
    chat_reply: '结合记忆组织回复',
  }
  return map[name] || ''
}

const waitForProcessText = () =>
  new Promise((resolve) => {
    setTimeout(resolve, 260)
  })

const toggleMemory = async (enabled) => {
  if (isThinking.value || isStreaming.value) return

  useMemory.value = !!enabled
  uni.setStorageSync(CHAT_MEMORY_SWITCH_KEY, useMemory.value)

  if (useMemory.value) {
    await initChatPage()
    uni.showToast({ title: '我会继续参考你留下的线索', icon: 'none' })
  } else {
    chatList.value = [welcomeMessage()]
    agentInsight.value = ''
    showHistoryPanel.value = false
    scrollToBottom()
    uni.showToast({ title: '这次就轻轻聊，不留下新线索', icon: 'none' })
  }
}

const archiveConversation = async () => {
  if (isThinking.value || isStreaming.value || isArchiving.value) return
  if (unsavedUserMessageCount.value === 0) {
    uni.showToast({
      title: hasSavedContextMessage.value ? '这条感受已经在档案里了' : '先说几句，再把它留下来',
      icon: 'none',
    })
    return
  }

  chatList.value = chatList.value.filter((item) => item.type !== 'archive_suggestion')
  const archiveLocalId = createLocalId()
  isArchiving.value = true
  agentInsight.value = '正在把这段感受收好'
  chatList.value.push({
    localId: archiveLocalId,
    role: 'system',
    content: '正在把这段感受收进档案...',
    status: 'streaming',
    time: getNowTime(),
  })
  scrollToBottom()

  try {
    const res = await archiveChatApi({
      user_id: userId.value,
      max_messages: 30,
    })
    const archiveIndex = findMessageIndex(archiveLocalId)
    if (res?.record_id) {
      uni.showToast({ title: '已经帮你留下来了', icon: 'none' })
      if (archiveIndex >= 0) {
        chatList.value[archiveIndex].content = `我已经帮你留下来了：${res.mood} · ${res.summary}`
        chatList.value[archiveIndex].status = 'done'
      }
      agentInsight.value = '这段感受已经留下'
      scrollToBottom()
    } else {
      if (archiveIndex >= 0) {
        chatList.value[archiveIndex].content = '暂无可保存的聊天内容'
        chatList.value[archiveIndex].status = 'done'
      }
      agentInsight.value = ''
      uni.showToast({ title: '暂无可保存内容', icon: 'none' })
    }
  } catch (error) {
    console.error('保存失败', error)
    const archiveIndex = findMessageIndex(archiveLocalId)
    if (archiveIndex >= 0) {
      chatList.value[archiveIndex].content = '保存失败，请稍后再试'
      chatList.value[archiveIndex].status = 'failed'
    }
    agentInsight.value = ''
    uni.showToast({ title: '保存失败，请稍后再试', icon: 'none' })
  } finally {
    isArchiving.value = false
    scrollToBottom()
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
      historyRecords.value = []
      showHistoryPanel.value = true
      return
    }
    historyRecords.value = records
    showHistoryPanel.value = true
  } catch (error) {
    console.error('查询历史情绪失败', error)
    uni.showToast({ title: '查询失败，请稍后再试', icon: 'none' })
  }
}

const closeHistoryPanel = () => {
  showHistoryPanel.value = false
}

const chatWithHistoryRecord = (record) => {
  if (!record || isThinking.value || isStreaming.value) return
  showHistoryPanel.value = false
  const context = {
    emotion: record.mood || '',
    tags: String(record.tags || '')
      .split(',')
      .map((item) => item.trim())
      .filter(Boolean),
    detail: [],
    content: record.description || '',
    recordDate: record.record_date || String(record.created_at || '').slice(0, 10),
  }
  const message = buildContextMessage(context)
  if (message) {
    sendMessage(message, { emotionContext: context, fromSavedRecord: true })
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

const formatHistoryTime = (value) => {
  if (!value) return ''
  const text = String(value)
  const timeMatch = text.match(/(\d{1,2}):(\d{2})/)
  if (timeMatch) {
    return `${timeMatch[1].padStart(2, '0')}:${timeMatch[2]}`
  }
  const parsed = new Date(text)
  if (Number.isNaN(parsed.getTime())) return ''
  const hh = String(parsed.getHours()).padStart(2, '0')
  const mm = String(parsed.getMinutes()).padStart(2, '0')
  return `${hh}:${mm}`
}

const createLocalId = () => `${Date.now()}_${Math.random().toString(36).slice(2, 7)}`

let scrollTimer = 0
const scrollToBottom = () => {
  if (scrollTimer) clearTimeout(scrollTimer)
  scrollTimer = setTimeout(() => {
    scrollTopId.value = ''
    setTimeout(() => {
      scrollTopId.value = 'scroll-bottom'
    }, 50)
    scrollTimer = 0
  }, 100)
}
</script>

<style lang="scss" scoped>
.chat-page {
  height: 100vh;
  min-height: 100vh;
  position: relative;
  background: $emo-page-bg;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-page::after {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: calc(env(safe-area-inset-bottom) + 180rpx);
  z-index: 0;
  background: linear-gradient(180deg, rgba(247, 239, 232, 0), #f7efe8 42%, #f7efe8 100%);
  pointer-events: none;
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
  filter: blur(56px);
  background: $emo-page-glow;
  transform: scale(1.08);
  pointer-events: none;
}

.quick-prompts {
  z-index: 2;
  padding: 2rpx 26rpx 14rpx;
}

.quick-title {
  padding-left: 2rpx;
  font-size: 20rpx;
  color: #8a766a;
}

.quick-list {
  margin-top: 10rpx;
  display: flex;
  gap: 10rpx;
  flex-wrap: wrap;
}

.quick-item {
  padding: 13rpx 18rpx;
  border-radius: 20rpx;
  background: rgba(255, 255, 255, 0.66);
  border: 1rpx solid rgba(255, 255, 255, 0.86);
  color: #554941;
  font-size: 22rpx;
  box-shadow: 0 14rpx 32rpx rgba(71, 52, 38, 0.07);
}

.composer-shell {
  position: relative;
  z-index: 2;
  background: linear-gradient(180deg, rgba(255, 250, 243, 0), #f7efe8 45%, #f7efe8 100%);
  transition: padding-bottom 0.22s ease;
}

.agent-process {
  width: fit-content;
  max-width: calc(100% - 52rpx);
  margin: 0 26rpx 10rpx;
  padding: 10rpx 16rpx;
  border-radius: 999rpx;
  display: flex;
  align-items: center;
  gap: 9rpx;
  color: #5d6f62;
  background: rgba(237, 251, 244, 0.9);
  border: 1rpx solid rgba(183, 226, 203, 0.82);
  box-shadow: 0 12rpx 28rpx rgba(63, 109, 89, 0.1);
}

.process-dot {
  width: 10rpx;
  height: 10rpx;
  border-radius: 50%;
  background: #5c836f;
  animation: processPulse 1.2s ease-in-out infinite;
}

.process-text {
  min-width: 0;
  font-size: 21rpx;
  font-weight: 700;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

@keyframes processPulse {
  0%,
  100% {
    opacity: 0.45;
    transform: scale(0.82);
  }

  50% {
    opacity: 1;
    transform: scale(1);
  }
}

.panel-mask {
  position: fixed;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  z-index: 20;
  display: flex;
  align-items: flex-end;
  background: rgba(47, 41, 37, 0.28);
}

.history-panel {
  width: 100%;
  max-height: 68vh;
  padding: 14rpx 24rpx calc(env(safe-area-inset-bottom) + 28rpx);
  border-radius: 34rpx 34rpx 0 0;
  background:
    linear-gradient(180deg, rgba(255, 253, 249, 0.98), rgba(250, 243, 236, 0.98));
  box-shadow: 0 -24rpx 60rpx rgba(64, 48, 36, 0.18);
}

.panel-handle {
  width: 70rpx;
  height: 8rpx;
  margin: 0 auto 22rpx;
  border-radius: 999rpx;
  background: rgba(153, 132, 117, 0.36);
}

.panel-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 18rpx;
  margin-bottom: 18rpx;
}

.panel-title {
  display: block;
  font-size: 32rpx;
  font-weight: 800;
  color: #2f2925;
}

.panel-subtitle {
  display: block;
  margin-top: 6rpx;
  font-size: 22rpx;
  color: #8a766a;
}

.panel-close {
  flex-shrink: 0;
  padding: 10rpx 18rpx;
  border-radius: 999rpx;
  font-size: 22rpx;
  color: #5d6f62;
  background: rgba(237, 251, 244, 0.86);
}

.history-list {
  max-height: 50vh;
}

.history-empty {
  padding: 28rpx 18rpx 34rpx;
  border-radius: 24rpx;
  background: rgba(255, 255, 255, 0.64);
  border: 1rpx solid rgba(255, 255, 255, 0.82);
}

.empty-title {
  display: block;
  font-size: 27rpx;
  font-weight: 800;
  color: #365f4d;
}

.empty-desc {
  display: block;
  margin-top: 10rpx;
  font-size: 23rpx;
  line-height: 1.5;
  color: #7a6b62;
}

.history-item {
  margin-bottom: 12rpx;
  padding: 18rpx;
  border-radius: 24rpx;
  background: rgba(255, 255, 255, 0.74);
  border: 1rpx solid rgba(255, 255, 255, 0.86);
}

.history-main {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16rpx;
}

.history-mood {
  font-size: 26rpx;
  font-weight: 800;
  color: #365f4d;
}

.history-date {
  font-size: 20rpx;
  color: #9a897d;
}

.history-tags {
  display: block;
  margin-top: 8rpx;
  font-size: 21rpx;
  color: #6c7c72;
}

.history-source {
  display: inline-flex;
  width: fit-content;
  margin-top: 8rpx;
  padding: 4rpx 12rpx;
  border-radius: 999rpx;
  font-size: 20rpx;
  color: #476256;
  background: rgba(237, 251, 244, 0.86);
}

.history-desc {
  display: block;
  margin-top: 8rpx;
  font-size: 23rpx;
  line-height: 1.45;
  color: #5b4f47;
}

.history-action {
  display: inline-flex;
  align-items: center;
  width: fit-content;
  margin-top: 14rpx;
  padding: 7rpx 16rpx;
  border-radius: 999rpx;
  font-size: 21rpx;
  font-weight: 700;
  color: #3f6d59;
  background: rgba(237, 250, 243, 0.92);
  border: 1rpx solid rgba(92, 131, 111, 0.2);
}
</style>
