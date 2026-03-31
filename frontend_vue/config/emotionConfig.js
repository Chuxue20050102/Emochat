// ============ 七档情绪 ============
export const emotionList = [
    {
        emoji: '😣', name: '崩溃',
        bgColor: 'linear-gradient(to bottom, #FAFCFF, #FFEFEA)',
        glowColor: 'rgba(255, 179, 167, 0.6)',
        subTags: ['焦虑', '委屈', '压抑', '疲惫', '痛苦', '绝望', '无助']
    },
    {
        emoji: '😕', name: '迷茫',
        bgColor: 'linear-gradient(to bottom, #FAFCFF, #F2EDFC)',
        glowColor: 'rgba(214, 204, 250, 0.6)',
        subTags: ['不知所措', '怀疑', '困惑', '无力', '空虚', '纠结']
    },
    {
        emoji: '🙁', name: '低落',
        bgColor: 'linear-gradient(to bottom, #FAFCFF, #EDF2F6)',
        glowColor: 'rgba(162, 184, 202, 0.6)',
        subTags: ['难过', '失望', '孤独', '无能为力', '沮丧', '遗憾']
    },
    {
        emoji: '😐', name: '平静',
        bgColor: 'linear-gradient(to bottom, #FAFCFF, #EDF7F1)',
        glowColor: 'rgba(189, 225, 205, 0.6)',
        subTags: ['淡然', '无聊', '波澜不惊', '放空', '发呆']
    },
    {
        emoji: '🙂', name: '轻松',
        bgColor: 'linear-gradient(to bottom, #FAFCFF, #E6F8F2)',
        glowColor: 'rgba(211, 240, 230, 0.6)',
        subTags: ['舒服', '松弛', '解脱', '自在', '宁静']
    },
    {
        emoji: '😊', name: '愉快',
        bgColor: 'linear-gradient(to bottom, #FAFCFF, #FFF6E0)',
        glowColor: 'rgba(255, 224, 142, 0.6)',
        subTags: ['放松', '满足', '开心', '小确幸', '期待']
    },
    {
        emoji: '😄', name: '极好',
        bgColor: 'linear-gradient(to bottom, #FAFCFF, #FFEFEA)',
        glowColor: 'rgba(255, 168, 148, 0.6)',
        subTags: ['激动', '狂喜', '充满力量', '感恩', '幸福']
    }
]

// ============ 原因标签 ============
export const reasonTags = [
    '学习', '人际', '工作', '家庭', '情感', '健康', '金钱', '未来'
]

// ============ 档案页情绪规则（颜色 + 趋势文案） ============
export const emotionRules = {
    '崩溃': { color: '#3A0CA3', emoji: '😣', trend: '这个月，你有些辛苦' },
    '迷茫': { color: '#4361EE', emoji: '😕', trend: '最近有点低落' },
    '低落': { color: '#4895EF', emoji: '🙁', trend: '最近有点低落' },
    '平静': { color: '#4CC9A6', emoji: '😐', trend: '大多数时候是平静的 🌿' },
    '轻松': { color: '#52B788', emoji: '🙂', trend: '你在慢慢恢复' },
    '愉快': { color: '#FFD60A', emoji: '😊', trend: '这个月有不少温暖时刻' },
    '极好': { color: '#FB8500', emoji: '😄', trend: '这个月充满能量 ✨' }
}
