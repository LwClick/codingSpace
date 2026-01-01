"""
API v1 路由
"""
from fastapi import APIRouter
from app.api.v1 import auth, problems

api_router = APIRouter()

# 注册子路由
api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(problems.router, prefix="/problems", tags=["题目"])

