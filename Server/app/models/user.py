from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Text, Boolean, Date
from sqlalchemy.orm import relationship
from app.db import Base

class User(Base):
    # 用户表定义
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, index=True, nullable=False)  # 用户名唯一
    hashed_password = Column(String(128), nullable=False)  # 加密后的密码
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # 创建时间
    
    group_id = Column(Integer, ForeignKey("plugin_groups.id"), nullable=True)
    permissions = Column(Text, nullable=True) # Comma separated permissions
    expire_date = Column(DateTime(timezone=True), nullable=True)

    # Email & Verification
    email = Column(String(255), unique=True, index=True, nullable=True)
    is_verified = Column(Boolean, default=False)
    verification_code = Column(String(6), nullable=True)
    
    # Password Reset
    reset_token = Column(String(128), nullable=True)
    reset_token_expire = Column(DateTime(timezone=True), nullable=True)

    # Profile & VIP & Check-in
    nickname = Column(String(50), nullable=True)
    avatar = Column(String(500), nullable=True)
    points = Column(Integer, default=0)
    level = Column(Integer, default=1)
    vip_type = Column(String(20), default='none') # 'none', 'vip', 'svip'
    vip_expire = Column(DateTime(timezone=True), nullable=True)
    vip_daily_quota = Column(Integer, default=0)
    vip_quota_reset_date = Column(Date, nullable=True)
    
    total_check_in_days = Column(Integer, default=0)
    consecutive_check_in = Column(Integer, default=0)
    last_check_in_date = Column(Date, nullable=True)

    group = relationship("PluginGroup", back_populates="users")
