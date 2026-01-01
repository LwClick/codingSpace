"""
文件相关的 Pydantic 模式
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class FileBase(BaseModel):
    """文件基础模式"""
    original_name: str
    file_size: int
    file_type: str
    file_extension: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[str] = None
    category: Optional[str] = None
    is_public: int = 0


class FileCreate(FileBase):
    """创建文件模式"""
    stored_name: str
    file_path: str


class FileUpdate(BaseModel):
    """更新文件模式"""
    description: Optional[str] = None
    tags: Optional[str] = None
    category: Optional[str] = None
    is_public: Optional[int] = None


class FileResponse(FileBase):
    """文件响应模式"""
    id: int
    user_id: int
    stored_name: str
    file_path: str
    download_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

