# -*- coding: utf-8 -*-
"""
数据库初始化脚本
功能：
1. 检查数据库连接
2. 创建所有定义的表（如果不存在）
3. 检查现有表的字段，如果缺失则自动添加
"""

import os
import sys
import logging
from sqlalchemy import create_engine, inspect, text
from app.core.config import settings
from app.db import Base
# 导入所有模型以确保它们被注册到 Base.metadata
from app.models import user, group, business, session

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_engine():
    """获取数据库引擎"""
    # 优先使用环境变量中的配置，如果没有则构建
    db_url = settings.DATABASE_URL
    if not db_url:
        host = os.getenv('DB_HOST', 'localhost')
        port = os.getenv('DB_PORT', '3306')
        user = os.getenv('DB_USER', 'root')
        password = os.getenv('DB_PASSWORD', '')
        db_name = os.getenv('DB_NAME', 'designer_db')
        db_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"
    
    return create_engine(db_url)

def map_python_type_to_sql(col_type):
    """将 SQLAlchemy 类型映射为 MySQL 类型"""
    type_str = str(col_type).lower()
    if 'varchar' in type_str:
        return type_str
    if 'string' in type_str:
        length = getattr(col_type, 'length', 255)
        return f"varchar({length})"
    if 'integer' in type_str or 'int' in type_str:
        return "int"
    if 'boolean' in type_str:
        return "tinyint(1)"
    if 'datetime' in type_str:
        return "datetime"
    if 'date' in type_str:
        return "date"
    if 'float' in type_str:
        return "float"
    if 'text' in type_str:
        return "text"
    return "varchar(255)" # 默认

def init_db():
    logger.info("🔄 开始数据库初始化检查...")
    
    try:
        engine = get_engine()
        inspector = inspect(engine)
        
        # 1. 创建缺失的表
        logger.info("📊 检查表结构...")
        Base.metadata.create_all(bind=engine)
        logger.info("✅ 基础表结构检查完成")
        
        # 2. 检查并补充缺失的列
        logger.info("🔍 检查缺失字段...")
        
        existing_tables = inspector.get_table_names()
        
        with engine.connect() as conn:
            for table_name, table in Base.metadata.tables.items():
                if table_name not in existing_tables:
                    continue
                
                # 获取数据库中现有的列
                existing_columns = [col['name'] for col in inspector.get_columns(table_name)]
                
                # 检查模型定义的列
                for column in table.columns:
                    if column.name not in existing_columns:
                        logger.info(f"  ➕ 发现缺失字段: {table_name}.{column.name}")
                        
                        # 构建 ALTER TABLE 语句
                        col_type = map_python_type_to_sql(column.type)
                        default_val = ""
                        
                        # 处理默认值 (简化处理，只处理常见类型)
                        if column.default:
                            arg = column.default.arg
                            if isinstance(arg, (int, float, bool)):
                                if isinstance(arg, bool):
                                    arg = 1 if arg else 0
                                default_val = f" DEFAULT {arg}"
                            elif isinstance(arg, str):
                                default_val = f" DEFAULT '{arg}'"
                        
                        nullable = "NULL" if column.nullable else "NOT NULL"
                        if column.nullable and not default_val:
                            default_val = " DEFAULT NULL"
                            
                        sql = f"ALTER TABLE {table_name} ADD COLUMN {column.name} {col_type} {nullable}{default_val};"
                        logger.info(f"  🚀 执行: {sql}")
                        conn.execute(text(sql))
        
            conn.commit()
        logger.info("✅ 数据库同步完成！")
        
    except Exception as e:
        logger.error(f"❌ 数据库初始化失败: {e}")
        # 不抛出异常，以免阻断容器启动（如果是网络波动等临时问题）
        # 但在生产环境中可能需要抛出

if __name__ == "__main__":
    init_db()
