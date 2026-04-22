const LOCAL_IP = '172.20.10.3'
const LOCAL_PORT = '8000'

const isH5 = typeof window !== 'undefined' && window.location
const isDev = process.env.NODE_ENV === 'development'

let baseUrl = ''

if (isH5 && isDev) {
    baseUrl = ''
} else if (isDev) {
    baseUrl = `http://${LOCAL_IP}:${LOCAL_PORT}`
}

const config = {
    baseUrl: baseUrl,
    apiPrefix: '/api',
    localIp: LOCAL_IP,
    localPort: LOCAL_PORT
}

export default config

export function getLocalIp() {
    return LOCAL_IP
}

export function setLocalIp(ip) {
    config.baseUrl = `http://${ip}:${LOCAL_PORT}`
    config.localIp = ip
}
