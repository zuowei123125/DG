# -*- coding: utf-8 -*-
"""
通用功能使用接口
核心：动态扣费逻辑（SVIP免费、VIP配额、普通积分）
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import date
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.user import User
from app.models.business import FeatureConfig, VipConfig, PointsHistory

router = APIRouter()

# ==================== 数据模型 ====================

class UseFeatureRequest(BaseModel):
    username: str
    feature_key: str
    device_id: str

# ==================== 通用功能使用 ====================

@router.post("/feature/use")
async def use_feature(data: UseFeatureRequest, db: Session = Depends(get_db)):
    """
    通用功能使用接口
    逻辑：
    1. SVIP用户：免费使用
    2. VIP用户：优先使用配额，配额用完后扣积分
    3. 普通用户：扣除积分
    """
    # 1. 获取功能配置
    feature = db.query(FeatureConfig).filter(FeatureConfig.feature_key == data.feature_key).first()
    if not feature or not feature.enabled:
        raise HTTPException(status_code=400, detail="功能不存在或已禁用")
    
    # 2. 获取用户信息
    user = db.query(User).filter(User.username == data.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    current_points = user.points if user.points else 0
    vip_type = user.vip_type
    vip_quota = user.vip_daily_quota if user.vip_daily_quota else 0
    quota_reset_date = user.vip_quota_reset_date
    
    # 3. 检查并重置VIP配额
    today = date.today()
    if vip_type in ['vip', 'svip'] and quota_reset_date != today:
        # 重置配额
        vip_config = db.query(VipConfig).filter(VipConfig.vip_type == vip_type).first()
        if vip_config:
            vip_quota = vip_config.daily_quota
            user.vip_daily_quota = vip_quota
            user.vip_quota_reset_date = today
            db.commit()
    
    # 4. 判断消耗类型
    cost_type = "points"
    points_cost = 0
    remaining_quota = vip_quota
    
    # SVIP免费
    if vip_type == 'svip' and feature.svip_points_cost == 0:
        cost_type = "free"
        message = "SVIP用户免费使用"
    
    # VIP配额
    elif vip_type == 'vip' and vip_quota > 0 and feature.vip_points_cost == 0:
        cost_type = "vip_quota"
        remaining_quota = vip_quota - 1
        user.vip_daily_quota = remaining_quota
        db.commit()
        message = f"VIP配额使用，剩余{remaining_quota}次"
    
    # 扣积分
    else:
        # 计算实际消耗
        if vip_type == 'vip' and feature.vip_points_cost > 0:
            points_cost = feature.vip_points_cost
        elif vip_type == 'svip' and feature.svip_points_cost > 0:
            points_cost = feature.svip_points_cost
        else:
            points_cost = feature.points_cost
        
        # 检查余额
        if current_points < points_cost:
            raise HTTPException(
                status_code=402,
                detail=f"积分不足。当前: {current_points}，需要: {points_cost}。请签到获取积分或开通VIP"
            )
        
        # 扣除积分
        new_balance = current_points - points_cost
        user.points = new_balance
        
        # 记录积分历史
        points_history = PointsHistory(
            user_id=user.id,
            username=data.username,
            type='consume',
            amount=-points_cost,
            balance=new_balance,
            description=f"使用{feature.feature_name}"
        )
        db.add(points_history)
        
        db.commit()
        message = f"消耗{points_cost}积分，剩余{new_balance}积分"
    
    # 5. 记录使用日志 (TODO: Add FeatureUsageLogs model if needed, currently skipping or adding to PointsHistory if consumed)
    # For now, we only log if points consumed. If we need separate usage log table, we need to create it.
    # The SQL version inserted into feature_usage_logs.
    # Let's assume PointsHistory covers financial aspect.
    # If we need analytics, we have analytics API.
    
    # 6. 返回结果
    return {
        "code": 200,
        "data": {
            "success": True,
            "feature_name": feature.feature_name,
            "cost_type": cost_type,
            "points_cost": points_cost,
            "vip_remaining_quota": remaining_quota if vip_type in ['vip', 'svip'] else None,
            "points_remaining": user.points,
            "message": message
        }
    }

