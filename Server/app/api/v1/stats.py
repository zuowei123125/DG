# -*- coding: utf-8 -*-
"""
统计接口
功能：数据统计和分析
"""

from fastapi import APIRouter, Header, HTTPException
from datetime import date, timedelta
import pymysql
from app.core.database import get_db_connection

router = APIRouter()

# ==================== 辅助函数 ====================

def verify_admin_token(token: str):
    """验证管理员Token"""
    expected_token = "admin-secret-token"
    if token != expected_token:
        raise HTTPException(status_code=401, detail="管理员Token无效")

# ==================== 统计功能 ====================

@router.get("/admin/stats/today")
async def get_today_stats(token: str = Header(..., alias="x-admin-token")):
    """今日统计"""
    verify_admin_token(token)
    
    conn = get_db_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            today = date.today()
            
            # 总用户数
            cursor.execute("SELECT COUNT(*) as total FROM users")
            total_users = cursor.fetchone()['total']
            
            # 今日签到数
            cursor.execute("""
                SELECT COUNT(DISTINCT user_id) as count
                FROM check_in_records
                WHERE check_in_date = %s
            """, (today,))
            checkin_count = cursor.fetchone()['count']
            
            # 今日功能使用次数
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM feature_usage_logs
                WHERE DATE(created_at) = %s
            """, (today,))
            feature_usage_count = cursor.fetchone()['count']
            
            # VIP用户数
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM users
                WHERE vip_type IN ('vip', 'svip')
                  AND (vip_expire IS NULL OR vip_expire > NOW())
            """)
            vip_count = cursor.fetchone()['count']
            
            return {
                "code": 200,
                "data": {
                    "total_users": total_users,
                    "checkin_count": checkin_count,
                    "feature_usage_count": feature_usage_count,
                    "vip_count": vip_count
                }
            }
    finally:
        conn.close()

@router.get("/admin/stats/feature-usage")
async def get_feature_usage_stats(
    days: int = 7,
    token: str = Header(..., alias="x-admin-token")
):
    """功能使用排行"""
    verify_admin_token(token)
    
    conn = get_db_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            start_date = date.today() - timedelta(days=days-1)
            
            cursor.execute("""
                SELECT 
                    l.feature_key,
                    f.feature_name,
                    COUNT(*) as usage_count
                FROM feature_usage_logs l
                LEFT JOIN features_config f ON l.feature_key = f.feature_key
                WHERE DATE(l.created_at) >= %s
                GROUP BY l.feature_key, f.feature_name
                ORDER BY usage_count DESC
                LIMIT 10
            """, (start_date,))
            
            return {
                "code": 200,
                "data": cursor.fetchall()
            }
    finally:
        conn.close()

@router.get("/admin/stats/points-trend")
async def get_points_trend(
    days: int = 7,
    token: str = Header(..., alias="x-admin-token")
):
    """积分趋势统计"""
    verify_admin_token(token)
    
    conn = get_db_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            start_date = date.today() - timedelta(days=days-1)
            
            cursor.execute("""
                SELECT 
                    DATE(created_at) as date,
                    SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) as earned,
                    SUM(CASE WHEN amount < 0 THEN -amount ELSE 0 END) as consumed
                FROM points_history
                WHERE DATE(created_at) >= %s
                GROUP BY DATE(created_at)
                ORDER BY date
            """, (start_date,))
            
            records = cursor.fetchall()
            for record in records:
                record['date'] = record['date'].isoformat()
            
            return {
                "code": 200,
                "data": records
            }
    finally:
        conn.close()

