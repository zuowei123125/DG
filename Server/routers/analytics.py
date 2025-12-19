"""
用户行为分析 API
记录和分析用户操作
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime
import json

router = APIRouter(prefix="/analytics", tags=["analytics"])

# 简单的内存存储（生产环境应该用数据库）
action_logs = []

class ActionLog(BaseModel):
    username: str
    device_id: str
    action: str
    details: Optional[Any] = None
    timestamp: int
    session_id: str

class ActionLogResponse(BaseModel):
    success: bool
    message: str

@router.post("/log", response_model=ActionLogResponse)
async def log_action(log: ActionLog):
    """
    记录用户行为
    """
    try:
        # 添加服务器时间
        log_entry = {
            **log.dict(),
            "server_time": datetime.now().isoformat(),
            "ip": "unknown"  # 可以从请求中获取
        }
        
        action_logs.append(log_entry)
        
        # 只保留最近 10000 条
        if len(action_logs) > 10000:
            action_logs.pop(0)
        
        # 可以在这里添加异常检测逻辑
        # 例如：检测同一用户短时间内的大量操作
        
        return ActionLogResponse(success=True, message="已记录")
    except Exception as e:
        return ActionLogResponse(success=False, message=str(e))

@router.get("/stats/{username}")
async def get_user_stats(username: str):
    """
    获取用户统计信息
    """
    user_logs = [log for log in action_logs if log.get("username") == username]
    
    # 统计各操作类型的次数
    action_counts = {}
    for log in user_logs:
        action = log.get("action", "unknown")
        action_counts[action] = action_counts.get(action, 0) + 1
    
    return {
        "username": username,
        "total_actions": len(user_logs),
        "action_counts": action_counts,
        "recent_actions": user_logs[-10:]  # 最近 10 条
    }

@router.get("/recent")
async def get_recent_logs(limit: int = 100):
    """
    获取最近的操作日志（管理员用）
    """
    return {
        "total": len(action_logs),
        "logs": action_logs[-limit:]
    }

