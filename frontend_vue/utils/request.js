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
        console.log(`[Mock] ${key}`, mockResult !== undefined ? '✅' : '⚠️ 无匹配')
        return Promise.resolve(mockResult !== undefined ? mockResult : {})
    }

    const fullUrl = config.baseUrl + url

    return new Promise((resolve, reject) => {
        uni.request({
            url: fullUrl,
            method,
            data,
            timeout: 60000,
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

export const postStream = async (url, data = {}, handlers = {}) => {
    const fullUrl = config.baseUrl + url

    if (typeof fetch !== 'function') {
        throw new Error('stream_not_supported')
    }

    let response
    try {
        response = await fetch(fullUrl, {
            method: 'POST',
            headers: {
                'content-type': 'application/json'
            },
            body: JSON.stringify(data),
            signal: handlers.signal
        })
    } catch (error) {
        if (error?.name === 'AbortError') {
            throw new Error('stream_aborted')
        }
        throw error
    }

    if (!response.ok || !response.body || typeof response.body.getReader !== 'function') {
        throw new Error('stream_not_supported')
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder('utf-8')
    let buffer = ''

    while (true) {
        let result
        try {
            result = await reader.read()
        } catch (error) {
            if (error?.name === 'AbortError') {
                throw new Error('stream_aborted')
            }
            throw error
        }

        const { value, done } = result
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
            const payload = line.trim()
            if (!payload) continue
            let parsed
            try {
                parsed = JSON.parse(payload)
            } catch (error) {
                continue
            }

            if (parsed.type === 'start' && handlers.onStart) {
                handlers.onStart(parsed)
            }
            if (parsed.type === 'delta' && handlers.onDelta) {
                handlers.onDelta(parsed.content || '', parsed)
            }
            if (parsed.type === 'end' && handlers.onEnd) {
                handlers.onEnd(parsed)
            }
        }
    }

    if (buffer.trim()) {
        try {
            const parsed = JSON.parse(buffer.trim())
            if (parsed.type === 'end' && handlers.onEnd) {
                handlers.onEnd(parsed)
            }
        } catch (error) {
            console.warn('stream tail parse failed', error)
        }
    }
}
