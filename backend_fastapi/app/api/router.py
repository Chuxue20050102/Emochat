from fastapi import APIRouter

from app.api.routes import agent, auth, chat, common, emotion, user

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(emotion.router)
api_router.include_router(user.router)
api_router.include_router(chat.router)
api_router.include_router(common.router)
api_router.include_router(agent.router)
