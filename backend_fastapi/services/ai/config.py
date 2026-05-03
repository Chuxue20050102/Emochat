import os

REDIS_HOST = os.getenv("EMOCHAT_REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.getenv("EMOCHAT_REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("EMOCHAT_REDIS_DB", "1"))
MEMORY_EXPIRY = int(os.getenv("EMOCHAT_MEMORY_TTL", str(7 * 24 * 60 * 60)))
MEMORY_PREFIX = "memory:"
SUMMARY_PREFIX = "memory_summary:"
PROFILE_PREFIX = "memory_profile:"
REDIS_URL = os.getenv("EMOCHAT_REDIS_URL", f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}")

DASHSCOPE_BASE_URL = os.getenv(
    "DASHSCOPE_BASE_URL",
    "https://dashscope.aliyuncs.com/compatible-mode/v1",
)
DASHSCOPE_MODEL = os.getenv("DASHSCOPE_MODEL", "qwen3.5-35b-a3b")
MAX_RECENT_MESSAGES = int(os.getenv("EMOCHAT_MAX_RECENT_MESSAGES", "8"))
MAX_RECENT_CHARS = int(os.getenv("EMOCHAT_MAX_RECENT_CHARS", "2400"))
MAX_RESPONSE_TOKENS = int(os.getenv("EMOCHAT_MAX_RESPONSE_TOKENS", "220"))
MEMORY_SUMMARY_TRIGGER = int(os.getenv("EMOCHAT_MEMORY_SUMMARY_TRIGGER", "10"))
PROFILE_REFRESH_TRIGGER = int(os.getenv("EMOCHAT_PROFILE_REFRESH_TRIGGER", "8"))
