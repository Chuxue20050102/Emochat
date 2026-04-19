from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from utils import success_resp, error_resp
import random

router = APIRouter(prefix="/api/common", tags=["公共接口"])


@router.get("/greeting")
def get_daily_greeting(db: Session = Depends(get_db)):
    """
    随机获取一条今日问候/积极肯定语
    """
    try:
        greetings = db.query(models.Greeting).all()
        if not greetings:
            # 如果数据库没语料，返回个默认的
            return success_resp(data={
                "id": 0,
                "content": "无论今天发生了什么，都请记得好好爱自己。",
                "author": "EmoChat"
            })

        # 随机选一条
        lucky_one = random.choice(greetings)
        return success_resp(data={
            "id": lucky_one.id,
            "content": lucky_one.content,
            "author": lucky_one.author
        })
    except Exception as e:
        # 如果表还没建好或者报错，降级返回
        return success_resp(data={
            "id": 0,
            "content": "每一朵花都会在属于它的季节绽放，你也是。",
            "author": "EmoChat"
        })


# 2. 初始化问候语数据
@router.post("/init-greetings")
def init_greetings(db: Session = Depends(get_db)):
    # 防止重复插入
    exists = db.query(models.Greeting).first()
    if exists:
        return success_resp(msg="问候语已初始化，无需重复添加")

    # 要插入的数据
    data_list = [
        # 原有问候语
        models.Greeting(content="无论今天发生什么，都请记得好好爱自己。", author="系统"),
        models.Greeting(content="慢慢来，谁都有发光的一天。", author="系统"),
        models.Greeting(content="你很棒，不必焦虑，不必着急。", author="系统"),
        models.Greeting(content="每一朵花都会在属于它的季节绽放，你也是。", author="EmoChat"),
        models.Greeting(content="允许一切发生，你已经做得很好了。", author="系统"),
        # 白天模式问候语
        models.Greeting(content="今天，也值得被温柔对待", author="系统"),
        models.Greeting(content="可以慢一点开始", author="系统"),
        models.Greeting(content="不用急着进入状态", author="系统"),
        models.Greeting(content="现在这一刻，可以不用很用力", author="系统"),
        models.Greeting(content="从一点点开始就好", author="系统"),
        models.Greeting(content="你不需要准备好", author="系统"),
        models.Greeting(content="如果有点乱，也没关系", author="系统"),
        models.Greeting(content="可以先停一下", author="系统"),
        models.Greeting(content="再慢慢来", author="系统"),
        # 夜间模式问候语
        models.Greeting(content="外面安静下来了", author="系统"),
        models.Greeting(content="有些感受开始浮出来", author="系统"),
        models.Greeting(content="可以慢慢说", author="系统"),
        models.Greeting(content="现在不用太清醒", author="系统"),
        models.Greeting(content="可以轻一点表达", author="系统"),
        models.Greeting(content="我在这里", author="系统"),
        models.Greeting(content="夜晚适合慢一点", author="系统"),
        models.Greeting(content="不用解释什么", author="系统"),
        models.Greeting(content="只是说说也可以", author="系统"),
        # 模糊状态问候语
        models.Greeting(content="说不清也没关系", author="系统"),
        models.Greeting(content="可以从一句话开始", author="系统"),
        models.Greeting(content="不用整理", author="系统"),
        models.Greeting(content="如果有点乱", author="系统"),
        models.Greeting(content="先写一点看看", author="系统"),
        models.Greeting(content="不用完整", author="系统"),
        models.Greeting(content="不确定发生了什么也可以", author="系统"),
        models.Greeting(content="慢慢来就好", author="系统"),
        models.Greeting(content="从感觉开始", author="系统"),
        # 低落状态问候语
        models.Greeting(content="如果今天有点难", author="系统"),
        models.Greeting(content="可以慢慢说", author="系统"),
        models.Greeting(content="不用一个人扛着", author="系统"),
        models.Greeting(content="不用撑得很好", author="系统"),
        models.Greeting(content="从最重的那一点开始", author="系统"),
        models.Greeting(content="我在", author="系统"),
        models.Greeting(content="你可以不需要整理情绪", author="系统"),
        models.Greeting(content="只是表达就好", author="系统"),
        models.Greeting(content="不用急", author="系统"),
    ]

    db.add_all(data_list)
    db.commit()
    return success_resp(msg="问候语初始化成功！")