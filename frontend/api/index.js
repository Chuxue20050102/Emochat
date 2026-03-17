import { post, get, del } from '../utils/request'

export const registerApi = (data) => post('/api/auth/register', data)
export const loginApi = (data) => post('/api/auth/login', data)
export const guestApi = () => post('/api/auth/guest')

export const recordEmotionApi = (data) => post('/api/emotion/record', data)
export const getCalendarApi = (data) => get('/api/emotion/calendar', data)

export const getUserProfileApi = (data) => get('/api/user/profile', data)
