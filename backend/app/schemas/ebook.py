"""
电子书相关的 Pydantic 模式
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class EbookBase(BaseModel):
    """电子书基础模式"""
    title: str
    author: Optional[str] = None
    description: Optional[str] = None
    file_name: str
    file_size: int
    file_type: str
    cover_image: Optional[str] = None
    tags: Optional[str] = None
    reading_progress: int = 0


class EbookCreate(EbookBase):
    """创建电子书模式"""
    file_path: str


class EbookUpdate(BaseModel):
    """更新电子书模式"""
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    cover_image: Optional[str] = None
    tags: Optional[str] = None
    reading_progress: Optional[int] = None


class EbookResponse(EbookBase):
    """电子书响应模式"""
    id: int
    user_id: int
    file_path: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

