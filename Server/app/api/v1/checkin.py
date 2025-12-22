# -*- coding: utf-8 -*-
"""
签到接口
功能：每日签到、签到状态查询、签到日历
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db import get_db
from app.models.user import User
from app.models.business import CheckInConfig, VipConfig, CheckInRecord, PointsHistory

router = APIRouter()

# ==================== 数据模型 ====================

class CheckInRequest(BaseModel):
    username: str

# ==================== 签到功能 ====================

@router.post("/checkin/daily")
async def daily_checkin(data: CheckInRequest, db: Session = Depends(get_db)):
    """每日签到"""
    # 1. 获取用户信息
    user = db.query(User).filter(User.username == data.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 2. 检查今日是否已签到
    today = date.today()
    if user.last_check_in_date == today:
        raise HTTPException(status_code=400, detail="今日已签到，明天再来吧")
    
    # 3. 计算连续天数
    consecutive_days = user.consecutive_check_in if user.consecutive_check_in else 0
    total_days = user.total_check_in_days if user.total_check_in_days else 0
    
    yesterday = today - timedelta(days=1)
    if user.last_check_in_date == yesterday:
        # 连续签到
        consecutive_days += 1
    else:
        # 中断了，重新开始
        consecutive_days = 1
    
    total_days += 1
    
    # 4. 从配置表获取奖励
    reward_config = db.query(CheckInConfig)\
        .filter(CheckInConfig.consecutive_days <= consecutive_days, CheckInConfig.enabled == True)\
        .order_by(CheckInConfig.consecutive_days.desc())\
        .first()
    
    if not reward_config:
        # 如果没有配置，默认给10积分
        base_points = 10
        bonus_points = 0
        total_points = 10
    else:
        base_points = reward_config.base_points
        bonus_points = reward_config.bonus_points
        total_points = reward_config.total_points
    
    # 5. 应用VIP倍数
    vip_multiplier = 1.0
    if user.vip_type and user.vip_type in ['vip', 'svip']:
        vip_config = db.query(VipConfig).filter(VipConfig.vip_type == user.vip_type).first()
        if vip_config:
            vip_multiplier = float(vip_config.points_multiplier)
    
    points_earned = int(total_points * vip_multiplier)
    current_points = user.points if user.points else 0
    new_balance = current_points + points_earned
    
    # 6. 更新用户数据
    user.points = new_balance
    user.total_check_in_days = total_days
    user.consecutive_check_in = consecutive_days
    user.last_check_in_date = today
    
    # 7. 记录签到记录
    checkin_record = CheckInRecord(
        user_id=user.id,
        username=data.username,
        check_in_date=today,
        points_earned=points_earned,
        consecutive_days=consecutive_days,
        vip_multiplier=vip_multiplier
    )
    db.add(checkin_record)
    
    # 8. 记录积分历史
    points_history = PointsHistory(
        user_id=user.id,
        username=data.username,
        type='checkin',
        amount=points_earned,
        balance=new_balance,
        description=f"每日签到奖励（连续{consecutive_days}天）"
    )
    db.add(points_history)
    
    db.commit()
    
    # 9. 返回结果
    return {
        "code": 200,
        "data": {
            "success": True,
            "points_earned": points_earned,
            "base_points": base_points,
            "bonus_points": bonus_points,
            "vip_multiplier": vip_multiplier,
            "consecutive_days": consecutive_days,
            "total_check_in_days": total_days,
            "total_points": new_balance,
            "message": f"签到成功！连续签到{consecutive_days}天，获得{points_earned}积分"
        }
    }

@router.get("/checkin/config")
async def get_checkin_config(db: Session = Depends(get_db)):
    """获取签到奖励配置（公开）"""
    configs = db.query(CheckInConfig)\
        .filter(CheckInConfig.enabled == True)\
        .order_by(CheckInConfig.consecutive_days)\
        .all()
    
    result = []
    for config in configs:
        result.append({
            "consecutive_days": config.consecutive_days,
            "base_points": config.base_points,
            "bonus_points": config.bonus_points,
            "total_points": config.total_points
        })
    
    return {
        "code": 200,
        "data": result
    }

@router.get("/checkin/status")
async def get_checkin_status(username: str, db: Session = Depends(get_db)):
    """获取签到状态"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    today = date.today()
    today_checked = (user.last_check_in_date == today)
    
    return {
        "code": 200,
        "data": {
            "today_checked": today_checked,
            "consecutive_days": user.consecutive_check_in if user.consecutive_check_in else 0,
            "total_days": user.total_check_in_days if user.total_check_in_days else 0,
            "last_check_in_date": user.last_check_in_date.isoformat() if user.last_check_in_date else None
        }
    }

@router.get("/checkin/calendar/{year}/{month}")
async def get_checkin_calendar(username: str, year: int, month: int, db: Session = Depends(get_db)):
    """获取签到日历"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 使用 SQLAlchemy 提取日期部分
    # 注意：SQLite 和 MySQL 的日期函数不同
    # 为了兼容性，这里我们查询该月范围内的所有记录，然后在 Python 中处理
    
    import calendar
    _, last_day = calendar.monthrange(year, month)
    start_date = date(year, month, 1)
    end_date = date(year, month, last_day)
    
    records = db.query(CheckInRecord)\
        .filter(
            CheckInRecord.user_id == user.id,
            CheckInRecord.check_in_date >= start_date,
            CheckInRecord.check_in_date <= end_date
        ).all()
        
    checked_dates = [record.check_in_date.day for record in records]
    
    return {
        "code": 200,
        "data": {
            "year": year,
            "month": month,
            "checked_dates": checked_dates
        }
    }

@router.get("/checkin/history")
async def get_checkin_history(username: str, page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    """签到记录"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    offset = (page - 1) * limit
    
    total = db.query(func.count(CheckInRecord.id)).filter(CheckInRecord.user_id == user.id).scalar()
    
    records = db.query(CheckInRecord)\
        .filter(CheckInRecord.user_id == user.id)\
        .order_by(CheckInRecord.check_in_date.desc())\
        .offset(offset)\
        .limit(limit)\
        .all()
    
    result_records = []
    for record in records:
        result_records.append({
            "check_in_date": record.check_in_date.isoformat(),
            "points_earned": record.points_earned,
            "consecutive_days": record.consecutive_days,
            "created_at": record.created_at.isoformat() if record.created_at else None
        })
    
    return {
        "code": 200,
        "data": {
            "total": total,
            "records": result_records
        }
    }

@router.get("/checkin/config")
async def get_checkin_config(db: Session = Depends(get_db)):
    """获取签到奖励规则 (公开接口)"""
    configs = db.query(CheckInConfig).filter(CheckInConfig.enabled == True).order_by(CheckInConfig.consecutive_days.asc()).all()
    
    data = []
    for c in configs:
        data.append({
            "consecutive_days": c.consecutive_days,
            "base_points": c.base_points,
            "bonus_points": c.bonus_points,
            "total_points": c.total_points
        })
        
    return {
        "code": 200,
        "data": data
    }

