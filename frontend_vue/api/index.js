import { post, get, del } from '../utils/request'

export const registerApi = (data) => post('/api/auth/register', data)
export const loginApi = (data) => post('/api/auth/login', data)
export const guestApi = () => post('/api/auth/guest')

export const getEmotionTagsApi = () => get('/api/emotion/tags', {})
export const recordEmotionApi = (data) => post('/api/emotion/record', data)
export const getCalendarApi = (data) => get('/api/emotion/calendar', data)
export const getEmotionInsightsApi = (data) => get('/api/emotion/insights', data)
export const getEmotionDetailApi = (data) => get('/api/emotion/detail', data)
export const getEmotionHistoryApi = (data) => get('/api/emotion/history', data)

export const getUserProfileApi = (data) => get('/api/user/profile', data)
export const updateNicknameApi = (data) => post('/api/user/nickname', data)

export const getChatHistoryApi = (data) => get('/api/chat/history', data)
export const clearChatHistoryApi = (data) => del('/api/chat/history', data)
export const archiveChatApi = (data) => post('/api/chat/archive', data)
export const getEmotionHistoryFromChatApi = (data) => get('/api/chat/emotion-history', data)

export const runAgentApi = (data) => post('/api/agent/run', data)

export const getGreetingApi = () => get('/api/common/greeting', { _t: Date.now() })
export const getHomeCopyApi = (data) => get('/api/common/home-copy', data)
