from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import get_password_hash
import logging

logger = logging.getLogger(__name__)

def init_data(db: Session):
    """初始化数据：清理演示账号，重置admin密码"""
    try:
        # 1. 删除 user 和 test 账号
        users_to_delete = ["user", "test"]
        for username in users_to_delete:
            user = db.query(User).filter(User.username == username).first()
            if user:
                logger.info(f"Deleting demo user: {username}")
                db.delete(user)
        
        # 2. 更新或创建 admin 账号
        admin_username = "admin"
        new_password = "Demo123$%!"
        hashed_pwd = get_password_hash(new_password)
        
        admin = db.query(User).filter(User.username == admin_username).first()
        if admin:
            logger.info(f"Updating admin password")
            admin.hashed_password = hashed_pwd
        else:
            logger.info(f"Creating admin user")
            admin = User(
                username=admin_username,
                hashed_password=hashed_pwd,
                is_active=True
            )
            db.add(admin)
            
        db.commit()
    except Exception as e:
        logger.error(f"Error initializing data: {e}")
        db.rollback()
