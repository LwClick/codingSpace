"""
博客相关的 Pydantic 模式
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BlogBase(BaseModel):
    """博客基础模式"""
    title: str
    content: str
    summary: Optional[str] = None
    cover_image: Optional[str] = None
    tags: Optional[str] = None
    category: Optional[str] = None
    is_published: bool = False


class BlogCreate(BlogBase):
    """创建博客模式"""
    pass


class BlogUpdate(BaseModel):
    """更新博客模式"""
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    cover_image: Optional[str] = None
    tags: Optional[str] = None
    category: Optional[str] = None
    is_published: Optional[bool] = None


class BlogResponse(BlogBase):
    """博客响应模式"""
    id: int
    user_id: int
    view_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

