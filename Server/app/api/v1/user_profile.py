# -*- coding: utf-8 -*-
"""
用户资料接口
功能：获取和更新用户资料
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db import get_db
from app.models.user import User
from app.models.business import PointsHistory

router = APIRouter()

# ==================== 数据模型 ====================

class UserProfileUpdate(BaseModel):
    username: str
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    email: Optional[str] = None

# ==================== 用户资料管理 ====================

@router.get("/user/profile")
async def get_user_profile(username: str, db: Session = Depends(get_db)):
    """获取用户资料"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 转换为字典以便序列化
    user_data = {
        "username": user.username,
        "nickname": user.nickname,
        "avatar": user.avatar,
        "email": user.email,
        "points": user.points,
        "level": user.level,
        "vip_type": user.vip_type,
        "vip_expire": user.vip_expire.isoformat() if user.vip_expire else None,
        "vip_daily_quota": user.vip_daily_quota,
        "total_check_in_days": user.total_check_in_days,
        "consecutive_check_in": user.consecutive_check_in,
        "created_at": user.created_at.isoformat() if user.created_at else None
    }
    
    return {
        "code": 200,
        "data": user_data
    }

@router.put("/user/profile")
async def update_user_profile(data: UserProfileUpdate, db: Session = Depends(get_db)):
    """更新用户资料"""
    user = db.query(User).filter(User.username == data.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    if data.nickname is not None:
        user.nickname = data.nickname
    if data.avatar is not None:
        user.avatar = data.avatar
    if data.email is not None:
        user.email = data.email
    
    db.commit()
    
    return {
        "code": 200,
        "message": "更新成功"
    }

# ==================== 积分历史 ====================

@router.get("/points/history")
async def get_points_history(
    username: str,
    type: Optional[str] = None,
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """获取积分历史"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    offset = (page - 1) * limit
    
    query = db.query(PointsHistory).filter(PointsHistory.user_id == user.id)
    
    if type:
        query = query.filter(PointsHistory.type == type)
    
    total = query.count()
    records = query.order_by(PointsHistory.created_at.desc()).offset(offset).limit(limit).all()
    
    result_records = []
    for record in records:
        result_records.append({
            "type": record.type,
            "amount": record.amount,
            "balance": record.balance,
            "description": record.description,
            "created_at": record.created_at.isoformat() if record.created_at else None
        })
    
    return {
        "code": 200,
        "data": {
            "total": total,
            "current_balance": user.points,
            "records": result_records
        }
    }

