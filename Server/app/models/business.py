from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base
import enum

# Enums
class VipType(str, enum.Enum):
    none = "none"
    vip = "vip"
    svip = "svip"

class FeatureCategory(str, enum.Enum):
    general = "general"
    ai = "ai"
    export = "export"
    layer = "layer"
    other = "other"

# ========== Config Models ==========

class FeatureConfig(Base):
    __tablename__ = "features_config"
    
    id = Column(Integer, primary_key=True, index=True)
    feature_key = Column(String(50), unique=True, index=True, nullable=False)
    feature_name = Column(String(100), nullable=False)
    category = Column(String(50), default="general")
    points_cost = Column(Integer, default=0)
    vip_points_cost = Column(Integer, default=0)
    svip_points_cost = Column(Integer, default=0)
    enabled = Column(Boolean, default=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class VipConfig(Base):
    __tablename__ = "vip_config"
    
    id = Column(Integer, primary_key=True, index=True)
    vip_type = Column(String(20), unique=True, nullable=False) # 'vip', 'svip'
    name = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    daily_quota = Column(Integer, nullable=False) # -1 for infinite
    points_multiplier = Column(Float, default=1.0)
    enabled = Column(Boolean, default=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class CheckInConfig(Base):
    __tablename__ = "check_in_config"
    
    id = Column(Integer, primary_key=True, index=True)
    consecutive_days = Column(Integer, unique=True, nullable=False)
    base_points = Column(Integer, nullable=False)
    bonus_points = Column(Integer, nullable=False)
    total_points = Column(Integer, nullable=False)
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# ========== Record Models ==========

class CheckInRecord(Base):
    __tablename__ = "check_in_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    username = Column(String(50), nullable=False)
    check_in_date = Column(Date, nullable=False, index=True)
    points_earned = Column(Integer, nullable=False)
    consecutive_days = Column(Integer, nullable=False)
    vip_multiplier = Column(Float, default=1.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class PointsHistory(Base):
    __tablename__ = "points_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    username = Column(String(50), nullable=False)
    type = Column(String(20), nullable=False) # checkin, consume, refund, admin
    amount = Column(Integer, nullable=False)
    balance = Column(Integer, nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
