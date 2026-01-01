"""
博客模型
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base


class Blog(Base):
    """博客表"""
    __tablename__ = "blogs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(200), nullable=False, index=True)
    content = Column(Text, nullable=False)
    summary = Column(String(500), nullable=True)  # 摘要
    cover_image = Column(String(500), nullable=True)  # 封面图片URL
    tags = Column(String(500), nullable=True)  # 标签，用逗号分隔
    category = Column(String(50), nullable=True)  # 分类
    is_published = Column(Boolean, default=False)  # 是否发布
    view_count = Column(Integer, default=0)  # 浏览次数
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    user = relationship("User", backref="blogs")

