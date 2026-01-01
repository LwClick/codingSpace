"""
题目相关的 Pydantic 模式
"""
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class ProblemBase(BaseModel):
    """题目基础模式"""
    date: date
    title: str
    difficulty: Optional[str] = None
    description: Optional[str] = None
    solution: Optional[str] = None
    code: Optional[str] = None
    tags: Optional[str] = None


class ProblemCreate(ProblemBase):
    """创建题目模式"""
    pass


class ProblemUpdate(BaseModel):
    """更新题目模式"""
    title: Optional[str] = None
    difficulty: Optional[str] = None
    description: Optional[str] = None
    solution: Optional[str] = None
    code: Optional[str] = None
    tags: Optional[str] = None


class ProblemResponse(ProblemBase):
    """题目响应模式"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

