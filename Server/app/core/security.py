from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db import get_db
from app.models.session import UserSession

# 密码哈希配置（使用 bcrypt）
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # 验证明文密码与哈希是否匹配
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    # 对密码进行哈希
    return pwd_context.hash(password)

def create_access_token(subject: str, device_id: str, expires_delta: Optional[timedelta] = None) -> str:
    # 创建 JWT 访问令牌，默认过期时间从配置读取
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=getattr(settings, "ACCESS_TOKEN_EXPIRE_MINUTES", 60)))
    # 将 device_id 写入 Token Payload
    to_encode = {"sub": subject, "device_id": device_id, "exp": expire}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> str:
    """
    验证 JWT Token 并返回当前用户名 (sub)
    增加 Session 强校验：检查数据库中 Session 是否活跃
    """
    print("="*60)
    print("[get_current_user] 开始验证 Token")
    print(f"   - Token (前30字符): {token[:30]}...")
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的认证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # 1. 解析 Token
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        device_id: str = payload.get("device_id")
        
        print(f"[get_current_user] ✓ Token 解析成功")
        print(f"   - username: {username}")
        print(f"   - device_id: {device_id}")
        print(f"   - exp: {payload.get('exp')}")
        
        if username is None:
            print("[get_current_user] ✗ username 为空")
            raise credentials_exception
            
    except jwt.ExpiredSignatureError:
        print("[get_current_user] ✗ Token 已过期")
        raise credentials_exception
    except jwt.InvalidTokenError as e:
        print(f"[get_current_user] ✗ Token 无效: {e}")
        raise credentials_exception
    except jwt.PyJWTError as e:
        print(f"[get_current_user] ✗ Token 解析失败: {e}")
        raise credentials_exception

    # 2. Session 强校验 (如果有 device_id)
    # 如果 Token 是旧版本没有 device_id，可以选择放行或拒绝。为了安全建议逐步拒绝。
    # 这里我们假设所有新 Token 都有 device_id
    if device_id:
        print(f"[get_current_user] 开始 Session 强校验")
        # 查询 User ID
        from app.models.user import User
        user = db.query(User).filter(User.username == username).first()
        if not user:
            print(f"[get_current_user] ✗ 用户不存在: {username}")
            raise credentials_exception
        
        print(f"[get_current_user] ✓ 用户存在: user_id={user.id}")
            
        # 查询活跃 Session
        print(f"[get_current_user] 查询活跃 Session: user_id={user.id}, device_id={device_id}")
        session = db.query(UserSession).filter(
            UserSession.user_id == user.id,
            UserSession.device_id == device_id,
            UserSession.active == True
        ).first()
        
        if not session:
            # Session 不存在或已失效（被踢下线/登出）
            print(f"[get_current_user] ✗ Session 不存在或已失效")
            
            # 调试：列出该用户的所有 Session
            all_sessions = db.query(UserSession).filter(UserSession.user_id == user.id).all()
            print(f"[get_current_user] 该用户共有 {len(all_sessions)} 个 Session:")
            for s in all_sessions:
                print(f"   - session_id={s.id}, device_id={s.device_id}, active={s.active}")
            
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="会话已失效或在其他设备登录",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        print(f"[get_current_user] ✓ Session 验证通过: session_id={session.id}")
    else:
        print(f"[get_current_user] ⚠️ Token 中没有 device_id，跳过 Session 校验")
    
    print("="*60)
    return username
