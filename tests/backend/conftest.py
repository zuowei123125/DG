# -*- coding: utf-8 -*-
"""
Pytest 配置文件
提供测试fixtures和公共设置
"""

import pytest
import pymysql
import os
from typing import Generator

# 测试数据库配置
TEST_DB_CONFIG = {
    'host': os.getenv('TEST_DB_HOST', 'localhost'),
    'user': os.getenv('TEST_DB_USER', 'root'),
    'password': os.getenv('TEST_DB_PASSWORD', ''),
    'database': os.getenv('TEST_DB_NAME', 'designercep_test'),
    'charset': 'utf8mb4'
}

# API配置
API_BASE_URL = os.getenv('TEST_API_URL', 'https://backend.aidg168.uk/api/v1')
ADMIN_TOKEN = 'admin-secret-token'


@pytest.fixture(scope='session')
def db_connection():
    """数据库连接fixture（会话级别）"""
    conn = pymysql.connect(**TEST_DB_CONFIG)
    yield conn
    conn.close()


@pytest.fixture(scope='function')
def db_cursor(db_connection):
    """数据库游标fixture（函数级别，自动回滚）"""
    cursor = db_connection.cursor(pymysql.cursors.DictCursor)
    yield cursor
    db_connection.rollback()  # 测试后回滚
    cursor.close()


@pytest.fixture(scope='function')
def test_user(db_cursor):
    """创建测试用户"""
    username = 'test_user_pytest'
    password = 'test123456'
    email = 'test@example.com'
    
    # 清理可能存在的旧数据
    db_cursor.execute("DELETE FROM users WHERE username = %s", (username,))
    db_cursor.connection.commit()
    
    # 创建测试用户
    db_cursor.execute("""
        INSERT INTO users (username, password, email, points, vip_type, 
                          consecutive_check_in, total_check_in_days)
        VALUES (%s, %s, %s, 100, 'none', 0, 0)
    """, (username, password, email))
    db_cursor.connection.commit()
    
    # 获取用户信息
    db_cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = db_cursor.fetchone()
    
    yield user
    
    # 清理
    db_cursor.execute("DELETE FROM users WHERE username = %s", (username,))
    db_cursor.connection.commit()


@pytest.fixture(scope='function')
def vip_user(db_cursor):
    """创建VIP测试用户"""
    username = 'test_vip_user'
    
    # 清理
    db_cursor.execute("DELETE FROM users WHERE username = %s", (username,))
    db_cursor.connection.commit()
    
    # 创建VIP用户
    db_cursor.execute("""
        INSERT INTO users (username, password, email, points, vip_type, 
                          vip_daily_quota, vip_quota_reset_date)
        VALUES (%s, 'test123', 'vip@test.com', 200, 'vip', 20, CURDATE())
    """, (username,))
    db_cursor.connection.commit()
    
    db_cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = db_cursor.fetchone()
    
    yield user
    
    # 清理
    db_cursor.execute("DELETE FROM users WHERE username = %s", (username,))
    db_cursor.connection.commit()


@pytest.fixture(scope='function')
def test_feature(db_cursor):
    """创建测试功能配置"""
    feature_key = 'test_feature_pytest'
    
    # 清理
    db_cursor.execute("DELETE FROM features_config WHERE feature_key = %s", (feature_key,))
    db_cursor.connection.commit()
    
    # 创建测试功能
    db_cursor.execute("""
        INSERT INTO features_config 
        (feature_key, feature_name, category, points_cost, vip_points_cost, 
         svip_points_cost, enabled)
        VALUES (%s, '测试功能', 'test', 50, 0, 0, 1)
    """, (feature_key,))
    db_cursor.connection.commit()
    
    db_cursor.execute("SELECT * FROM features_config WHERE feature_key = %s", (feature_key,))
    feature = db_cursor.fetchone()
    
    yield feature
    
    # 清理
    db_cursor.execute("DELETE FROM features_config WHERE feature_key = %s", (feature_key,))
    db_cursor.connection.commit()


@pytest.fixture
def admin_headers():
    """管理员请求头"""
    return {'x-admin-token': ADMIN_TOKEN}


@pytest.fixture
def user_headers(test_user):
    """用户请求头（需要实际token生成逻辑）"""
    # 这里简化处理，实际应该调用登录接口获取token
    return {'Authorization': 'Bearer test_token'}


# 测试数据清理
def pytest_sessionfinish(session, exitstatus):
    """测试会话结束后清理"""
    try:
        conn = pymysql.connect(**TEST_DB_CONFIG)
        cursor = conn.cursor()
        
        # 清理测试数据
        cursor.execute("DELETE FROM users WHERE username LIKE 'test_%'")
        cursor.execute("DELETE FROM features_config WHERE feature_key LIKE 'test_%'")
        cursor.execute("DELETE FROM check_in_records WHERE username LIKE 'test_%'")
        cursor.execute("DELETE FROM points_history WHERE username LIKE 'test_%'")
        cursor.execute("DELETE FROM feature_usage_logs WHERE username LIKE 'test_%'")
        
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"清理测试数据失败: {e}")

