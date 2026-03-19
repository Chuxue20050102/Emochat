"""
EmoChat AI 服务层
调用 通义千问 (Qwen) 大模型，提供情绪陪伴对话能力。
兼容 OpenAI SDK 格式。
"""

from openai import OpenAI

# 阿里云 DashScope OpenAI 兼容接口地址
client = OpenAI(
    api_key="sk-4f12ee505797457baf9cbf4d3451467f",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 系统人设 prompt —— 定义 AI 的角色
SYSTEM_PROMPT = """你是「EmoChat 情绪陪伴助手」，一个温暖、有同理心的 AI 伙伴。

你的沟通风格：
- 温柔但不敷衍，像一个真正关心你的朋友
- 会先倾听和共情，再给建议
- 回复简洁（控制在 100 字以内），不要长篇大论
- 适当使用 emoji 让对话更亲切 🌿
- 如果用户表达了负面情绪，先肯定 ta 的感受，再温和引导

你不是心理医生，不做诊断，不开药方。如果用户表达了严重的自伤/自杀倾向，请温和地建议 ta 拨打心理援助热线。
"""


def chat_with_ai(user_message: str, history: list = None) -> str:
    """
    调用 Qwen 大模型进行对话。
    
    Args:
        user_message: 用户发送的消息
        history: 可选的历史对话列表，格式 [{"role": "user/assistant", "content": "..."}]
    
    Returns:
        AI 回复的文本内容
    """
    # 构建消息列表
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    # 如果有历史对话，加入上下文（最多保留最近 10 轮）
    if history:
        messages.extend(history[-20:])  
    
    # 加入本次用户消息
    messages.append({"role": "user", "content": user_message})
    
    try:
        response = client.chat.completions.create(
            model="qwen-plus",  # 使用通义千问 Plus 模型
            messages=messages,
            max_tokens=300,
            temperature=0.8,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"[AI Service Error] {e}")
        return "抱歉，我暂时有点累了，请稍后再和我聊聊 🌙"
