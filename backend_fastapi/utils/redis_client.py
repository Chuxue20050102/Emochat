import redis
import json
from typing import Optional, List, Dict

# 创建Redis连接
redis_client = redis.Redis(
    host='127.0.0.1',  # Redis服务器地址
    port=6379,         # Redis端口
    db=1,              # 数据库编号
    decode_responses=True  # 自动解码响应为字符串
)

# 缓存键前缀
CHAT_HISTORY_PREFIX = "chat:history:"
# 缓存过期时间（7天）
CACHE_EXPIRY = 7 * 24 * 60 * 60

def get_chat_history(user_id: int) -> List[Dict]:
    """
    获取用户的聊天历史记录
    """
    key = f"{CHAT_HISTORY_PREFIX}{user_id}"
    history = redis_client.get(key)
    if history:
        return json.loads(history)
    return []

def save_chat_history(user_id: int, messages: List[Dict]) -> bool:
    """
    保存用户的聊天历史记录
    """
    key = f"{CHAT_HISTORY_PREFIX}{user_id}"
    try:
        redis_client.setex(key, CACHE_EXPIRY, json.dumps(messages))
        return True
    except Exception as e:
        print(f"[Redis Error] {e}")
        return False

def add_chat_message(user_id: int, role: str, content: str) -> bool:
    """
    添加一条聊天消息到历史记录
    """
    # 获取现有历史记录
    history = get_chat_history(user_id)
    # 添加新消息
    history.append({"role": role, "content": content})
    # 保存更新后的历史记录
    return save_chat_history(user_id, history)

def clear_chat_history(user_id: int) -> bool:
    """
    清空用户的聊天历史记录
    """
    key = f"{CHAT_HISTORY_PREFIX}{user_id}"
    try:
        redis_client.delete(key)
        return True
    except Exception as e:
        print(f"[Redis Error] {e}")
        return False
