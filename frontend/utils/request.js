/**
 * 🔧 全局请求工具
 * 
 * MOCK_MODE = true  → 所有请求走本地假数据，不连后端（当前开发阶段）
 * MOCK_MODE = false → 正式连接后端 API
 */
const BASE_URL = 'http://127.0.0.1:8000'
const MOCK_MODE = true   // ← 后端跑通后改成 false 即可

// ============ 假数据仓库 ============
const MOCK_DATA = {
    'POST /api/auth/login': { user_id: 1001, nickname: '测试用户' },
    'POST /api/auth/register': { user_id: 1002, nickname: '新用户' },
    'POST /api/auth/guest': { user_id: 9999, nickname: '游客小星星' },
    'POST /api/emotion/record': { record_id: 1 },
    'GET /api/emotion/calendar': {
        '2026-03-01': '愉快', '2026-03-05': '平静', '2026-03-10': '低落',
        '2026-03-12': '极好', '2026-03-14': '轻松', '2026-03-17': '愉快'
    },
    'GET /api/emotion/detail': [],
    'GET /api/user/profile': { nickname: '测试用户', total_records: 6 },
    'POST /api/chat/send': { reply_msg: '我听到你了，一切都会好起来的。（Mock）', is_crisis: false },
    'GET /api/chat/history': [],
    'DELETE /api/chat/history': null,
}

export const request = (url, method = 'GET', data = {}) => {
    // Mock 模式：直接返回假数据，0延迟
    if (MOCK_MODE) {
        const key = `${method} ${url.split('?')[0]}`
        const mockResult = MOCK_DATA[key]
        console.log(`[Mock] ${key}`, mockResult !== undefined ? '✅' : '⚠️ 无匹配')
        return Promise.resolve(mockResult !== undefined ? mockResult : {})
    }

    // 正式模式：真实请求后端
    return new Promise((resolve, reject) => {
        uni.request({
            url: BASE_URL + url,
            method,
            data,
            timeout: 5000,
            header: {
                'content-type': 'application/json'
            },
            success: (res) => {
                const responseData = res.data
                if (responseData.code === 200) {
                    resolve(responseData.data)
                } else {
                    uni.showToast({ title: responseData.msg || '请求失败', icon: 'none' })
                    reject(responseData.msg)
                }
            },
            fail: (err) => {
                uni.showToast({ title: '网络无法连接到本地服务器', icon: 'none' })
                reject(err)
            }
        })
    })
}

export const get = (url, data) => request(url, 'GET', data)
export const post = (url, data) => request(url, 'POST', data)
export const del = (url, data) => request(url, 'DELETE', data)
