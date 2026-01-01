"""
新闻模型
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base


class News(Base):
    """新闻表"""
    __tablename__ = "news"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, index=True)
    content = Column(Text, nullable=True)
    summary = Column(String(1000), nullable=True)  # 摘要
    source = Column(String(200), nullable=True)  # 来源
    source_url = Column(String(1000), nullable=True)  # 来源链接
    author = Column(String(100), nullable=True)  # 作者
    category = Column(String(50), nullable=True, index=True)  # 分类
    tags = Column(String(500), nullable=True)  # 标签
    cover_image = Column(String(1000), nullable=True)  # 封面图片
    publish_date = Column(DateTime(timezone=True), nullable=True)  # 发布时间
    crawl_date = Column(DateTime(timezone=True), server_default=func.now())  # 爬取时间
    view_count = Column(Integer, default=0)  # 浏览次数
    is_featured = Column(Integer, default=0)  # 是否精选（0=否，1=是）
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

