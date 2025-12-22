# -*- coding: utf-8 -*-
"""
管理员配置接口
功能：管理功能配置、VIP配置、签到配置
"""

from fastapi import APIRouter, Header, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.business import FeatureConfig, VipConfig, CheckInConfig

router = APIRouter()

# ==================== 数据模型 ====================

class FeatureConfigCreate(BaseModel):
    feature_key: str
    feature_name: str
    category: str = "general"
    points_cost: int
    vip_points_cost: int = 0
    svip_points_cost: int = 0
    description: Optional[str] = None

class FeatureConfigUpdate(BaseModel):
    points_cost: Optional[int] = None
    vip_points_cost: Optional[int] = None
    svip_points_cost: Optional[int] = None
    enabled: Optional[bool] = None
    description: Optional[str] = None

class VIPConfigUpdate(BaseModel):
    price: Optional[float] = None
    daily_quota: Optional[int] = None
    points_multiplier: Optional[float] = None

class CheckInConfigCreate(BaseModel):
    consecutive_days: int
    base_points: int
    bonus_points: int
    total_points: int

class CheckInConfigUpdate(BaseModel):
    base_points: Optional[int] = None
    bonus_points: Optional[int] = None
    total_points: Optional[int] = None

# ==================== 辅助函数 ====================

def verify_admin_token(token: str):
    """验证管理员Token"""
    expected_token = "admin-secret-token"
    if token != expected_token:
        raise HTTPException(status_code=401, detail="管理员Token无效")

# ==================== 功能配置管理 ====================

@router.get("/admin/config/features")
async def get_features_config(token: str = Header(..., alias="x-admin-token"), db: Session = Depends(get_db)):
    """获取所有功能配置"""
    verify_admin_token(token)
    features = db.query(FeatureConfig).order_by(FeatureConfig.category, FeatureConfig.feature_key).all()
    return features

@router.post("/admin/config/features")
async def create_feature_config(
    data: FeatureConfigCreate,
    token: str = Header(..., alias="x-admin-token"),
    db: Session = Depends(get_db)
):
    """新增功能配置"""
    verify_admin_token(token)
    
    existing = db.query(FeatureConfig).filter(FeatureConfig.feature_key == data.feature_key).first()
    if existing:
        raise HTTPException(status_code=400, detail="功能标识已存在")
    
    new_feature = FeatureConfig(
        feature_key=data.feature_key,
        feature_name=data.feature_name,
        category=data.category,
        points_cost=data.points_cost,
        vip_points_cost=data.vip_points_cost,
        svip_points_cost=data.svip_points_cost,
        description=data.description
    )
    db.add(new_feature)
    db.commit()
    return {"code": 200, "message": "创建成功"}

@router.put("/admin/config/features/{feature_key}")
async def update_feature_config(
    feature_key: str,
    data: FeatureConfigUpdate,
    token: str = Header(..., alias="x-admin-token"),
    db: Session = Depends(get_db)
):
    """更新功能配置"""
    verify_admin_token(token)
    
    feature = db.query(FeatureConfig).filter(FeatureConfig.feature_key == feature_key).first()
    if not feature:
        raise HTTPException(status_code=404, detail="功能配置不存在")
    
    if data.points_cost is not None:
        feature.points_cost = data.points_cost
    if data.vip_points_cost is not None:
        feature.vip_points_cost = data.vip_points_cost
    if data.svip_points_cost is not None:
        feature.svip_points_cost = data.svip_points_cost
    if data.enabled is not None:
        feature.enabled = data.enabled
    if data.description is not None:
        feature.description = data.description
    
    db.commit()
    return {"code": 200, "message": "更新成功"}

@router.delete("/admin/config/features/{feature_key}")
async def delete_feature_config(
    feature_key: str,
    token: str = Header(..., alias="x-admin-token"),
    db: Session = Depends(get_db)
):
    """删除功能配置"""
    verify_admin_token(token)
    
    feature = db.query(FeatureConfig).filter(FeatureConfig.feature_key == feature_key).first()
    if not feature:
        raise HTTPException(status_code=404, detail="功能配置不存在")
    
    db.delete(feature)
    db.commit()
    return {"code": 200, "message": "删除成功"}

# ==================== VIP配置管理 ====================

@router.get("/admin/config/vip")
async def get_vip_config(token: str = Header(..., alias="x-admin-token"), db: Session = Depends(get_db)):
    """获取VIP配置"""
    verify_admin_token(token)
    
    # Sort order: vip, svip
    # We can fetch all and sort in python or rely on insertion order/id
    configs = db.query(VipConfig).all()
    # Simple sort
    configs.sort(key=lambda x: 0 if x.vip_type == 'vip' else 1)
    return configs

@router.put("/admin/config/vip/{vip_type}")
async def update_vip_config(
    vip_type: str,
    data: VIPConfigUpdate,
    token: str = Header(..., alias="x-admin-token"),
    db: Session = Depends(get_db)
):
    """更新VIP配置"""
    verify_admin_token(token)
    
    if vip_type not in ['vip', 'svip']:
        raise HTTPException(status_code=400, detail="VIP类型必须是vip或svip")
    
    config = db.query(VipConfig).filter(VipConfig.vip_type == vip_type).first()
    if not config:
        raise HTTPException(status_code=404, detail="VIP配置不存在")
    
    if data.price is not None:
        config.price = data.price
    if data.daily_quota is not None:
        config.daily_quota = data.daily_quota
    if data.points_multiplier is not None:
        config.points_multiplier = data.points_multiplier
    
    db.commit()
    return {"code": 200, "message": "更新成功"}

# ==================== 签到配置管理 ====================

@router.get("/admin/config/checkin")
async def get_checkin_config(token: str = Header(..., alias="x-admin-token"), db: Session = Depends(get_db)):
    """获取签到配置"""
    verify_admin_token(token)
    configs = db.query(CheckInConfig).filter(CheckInConfig.enabled == True).order_by(CheckInConfig.consecutive_days).all()
    return configs

@router.post("/admin/config/checkin")
async def create_checkin_config(
    data: CheckInConfigCreate,
    token: str = Header(..., alias="x-admin-token"),
    db: Session = Depends(get_db)
):
    """新增签到档位"""
    verify_admin_token(token)
    
    existing = db.query(CheckInConfig).filter(CheckInConfig.consecutive_days == data.consecutive_days).first()
    if existing:
        raise HTTPException(status_code=400, detail="该连续天数配置已存在")
    
    new_config = CheckInConfig(
        consecutive_days=data.consecutive_days,
        base_points=data.base_points,
        bonus_points=data.bonus_points,
        total_points=data.total_points
    )
    db.add(new_config)
    db.commit()
    return {"code": 200, "message": "创建成功"}

@router.put("/admin/config/checkin/{consecutive_days}")
async def update_checkin_config(
    consecutive_days: int,
    data: CheckInConfigUpdate,
    token: str = Header(..., alias="x-admin-token"),
    db: Session = Depends(get_db)
):
    """更新签到档位"""
    verify_admin_token(token)
    
    config = db.query(CheckInConfig).filter(CheckInConfig.consecutive_days == consecutive_days).first()
    if not config:
        raise HTTPException(status_code=404, detail="签到配置不存在")
    
    if data.base_points is not None:
        config.base_points = data.base_points
    if data.bonus_points is not None:
        config.bonus_points = data.bonus_points
    if data.total_points is not None:
        config.total_points = data.total_points
    
    db.commit()
    return {"code": 200, "message": "更新成功"}

@router.delete("/admin/config/checkin/{consecutive_days}")
async def delete_checkin_config(
    consecutive_days: int,
    token: str = Header(..., alias="x-admin-token"),
    db: Session = Depends(get_db)
):
    """删除签到档位"""
    verify_admin_token(token)
    
    config = db.query(CheckInConfig).filter(CheckInConfig.consecutive_days == consecutive_days).first()
    if not config:
        raise HTTPException(status_code=404, detail="签到配置不存在")
    
    db.delete(config)
    db.commit()
    return {"code": 200, "message": "删除成功"}

