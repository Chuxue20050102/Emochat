import re

CRISIS_KEYWORDS = (
    "自杀",
    "轻生",
    "结束生命",
    "不想活",
    "想死",
    "去死",
    "割腕",
    "跳楼",
    "服药自杀",
    "上吊",
    "活着没意义",
    "活着好累",
    "消失算了",
    "不如死了",
    "伤害自己",
    "自残",
    "崩溃",
    "绝望",
)

SAD_KEYWORDS = ("难过", "低落", "委屈", "伤心", "压抑", "沮丧", "失落")
ANXIOUS_KEYWORDS = ("焦虑", "紧张", "压力大", "睡不着", "害怕", "撑不住", "心慌", "烦躁")


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", "", (text or "").lower())


def detect_crisis_level(text: str) -> str:
    normalized = normalize_text(text)
    if not normalized:
        return "none"

    if any(k in normalized for k in CRISIS_KEYWORDS):
        return "crisis"
    if ("死" in normalized or "自残" in normalized) and ("计划" in normalized or "今晚" in normalized):
        return "crisis"
    return "none"


def detect_crisis(text: str) -> bool:
    return detect_crisis_level(text) == "crisis"


def classify_user_state(text: str) -> str:
    normalized = normalize_text(text)
    if not normalized:
        return "normal"

    risk = detect_crisis_level(normalized)
    if risk == "crisis":
        return "crisis"
    if any(keyword in normalized for keyword in ANXIOUS_KEYWORDS):
        return "anxious"
    if any(keyword in normalized for keyword in SAD_KEYWORDS):
        return "sad"
    return "normal"


def select_response_mode(state: str) -> str:
    mapping = {
        "normal": "listener",
        "sad": "followup",
        "anxious": "stabilize",
        "crisis": "safety",
    }
    return mapping.get(state, "listener")


def crisis_help_message() -> str:
    return (
        "我看到你现在很痛苦，你不需要一个人扛。"
        "如果你有伤害自己的冲动，请立刻联系你信任的人，"
        "并尽快联系当地紧急援助电话（如 120/110）或心理危机热线。"
    )
