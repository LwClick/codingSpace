"""
文件模型
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, BigInteger
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base


class File(Base):
    """文件表"""
    __tablename__ = "files"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    original_name = Column(String(500), nullable=False)  # 原始文件名
    stored_name = Column(String(500), nullable=False)  # 存储文件名
    file_path = Column(String(1000), nullable=False)  # 文件存储路径
    file_size = Column(BigInteger, nullable=False)  # 文件大小（字节）
    file_type = Column(String(100), nullable=False)  # MIME类型
    file_extension = Column(String(20), nullable=True)  # 文件扩展名
    description = Column(Text, nullable=True)  # 文件描述
    tags = Column(String(500), nullable=True)  # 标签
    category = Column(String(50), nullable=True)  # 分类（document, image, video等）
    is_public = Column(Integer, default=0)  # 是否公开（0=私有，1=公开）
    download_count = Column(Integer, default=0)  # 下载次数
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    user = relationship("User", backref="files")

