"""
电子书模型
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base


class Ebook(Base):
    """电子书表"""
    __tablename__ = "ebooks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(200), nullable=False, index=True)
    author = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    file_path = Column(String(500), nullable=False)  # 文件存储路径
    file_name = Column(String(200), nullable=False)  # 原始文件名
    file_size = Column(Integer, nullable=False)  # 文件大小（字节）
    file_type = Column(String(50), nullable=False)  # 文件类型（pdf, epub, mobi等）
    cover_image = Column(String(500), nullable=True)  # 封面图片
    tags = Column(String(500), nullable=True)  # 标签
    reading_progress = Column(Integer, default=0)  # 阅读进度（0-100）
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    user = relationship("User", backref="ebooks")


