from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.auth import (
    UserLogin, UserRegister, Token, UserLogout, UserHeartbeat, 
    VerifyRequest, VerifyResponse, VerifyEmailRequest, 
    ForgotPasswordRequest, ResetPasswordRequest, SendVerificationCodeRequest
)
from app.services.auth_service import auth_service
from app.db import get_db
from app.models.session import UserSession
from app.models.user import User
from app.core.security import get_current_user
from datetime import datetime, timezone

router = APIRouter()

@router.post("/verify", response_model=VerifyResponse)
async def verify(
    verify_data: VerifyRequest, 
    db: Session = Depends(get_db),
    current_username: str = Depends(get_current_user)
):
    """验证用户授权状态"""
    # 许可证验证接口：验证 token 是否有效，检查账户过期，更新活跃时间
    return auth_service.verify_license(db, verify_data, current_username)

@router.post("/send-verification-code")
async def send_verification_code(body: SendVerificationCodeRequest, db: Session = Depends(get_db)):
    # 发送注册验证码
    return auth_service.send_verification_code(db, body.email)

@router.post("/login", response_model=Token)
async def login(login_data: UserLogin, db: Session = Depends(get_db)):
    # 登录接口：校验用户密码，返回访问令牌
    return auth_service.login(db, login_data)

@router.post("/register", response_model=Token)
async def register(register_data: UserRegister, db: Session = Depends(get_db)):
    # 注册接口：创建新用户，返回访问令牌
    return auth_service.register(db, register_data)

@router.post("/verify-email")
async def verify_email(body: VerifyEmailRequest, db: Session = Depends(get_db)):
    return auth_service.verify_email(db, body.username, body.code)

@router.post("/forgot-password")
async def forgot_password(body: ForgotPasswordRequest, db: Session = Depends(get_db)):
    return auth_service.forgot_password(db, body.email)

@router.post("/reset-password")
async def reset_password(body: ResetPasswordRequest, db: Session = Depends(get_db)):
    if body.new_password != body.confirm_password:
        raise HTTPException(status_code=400, detail="两次输入的密码不一致")
    # 传入 email 参数
    return auth_service.reset_password(db, body.token, body.new_password, body.email)

@router.post("/logout")
async def logout(body: UserLogout, db: Session = Depends(get_db)):
    # 登出接口：将指定设备会话置为非活跃
    return auth_service.logout(db, body.username, body.device_id)

@router.get("/online-time/{username}")
async def get_online_time(username: str, db: Session = Depends(get_db)):
    # 在线时长统计：累计历史会话的时长（秒），以及当前活跃会话的实时时长（秒）
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return {"username": username, "total_seconds": 0, "active_seconds": 0}
    # 历史累计（已登出的会话）
    total = db.query(UserSession).filter(
        UserSession.user_id == user.id,
        UserSession.active == False,
        UserSession.duration_seconds != None
    ).with_entities(UserSession.duration_seconds).all()
    total_seconds = sum([d[0] for d in total]) if total else 0
    # 当前活跃会话实时时长
    now = datetime.now(timezone.utc)
    active = db.query(UserSession).filter(
        UserSession.user_id == user.id,
        UserSession.active == True,
        UserSession.login_at != None
    ).first()
    if active:
        login_at = active.login_at
        if login_at and login_at.tzinfo is None:
            login_at = login_at.replace(tzinfo=timezone.utc)
            
        last_seen = active.last_seen_at or login_at
        if last_seen and last_seen.tzinfo is None:
            last_seen = last_seen.replace(tzinfo=timezone.utc)
            
        # 判定是否在线：如果 last_seen 在最近 2 分钟内，则认为在线，用 now 计算实时时长
        # 否则认为已断开（异常退出），用 last_seen 计算截止时长
        # 阈值设为 120 秒（假设前端心跳间隔为 60 秒）
        is_online = (now - last_seen).total_seconds() < 120
        
        if is_online:
            end_time = now
        else:
            end_time = last_seen
            
        active_seconds = int(max(0, (end_time - login_at).total_seconds())) if login_at else 0
    else:
        active_seconds = 0
    return {"username": username, "total_seconds": total_seconds, "active_seconds": active_seconds}
    
@router.post("/heartbeat")
async def heartbeat(body: UserHeartbeat, db: Session = Depends(get_db)):
    # 心跳接口：更新会话的最近在线时间
    return auth_service.heartbeat(db, body.username, body.device_id)


