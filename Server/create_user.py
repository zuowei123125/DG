import sys
import os

# Add current directory to sys.path
sys.path.append(os.getcwd())

from app.db import SessionLocal
from app.services.auth_service import auth_service
from app.schemas.auth import UserRegister
from app.core.security import get_password_hash
from app.models.user import User

def create_user(username, password, email=None):
    db = SessionLocal()
    try:
        # Check if user exists
        existing = db.query(User).filter(User.username == username).first()
        if existing:
            print(f"❌ 用户名 '{username}' 已存在")
            return

        # Prepare registration data
        # We bypass the code verification by not providing code, 
        # but we set email if provided.
        # However, auth_service.register sets is_verified=False by default if code is missing.
        # We might want to manually set is_verified=True after registration for convenience.
        
        register_data = UserRegister(
            username=username,
            password=password,
            confirm_password=password,
            email=email,
            device_id="local_script"
        )
        
        # Call register service
        try:
            token = auth_service.register(db, register_data)
            print(f"✅ 用户 '{username}' 注册成功！")
            
            # Manually verify the user for local convenience
            user = db.query(User).filter(User.username == username).first()
            if user:
                user.is_verified = True
                user.permissions = "admin" # Grant admin permissions for local test user
                db.commit()
                print(f"✅ 已自动验证邮箱并赋予 admin 权限")
                
        except Exception as e:
            print(f"❌ 注册失败: {e}")
            
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.path) < 2:
        print("Usage: python create_user.py [username] [password]")
    
    username = "admin"
    password = "password123"
    email = "admin@example.com"
    
    if len(sys.argv) > 1:
        username = sys.argv[1]
    if len(sys.argv) > 2:
        password = sys.argv[2]
        
    print(f"正在创建用户: {username} ...")
    create_user(username, password, email)
