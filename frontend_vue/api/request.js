// api/request.js
// 这是最简单的封装版本，给所有组员发请求用的

const BASE_URL = 'http://127.0.0.1:8000/api'

export function request(options) {
    return new Promise((resolve, reject) => {
        uni.request({
            url: BASE_URL + options.url,
            method: options.method || 'GET',
            data: options.data || {},
            header: {
                'content-type': 'application/json',
            },
            success: (res) => {
                // 请求成功
                if (res.data.code === 200) {
                    resolve(res.data.data) // 直接把那层 data 剥出来给页面
                } else {
                    uni.showToast({ title: res.data.msg || '请求错误', icon: 'none' })
                    reject(res.data.msg)
                }
            },
            fail: (err) => {
                uni.showToast({ title: '网络连接失败，请检查后端', icon: 'none' })
                reject(err)
            }
        })
    })
}
