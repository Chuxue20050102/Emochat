const LOCAL_IP = 'x9bff6ca.natappfree.cc'
const LOCAL_PORT = ''

// Default keeps native/app environments on natapp.
let baseUrl = `http://${LOCAL_IP}`

// H5 goes through devServer proxy (/api -> backend), so use same-origin.
// #ifdef H5
baseUrl = ''
// #endif

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
    // H5 should always keep same-origin and use /api proxy.
    // #ifdef H5
    config.baseUrl = ''
    config.localIp = ip
    return
    // #endif

    config.baseUrl = LOCAL_PORT ? `http://${ip}:${LOCAL_PORT}` : `http://${ip}`
    config.localIp = ip
}
