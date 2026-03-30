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
        models.Greeting(content="无论今天发生什么，都请记得好好爱自己。", author="系统"),
        models.Greeting(content="慢慢来，谁都有发光的一天。", author="系统"),
        models.Greeting(content="你很棒，不必焦虑，不必着急。", author="系统"),
        models.Greeting(content="每一朵花都会在属于它的季节绽放，你也是。", author="EmoChat"),
        models.Greeting(content="允许一切发生，你已经做得很好了。", author="系统"),
    ]

    db.add_all(data_list)
    db.commit()
    return success_resp(msg="问候语初始化成功！")