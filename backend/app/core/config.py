"""
应用配置管理
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """应用配置"""
    
    # 应用信息
    APP_NAME: str = "codingSpace Backend"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./codingSpace.db"
    
    # JWT配置
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7天
    
    # CORS配置
    CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"
    
    # 文件存储配置
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB，单位：字节
    
    # 外部服务配置（用于新闻爬虫等服务）
    NEWS_CRAWLER_URL: str = ""  # 新闻爬虫服务地址
    
    @property
    def cors_origins_list(self) -> List[str]:
        """将CORS_ORIGINS字符串转换为列表"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

