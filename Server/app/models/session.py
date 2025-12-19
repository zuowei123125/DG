from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db import Base

class UserSession(Base):
    # 用户会话表，用于限制单设备同时在线
    __tablename__ = "user_sessions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    device_id = Column(String(128), nullable=False, index=True)  # 设备标识（前端提供）
    active = Column(Boolean, default=True, nullable=False)       # 是否处于活跃登录状态
    expires_at = Column(DateTime(timezone=True), nullable=True)  # 过期时间（与令牌一致）
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    login_at = Column(DateTime(timezone=True), nullable=True)    # 登录时间
    logout_at = Column(DateTime(timezone=True), nullable=True)   # 登出时间
    duration_seconds = Column(Integer, nullable=True)            # 在线时长（秒）
    last_seen_at = Column(DateTime(timezone=True), nullable=True) # 最近心跳时间（用于统计活跃时长）

    user = relationship("User")
