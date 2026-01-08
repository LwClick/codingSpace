"""
题目模型
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base


class Problem(Base):
    """题目表"""
    __tablename__ = "problems"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    title = Column(String(200), nullable=False)
    difficulty = Column(String(20), nullable=True)  # easy, medium, hard
    description = Column(Text, nullable=True)
    solution = Column(Text, nullable=True)  # 解题思路
    code = Column(Text, nullable=True)  # 代码
    tags = Column(String(500), nullable=True)  # 标签，用逗号分隔
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    user = relationship("User", backref="problems")


