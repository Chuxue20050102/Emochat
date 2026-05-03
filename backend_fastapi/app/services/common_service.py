import random
from typing import Dict, List

from sqlalchemy.orm import Session

import models
from app.repositories import greeting_repository, home_copy_repository

DEFAULT_GREETING = {
    "id": 0,
    "content": "你不需要一下子变好，愿意靠近自己已经很重要。",
    "author": "EmoChat",
}

INITIAL_GREETINGS: List[str] = [
    "你不需要一下子变好，愿意靠近自己已经很重要。",
    "今天可以慢一点，感受被看见就已经算开始。",
    "不用把一切都说明白，先照顾好此刻的自己。",
    "那些说不出口的情绪，也值得被温柔对待。",
    "能停下来看见自己，本身就是一种力量。",
    "可以慢一点开始，不用急着整理好所有语言。",
    "你愿意停下来看看自己，这已经很了不起。",
    "把最真实的一点点先放下来，也算一种照顾。",
    "不确定也没关系，我们可以从一个感受开始。",
    "今天也请给自己一点温柔的空间。",
    "不用非得积极，真实就够了。",
    "情绪没有对错，它只是路过你。",
    "记录本身，就是一种对自己的在意。",
    "你不需要今天就好起来。",
    "有些日子能打开这个页面，就已经是照顾自己了。",
    "不用急着翻篇，先在这里停一停。",
    "世界上已经有太多要求了，这里没有。",
    "把说不清的放进来，比憋着好。",
    "对自己有耐心，本身就很勇敢。",
    "你可以只是来写一句话，甚至只选一个表情。",
]

INITIAL_HOME_COPIES = [
    ("home_card1", "default", "opening_default", "{nickname}，今天也慢慢来"),
    ("home_card1", "default", "opening_guest", "今天也慢慢来"),
    ("home_card1", "default", "opening_newbie", "{nickname}，先从一个感受开始就好"),
    ("home_card1", "default", "opening_returning", "最近的你，我有在慢慢看见"),
    ("home_card1", "default", "opening_recorded_today", "今天的这一点感受已经被接住了"),
    ("home_card1", "default", "hint_newbie_record", "可以先选一个情绪"),
    ("home_card1", "default", "hint_newbie_chat", "想直接聊聊也可以"),
    ("home_card1", "default", "hint_newbie_profile", "记录几次后就能回看状态"),
    ("home_card1", "default", "status_empty", "今天还没有留下心情"),
    ("home_card1", "default", "status_today", "今天已经留下 {count} 次心情"),
    ("home_card1", "default", "status_total", "已经留下 {count} 条线索"),
    ("home_chat_entry", "default", "tag", "今日状态"),
    ("home_chat_entry", "default", "title", "今天要不要先说一句最真实的感受？"),
    ("home_chat_entry", "default", "subtitle", "不需要整理好语言，你开口，我就在。"),
    ("home_chat_entry", "default", "desc", "你可以只说一句近况，我会顺着你的节奏聊下去。"),
    ("home_chat_entry", "anxious", "title", "先说一句最让你紧绷的事"),
    ("home_chat_entry", "anxious", "subtitle", "先不解决，我们一起把那口气慢慢放下来。"),
    ("home_chat_entry", "low", "title", "不用解释太多，我先陪你坐会儿"),
    ("home_chat_entry", "low", "subtitle", "你现在的感受就很重要，说出一句就好。"),
    ("home_chat_entry", "calm", "title", "要不要记录今天的小确幸？"),
    ("home_chat_entry", "calm", "subtitle", "把今天那个稳定的瞬间留下来，它会给你力量。"),
]

MOJIBAKE_MARKERS = ("�", "浠", "鎯", "杩", "璁", "鐨", "鍙", "涓", "鏈", "妗")


def _looks_broken(text: str) -> bool:
    value = str(text or "")
    return any(marker in value for marker in MOJIBAKE_MARKERS)


def _format_template(text: str, **kwargs) -> str:
    try:
        return str(text or "").format(**kwargs)
    except (KeyError, ValueError):
        return str(text or "")


def get_daily_greeting(db: Session):
    greetings = [item for item in greeting_repository.list_all(db) if not _looks_broken(item.content)]
    if not greetings:
        return DEFAULT_GREETING
    lucky_one = random.choice(greetings)
    return {"id": lucky_one.id, "content": lucky_one.content, "author": lucky_one.author}


def init_greetings(db: Session) -> int:
    existing = greeting_repository.list_all(db)
    existing_contents = {g.content for g in existing}

    missing = [
        models.Greeting(content=text, author="系统")
        for text in INITIAL_GREETINGS
        if text not in existing_contents
    ]

    if not missing:
        return 0

    greeting_repository.bulk_insert(db, missing)
    return len(missing)


def init_home_copies(db: Session) -> int:
    existing = home_copy_repository.list_by_module(db, "home_card1") + home_copy_repository.list_by_module(db, "home_chat_entry")
    existing_map = {(item.module, item.state, item.field): item for item in existing}

    changed = 0
    missing = []
    for module, state, field, content in INITIAL_HOME_COPIES:
        key = (module, state, field)
        existing_item = existing_map.get(key)
        if not existing_item:
            missing.append(models.HomeCopy(module=module, state=state, field=field, content=content))
            continue
        if existing_item.content != content:
            existing_item.content = content
            changed += 1

    if missing:
        home_copy_repository.bulk_insert(db, missing)
        changed += len(missing)
    elif changed:
        db.commit()

    return changed


def get_home_copy(db: Session, module: str, state: str = "default") -> Dict[str, str]:
    default_items = home_copy_repository.list_by_module_and_state(db, module, "default")
    state_items = []
    if state and state != "default":
        state_items = home_copy_repository.list_by_module_and_state(db, module, state)

    merged: Dict[str, str] = {
        item.field: item.content
        for item in default_items
        if not _looks_broken(item.content)
    }
    for item in state_items:
        if not _looks_broken(item.content):
            merged[item.field] = item.content
    return merged


def format_home_copy(text: str, **kwargs) -> str:
    return _format_template(text, **kwargs)
