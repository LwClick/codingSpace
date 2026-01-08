"""
数据库连接和初始化
"""
from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# 创建数据库引擎
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基础模型类
Base = declarative_base()


def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def is_database_initialized() -> bool:
    """检查数据库是否已初始化（通过核心表是否存在判断）"""
    inspector = inspect(engine)
    return inspector.has_table("users")


def init_db() -> bool:
    """首次初始化数据库表，已初始化则跳过
    
    返回值:
        True  - 本次调用进行了初始化（首次）
        False - 数据库已初始化（未做任何操作）
    """
    if is_database_initialized():
        return False
    # 导入所有模型，确保它们被注册
    from app.models import user, problem, blog, ebook, file, news  # noqa
    # 创建所有表（仅首次）
    Base.metadata.create_all(bind=engine)
    return True
