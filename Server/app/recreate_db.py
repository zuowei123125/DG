# -*- coding: utf-8 -*-
"""
数据库重建脚本
功能：
1. 连接到 MySQL 服务器
2. 删除现有数据库（如果存在）
3. 创建新数据库
4. 根据模型定义创建所有表

使用方法：
在 Server 目录下运行：
docker-compose exec backend python -m app.recreate_db
"""

import logging
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import make_url
from app.core.config import settings
from app.db import Base
# 导入所有模型以确保它们被注册到 Base.metadata
from app.models import user, group, business, session

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def recreate_database():
    logger.info("🚀 开始重建数据库...")
    
    # 1. 获取数据库配置
    db_url = settings.DATABASE_URL
    
    if not db_url.startswith("mysql"):
        logger.error("❌ 此脚本仅支持 MySQL 数据库重建")
        return

    try:
        # 解析 URL
        url = make_url(db_url)
        db_name = url.database
        
        # 构建连接到 MySQL 系统库的 URL (不指定具体数据库，以便执行 DROP/CREATE)
        # 我们连接到 'mysql' 库或者不指定库
        # 注意：需要有足够的权限
        root_url = url.set(database='mysql')
        
        logger.info(f"🔌 连接到数据库服务器: {url.host}")
        
        # 使用 AUTOCOMMIT 隔离级别，因为 CREATE/DROP DATABASE 不能在事务中运行
        engine = create_engine(root_url, isolation_level="AUTOCOMMIT")
        
        with engine.connect() as conn:
            # 删除旧数据库
            logger.info(f"🗑️  删除数据库: {db_name}")
            conn.execute(text(f"DROP DATABASE IF EXISTS {db_name}"))
            
            # 创建新数据库
            logger.info(f"✨ 创建数据库: {db_name}")
            conn.execute(text(f"CREATE DATABASE {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
            
        # 2. 创建表结构
        logger.info("🏗️  创建表结构...")
        
        # 连接到新创建的数据库
        target_engine = create_engine(db_url)
        Base.metadata.create_all(bind=target_engine)
        
        logger.info("✅ 数据库重建完成！所有表已创建。")
        logger.info("📋 包含的表: " + ", ".join(Base.metadata.tables.keys()))
        
    except Exception as e:
        logger.error(f"❌ 重建数据库失败: {str(e)}")
        raise

if __name__ == "__main__":
    recreate_database()
