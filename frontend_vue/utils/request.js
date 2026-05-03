import config from '../config/index.js'

const MOCK_MODE = false

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
}

export const request = (url, method = 'GET', data = {}) => {
    if (MOCK_MODE) {
        const key = `${method} ${url.split('?')[0]}`
        const mockResult = MOCK_DATA[key]
        return Promise.resolve(mockResult !== undefined ? mockResult : {})
    }

    const fullUrl = config.baseUrl + url

    return new Promise((resolve, reject) => {
        uni.request({
            url: fullUrl,
            method,
            data,
            timeout: 120000,
            header: {
                'content-type': 'application/json'
            },
            success: (res) => {
                const responseData = res.data
                if (responseData.code === 200) {
                    resolve(responseData.data)
                } else {
                    uni.showToast({ title: responseData.msg || '请求失败', icon: 'none' })
                    reject({ isBizError: true, msg: responseData.msg })
                }
            },
            fail: (err) => {
                uni.showToast({ title: '网络无法连接到服务器', icon: 'none' })
                reject({ isBizError: false, err })
            }
        })
    })
}

export const get = (url, data) => request(url, 'GET', data)
export const post = (url, data) => request(url, 'POST', data)
export const del = (url, data) => request(url, 'DELETE', data)
