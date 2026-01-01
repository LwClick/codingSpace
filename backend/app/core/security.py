"""
安全相关工具函数
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
import base64
import os

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# RSA密钥对（单例模式）
_rsa_private_key = None
_rsa_public_key = None


def get_rsa_keys():
    """获取或生成RSA密钥对"""
    global _rsa_private_key, _rsa_public_key
    
    if _rsa_private_key is None or _rsa_public_key is None:
        # 尝试从环境变量或文件加载密钥
        private_key_pem = os.getenv("RSA_PRIVATE_KEY")
        public_key_pem = os.getenv("RSA_PUBLIC_KEY")
        
        if private_key_pem and public_key_pem:
            # 从环境变量加载
            _rsa_private_key = serialization.load_pem_private_key(
                private_key_pem.encode(),
                password=None,
                backend=default_backend()
            )
            _rsa_public_key = serialization.load_pem_public_key(
                public_key_pem.encode(),
                backend=default_backend()
            )
        else:
            # 生成新的密钥对
            _rsa_private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )
            _rsa_public_key = _rsa_private_key.public_key()
    
    return _rsa_private_key, _rsa_public_key


def get_public_key_pem() -> str:
    """获取公钥的PEM格式字符串"""
    _, public_key = get_rsa_keys()
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return public_key_pem.decode('utf-8')


def decrypt_password(encrypted_password: str) -> str:
    """使用RSA私钥解密密码"""
    try:
        private_key, _ = get_rsa_keys()
        
        # Base64解码
        encrypted_bytes = base64.b64decode(encrypted_password)
        
        # RSA解密
        decrypted_bytes = private_key.decrypt(
            encrypted_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # 转换为字符串
        return decrypted_bytes.decode('utf-8')
    except Exception as e:
        raise ValueError(f"密码解密失败: {str(e)}")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """获取密码哈希"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

