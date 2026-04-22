import config from '../config/index.js'

const BASE_URL = config.baseUrl + config.apiPrefix

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
                if (res.data.code === 200) {
                    resolve(res.data.data)
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
