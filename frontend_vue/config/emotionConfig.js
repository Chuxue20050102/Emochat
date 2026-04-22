export const emotionList = [
  {
    emoji: '😭',
    name: '非常不愉快',
    bgColor: 'linear-gradient(180deg, #F7F4FF 0%, #E5DBFF 100%)',
    glowColor: 'rgba(94, 62, 173, 0.42)',
    subTags: ['崩溃', '绝望', '窒息感', '无法承受', '想躲起来', '惊恐', '失控', '无助', '自责', '压垮了', '情绪爆炸', '喘不过气'],
  },
  {
    emoji: '😣',
    name: '不愉快',
    bgColor: 'linear-gradient(180deg, #F8F5FF 0%, #EDE3FF 100%)',
    glowColor: 'rgba(122, 88, 198, 0.4)',
    subTags: ['烦躁', '委屈', '压力大', '心累', '不安', '焦虑', '烦闷', '难受', '挫败', '失眠', '紧绷', '敏感'],
  },
  {
    emoji: '😕',
    name: '有点不愉快',
    bgColor: 'linear-gradient(180deg, #F5F7FF 0%, #E2E9FF 100%)',
    glowColor: 'rgba(104, 116, 210, 0.38)',
    subTags: ['有点闷', '低落', '担心', '失望', '心里堵', '迷茫', '提不起劲', '没精神', '不太舒服', '小失落', '内耗', '不确定'],
  },
  {
    emoji: '😐',
    name: '中性',
    bgColor: 'linear-gradient(180deg, #F4F9FF 0%, #DCEBFF 100%)',
    glowColor: 'rgba(88, 150, 220, 0.35)',
    subTags: ['平静', '淡然', '发呆', '放空', '没波动', '一般', '还好', '平稳', '无聊', '木木的', '低刺激', '慢节奏'],
  },
  {
    emoji: '🙂',
    name: '有点愉快',
    bgColor: 'linear-gradient(180deg, #F2FCFF 0%, #D8F3F8 100%)',
    glowColor: 'rgba(74, 185, 186, 0.35)',
    subTags: ['轻松', '舒服', '安心', '有盼头', '回暖', '松一口气', '被安慰', '慢慢变好', '放松', '有希望', '踏实', '稳定向上'],
  },
  {
    emoji: '😊',
    name: '愉快',
    bgColor: 'linear-gradient(180deg, #F2FFF8 0%, #D9F4E4 100%)',
    glowColor: 'rgba(86, 178, 115, 0.35)',
    subTags: ['开心', '满足', '顺利', '被理解', '有收获', '舒畅', '有成就感', '专注', '状态在线', '被支持', '明朗', '积极'],
  },
  {
    emoji: '😄',
    name: '很愉快',
    bgColor: 'linear-gradient(180deg, #FAFFF0 0%, #E8F5C7 100%)',
    glowColor: 'rgba(154, 190, 70, 0.35)',
    subTags: ['兴奋', '状态好', '有动力', '特别开心', '想分享', '超满足', '干劲满满', '轻盈', '灵感多', '成就满格', '自信', '很有能量'],
  },
  {
    emoji: '🤩',
    name: '非常愉快',
    bgColor: 'linear-gradient(180deg, #FFFCEF 0%, #FFE8B8 100%)',
    glowColor: 'rgba(241, 166, 68, 0.38)',
    subTags: ['幸福感', '成就感', '能量满格', '太棒了', '今天很亮', '高光时刻', '心花怒放', '雀跃', '充满爱意', '非常幸运', '圆满', '值得庆祝'],
  },
]

export const reasonTags = ['学习', '人际', '工作', '家庭', '情感', '天气', '生理期', '健康', '金钱', '未来']

export const emotionRules = {
  非常不愉快: { color: '#5E3EAD', emoji: '😭', trend: '最近承受了很多，先照顾好自己。' },
  不愉快: { color: '#7A58C6', emoji: '😣', trend: '这段时间不容易，你已经很努力了。' },
  有点不愉快: { color: '#6874D2', emoji: '😕', trend: '有波动很正常，正在慢慢调节中。' },
  中性: { color: '#5896DC', emoji: '😐', trend: '整体比较平稳，节奏在回到轨道。' },
  有点愉快: { color: '#4AB9BA', emoji: '🙂', trend: '状态开始回暖，继续保持。' },
  愉快: { color: '#56B273', emoji: '😊', trend: '近期有不少让你舒心的时刻。' },
  很愉快: { color: '#9ABE46', emoji: '😄', trend: '状态很好，能量感在提升。' },
  非常愉快: { color: '#F1A644', emoji: '🤩', trend: '近期整体很亮眼，活力十足。' },
}
