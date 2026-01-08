"""
codingSpace 后端主应用
基于 FastAPI 框架
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.v1 import api_router
from app.db.database import init_db, SessionLocal
from app.db.init_data import init_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化数据库
    did_init = init_db()
    
    # 仅首次初始化时执行数据初始化
    if did_init:
        db = SessionLocal()
        try:
            init_data(db)
        finally:
            db.close()
        
    yield
    # 关闭时清理资源（如果需要）


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="codingSpace平台后端API",
    lifespan=lifespan
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "欢迎使用 codingSpace API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
