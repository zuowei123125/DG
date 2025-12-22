# -*- coding: utf-8 -*-
"""
数据库连接管理
"""

import pymysql
import os

def get_db_connection():
    """获取数据库连接"""
    return pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=int(os.getenv('DB_PORT', 3306)),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'designercep'),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.Cursor
    )

