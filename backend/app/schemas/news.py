"""
新闻相关的 Pydantic 模式
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class NewsBase(BaseModel):
    """新闻基础模式"""
    title: str
    content: Optional[str] = None
    summary: Optional[str] = None
    source: Optional[str] = None
    source_url: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[str] = None
    cover_image: Optional[str] = None
    publish_date: Optional[datetime] = None
    is_featured: int = 0


class NewsCreate(NewsBase):
    """创建新闻模式"""
    pass


class NewsUpdate(BaseModel):
    """更新新闻模式"""
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[str] = None
    is_featured: Optional[int] = None


class NewsResponse(NewsBase):
    """新闻响应模式"""
    id: int
    view_count: int
    crawl_date: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

