from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.auth import UserLogin, UserRegister, Token, VerifyRequest, VerifyResponse
from app.schemas.client import LoginData
from app.models.user import User
from app.core.security import verify_password, get_password_hash, create_access_token
from app.models.session import UserSession
from datetime import datetime, timedelta, timezone
import random
import secrets
import string
from app.services.email_service import email_service

from app.models.group import PluginGroup

class AuthService:
    def login(self, db: Session, login_data: UserLogin) -> Token:
        # 根据用户名查找用户并验证密码
        user = db.query(User).filter(User.username == login_data.username).first()
        
        if not user or not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 单设备同时在线限制：自动踢掉其他设备的旧会话
        now = datetime.now(timezone.utc)
        other_active_sessions = (
            db.query(UserSession)
            .filter(
                UserSession.user_id == user.id,
                UserSession.device_id != login_data.device_id,
                UserSession.active == True,
                (UserSession.expires_at == None) | (UserSession.expires_at > now),
            )
            .all()
        )
        
        # 自动踢掉其他设备（设置为非活跃）
        if other_active_sessions:
            for session in other_active_sessions:
                session.active = False
                session.logout_at = now
                # 计算该会话的时长
                if session.login_at:
                    login_at = session.login_at
                    if login_at.tzinfo is None:
                        login_at = login_at.replace(tzinfo=timezone.utc)
                    session.duration_seconds = int((now - login_at).total_seconds())
            db.commit()

        token = create_access_token(subject=login_data.username, device_id=login_data.device_id)
        # 记录/更新当前设备会话
        
        session = (
            db.query(UserSession)
            .filter(UserSession.user_id == user.id, UserSession.device_id == login_data.device_id)
            .first()
        )
        expires = now + timedelta(days=7)  # 7 天有效期
        
        if session:
            session.active = True
            session.expires_at = expires
            session.login_at = now
            session.logout_at = None
            session.duration_seconds = None
            session.last_seen_at = now
        else:
            session = UserSession(
                user_id=user.id,
                device_id=login_data.device_id,
                active=True,
                expires_at=expires,
                login_at=now,
                last_seen_at=now,
            )
            db.add(session)
        
        db.commit()

        return Token(access_token=token, token_type="bearer", username=login_data.username)

    def client_login(self, db: Session, login_data: UserLogin) -> LoginData:
        # Re-use logic or call login internally?
        # Ideally refactor, but for now let's copy the essential verification logic to ensure correct return type
        # Or better, call login to get token and session handling, then enrich data.
        
        token_obj = self.login(db, login_data)
        user = db.query(User).filter(User.username == login_data.username).first()
        
        permissions_list = []
        if user.permissions:
            permissions_list = [p.strip() for p in user.permissions.split(",")]
            
        expire_date_str = None
        if user.expire_date:
            expire_date_str = user.expire_date.strftime("%Y-%m-%d")

        return LoginData(
            token=token_obj.access_token,
            username=user.username,
            expire_date=expire_date_str,
            permissions=permissions_list
        )

    def register(self, db: Session, register_data: UserRegister) -> Token:
        # 校验确认密码一致性
        if register_data.password != register_data.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="两次输入的密码不一致"
            )
        # 检查用户名是否已存在
        existing = db.query(User).filter(User.username == register_data.username).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已被注册"
            )
            
        # 检查邮箱是否已存在
        if register_data.email:
             existing_email = db.query(User).filter(User.email == register_data.email).first()
             if existing_email:
                 # 如果已验证，或者是旧流程（无验证码），则报错
                 # 新流程（有验证码）允许存在未验证的用户记录（即临时用户）
                 is_new_flow = hasattr(register_data, "code") and register_data.code
                 if existing_email.is_verified or not is_new_flow:
                     raise HTTPException(
                         status_code=status.HTTP_400_BAD_REQUEST,
                         detail="该邮箱已被注册"
                     )
        
        # 验证码校验逻辑 (如果提供了验证码)
        if hasattr(register_data, "code") and register_data.code:
             # 这里需要一种机制来验证验证码，通常需要先调用 send-verification-code 接口
             # 并在数据库或缓存中暂存验证码。
             # 由于当前 User 表是注册成功才创建，我们需要一个临时存储或者允许预先创建未验证用户。
             # 方案：先查询是否有未验证的同名/同邮箱用户，或者使用 Redis。
             # 简单方案：使用一个专门的 VerificationCode 表，或者复用 User 表但标记状态。
             
             # 这里为了配合新的需求，我们需要修改 User 表的使用方式：
             # 1. 发送验证码时，如果用户不存在，创建一个 is_verified=False 的用户，存 code
             # 2. 注册时，查找该用户，验证 code，更新密码等信息，设 is_verified=True
             
             # 但 send-verification-code 接口目前还未实现，我们先假设用户通过该接口发送了验证码
             # 并且我们通过 email 查找到了这个预创建的用户记录
             
             pre_user = db.query(User).filter(User.email == register_data.email).first()
             if not pre_user:
                 raise HTTPException(status_code=400, detail="请先发送验证码")
             if pre_user.verification_code != register_data.code:
                 raise HTTPException(status_code=400, detail="验证码错误")
             
             # 验证通过，更新用户信息 (从预创建转为正式)
             user = pre_user
             user.username = register_data.username
             user.hashed_password = get_password_hash(register_data.password)
             user.is_verified = True
             user.verification_code = None
             
             # 处理组逻辑
             target_group = db.query(PluginGroup).filter(PluginGroup.name == "default").first()
             if not target_group:
                  target_group = db.query(PluginGroup).first()
             user.group_id = target_group.id if target_group else None
             
        else:
            # 旧逻辑：直接创建，后续验证
            # 创建新用户，保存哈希后的密码
            # 自动分配组策略：
            # 1. 尝试查找名为 "default" 的组
            # 2. 如果不存在，尝试使用数据库中第一个组
            # 3. 如果没有任何组，则 group_id 为 None
            
            target_group = db.query(PluginGroup).filter(PluginGroup.name == "default").first()
            if not target_group:
                 target_group = db.query(PluginGroup).first()
            
            group_id = target_group.id if target_group else None
    
            user = User(
                username=register_data.username,
                hashed_password=get_password_hash(register_data.password),
                group_id=group_id,
                email=register_data.email,
                is_verified=False
            )
            
            # 如果提供了邮箱，生成验证码并发送
            if register_data.email:
                code = ''.join(random.choices(string.digits, k=6))
                user.verification_code = code
                try:
                    email_service.send_verification_email(register_data.email, code)
                except Exception as e:
                    print(f"Failed to send verification email: {e}")
        
        db.add(user)
        db.commit()
        db.refresh(user)

        # 注册成功后，自动创建会话并登录
        # 注意：这里需要 device_id，如果前端未传，默认值为 "unknown_device"
        device_id = getattr(register_data, "device_id", "unknown_device")
        
        # 创建 Session
        now = datetime.now(timezone.utc)
        expires = now + timedelta(days=7)  # 保持与 Login 一致
        session = UserSession(
            user_id=user.id,
            device_id=device_id,
            active=True,
            expires_at=expires,
            login_at=now,
            last_seen_at=now,
        )
        db.add(session)
        db.commit()

        token = create_access_token(subject=register_data.username, device_id=device_id)
        return Token(access_token=token, token_type="bearer", username=register_data.username)
    
    def send_verification_code(self, db: Session, email: str) -> dict:
        # 1. 检查邮箱是否已被正式注册
        existing = db.query(User).filter(User.email == email, User.is_verified == True).first()
        if existing:
            raise HTTPException(status_code=400, detail="该邮箱已被注册")
            
        # 2. 查找或创建临时用户记录
        user = db.query(User).filter(User.email == email).first()
        code = ''.join(random.choices(string.digits, k=6))
        
        if user:
            # 更新现有临时用户的验证码
            user.verification_code = code
        else:
            # 创建临时用户 (username 暂时用 email 占位，注册时会更新)
            # 注意：username 是 unique 且 nullable=False，所以必须给一个值
            # 我们可以用 "temp_{email}" 或者随机字符串，只要不冲突
            temp_username = f"temp_{secrets.token_hex(8)}"
            user = User(
                username=temp_username,
                email=email,
                hashed_password="temp_password_placeholder", # 必填字段占位
                is_verified=False,
                verification_code=code
            )
            db.add(user)
            
        db.commit()
        
        # 3. 发送邮件
        try:
            email_service.send_verification_email(email, code)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"邮件发送失败: {str(e)}")
            
        return {"detail": "验证码已发送"}
    
    def verify_email(self, db: Session, username: str, code: str) -> dict:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
        if user.is_verified:
            return {"detail": "邮箱已验证"}
        if not user.verification_code or user.verification_code != code:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="验证码错误")
        
        user.is_verified = True
        user.verification_code = None
        db.commit()
        return {"detail": "验证成功"}

    def forgot_password(self, db: Session, email: str) -> dict:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            # 为安全起见，不提示用户不存在，或者提示已发送
            return {"detail": "如果邮箱存在，重置邮件已发送"}
        
        # 改用6位数字验证码作为Token（为了用户体验）
        token = ''.join(random.choices(string.digits, k=6))
        
        # 存储 Token (复用 reset_token 字段，虽然叫 token 但存的是验证码)
        user.reset_token = token
        user.reset_token_expire = datetime.now(timezone.utc) + timedelta(minutes=30)
        db.commit()
        
        try:
            email_service.send_reset_password_email(email, token)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"邮件发送失败: {str(e)}")
            
        return {"detail": "如果邮箱存在，重置邮件已发送"}

    def reset_password(self, db: Session, token: str, new_password: str, email: str) -> dict:
        # 修改：reset_password 需要 email + code 来定位用户
        # 因为6位验证码可能重复，所以必须配合邮箱查找
        
        user = db.query(User).filter(User.email == email).first()
        if not user:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")

        if user.reset_token != token:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="验证码错误")
        
        if not user.reset_token_expire:
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="验证码无效")

        expire_time = user.reset_token_expire
        if expire_time.tzinfo is None:
            expire_time = expire_time.replace(tzinfo=timezone.utc)
            
        if expire_time < datetime.now(timezone.utc):
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="验证码已过期")
             
        user.hashed_password = get_password_hash(new_password)
        user.reset_token = None
        user.reset_token_expire = None
        db.commit()
        return {"detail": "密码重置成功"}

    def logout(self, db: Session, username: str, device_id: str) -> dict:
        # 将指定用户的指定设备会话标记为非活跃
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
        session = (
            db.query(UserSession)
            .filter(UserSession.user_id == user.id, UserSession.device_id == device_id, UserSession.active == True)
            .first()
        )
        if not session:
            # 没有活跃会话也视为成功，前端可以重入
            return {"detail": "已退出登录"}
        session.active = False
        # 记录退出时间与在线时长（秒）
        now = datetime.now(timezone.utc)
        session.logout_at = now
        if session.login_at:
            login_at = session.login_at
            if login_at.tzinfo is None:
                login_at = login_at.replace(tzinfo=timezone.utc)
            session.duration_seconds = int((now - login_at).total_seconds())
        db.commit()
        return {"detail": "已退出登录"}
    
    def heartbeat(self, db: Session, username: str, device_id: str) -> dict:
        # 更新指定设备会话的最近心跳时间，用于统计活跃在线时长
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
        session = (
            db.query(UserSession)
            .filter(UserSession.user_id == user.id, UserSession.device_id == device_id, UserSession.active == True)
            .first()
        )
        if not session:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="会话不存在或已登出")
        session.last_seen_at = datetime.now(timezone.utc)
        db.commit()
        return {"detail": "心跳已更新"}

    def verify_license(self, db: Session, verify_data: VerifyRequest, current_username: str) -> VerifyResponse:
        # 1. 验证用户是否存在
        user = db.query(User).filter(User.username == verify_data.username).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        # 2. 检查 Token 用户一致性
        if current_username != verify_data.username:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token 用户与请求用户不匹配"
            )

        # 3. 检查账户是否过期
        expire_date_str = None
        if user.expire_date:
            expire_dt = user.expire_date
            if expire_dt.tzinfo is None:
                expire_dt = expire_dt.replace(tzinfo=timezone.utc)
            
            if datetime.now(timezone.utc) > expire_dt:
                return VerifyResponse(
                    valid=False,
                    username=user.username,
                    expire_date=user.expire_date.isoformat()
                )
            expire_date_str = user.expire_date.isoformat()

        # 4. 检查会话是否活跃
        session = db.query(UserSession).filter(
            UserSession.user_id == user.id,
            UserSession.device_id == verify_data.device_id,
            UserSession.active == True
        ).first()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="会话不存在或已登出"
            )
        
        # 5. 更新最后活跃时间
        session.last_seen_at = datetime.now(timezone.utc)
        db.commit()
        
        return VerifyResponse(
            valid=True,
            username=user.username,
            expire_date=expire_date_str
        )

auth_service = AuthService()
