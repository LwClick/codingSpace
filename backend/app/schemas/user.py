"""
用户相关的 Pydantic 模式
"""
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """用户基础模式"""
    username: str
    email: Optional[EmailStr] = None


class UserCreate(UserBase):
    """创建用户模式"""
    password: str


class UserLogin(BaseModel):
    """用户登录模式"""
    username: str
    password: str  # 可以是明文密码或加密密码


class UserLoginEncrypted(BaseModel):
    """用户登录模式（加密密码）"""
    username: str
    encrypted_password: str  # Base64编码的RSA加密密码


class UserResponse(UserBase):
    """用户响应模式"""
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Token响应模式"""
    access_token: str
    token_type: str = "bearer"

