# -*- coding: utf-8 -*-
"""
完整数据库初始化脚本 (Local Execution)
功能：
1. 重建数据库（DROP & CREATE DATABASE）
2. 创建所有表结构
3. 创建默认数据（用户组、VIP配置、签到配置、功能配置）
4. 创建默认管理员账户 (admin/password123)

注意：此脚本设计为在本地或 Docker 容器内运行，直接连接 MySQL。
它会读取环境变量或使用默认配置。
"""

import logging
import os
import sys
import argparse
from datetime import datetime
from sqlalchemy.schema import CreateTable

# 确保可以将当前目录添加到 sys.path
sys.path.append(os.getcwd())

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import make_url

# 尝试导入应用模块
try:
    from app.core.config import settings
    from app.db import Base
    from app.models import user, group, business, session
    from app.models.user import User
    from app.models.group import PluginGroup
    from app.models.business import FeatureConfig, VipConfig, CheckInConfig
    from app.core.security import get_password_hash
except ImportError:
    print("❌ 无法导入应用模块，请确保在 Server 目录下运行此脚本")
    print("示例: python scripts/init_full_db.py")
    sys.exit(1)

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_sql_file():
    """生成完整的初始化 SQL 文件"""
    logger.info("📝 正在生成 SQL 文件 (init_db.sql) ...")
    
    # 获取数据库引擎 (用于编译 SQL)
    # 我们使用一个 mock engine，因为我们只想要 SQL 语句
    engine = create_engine("mysql+pymysql://", strategy="mock", executor=lambda sql, *args, **kwargs: print(sql.compile(dialect=engine.dialect)))
    
    # 真正的 engine 用于 dialect 编译
    compile_engine = create_engine("mysql+pymysql://")

    sql_content = []
    
    # 1. 准备数据库
    sql_content.append("-- ==========================================")
    sql_content.append("-- Database Initialization Script")
    sql_content.append(f"-- Generated at: {datetime.now()}")
    sql_content.append("-- ==========================================\n")
    
    # 既然 DROP DATABASE 被禁用，我们切换到目标数据库，并尝试删除所有表
    sql_content.append("-- 1. Select Database and Cleanup Tables")
    sql_content.append("USE designer_db;\n")
    
    # 获取所有表名并生成 DROP TABLE 语句
    # 注意：为了处理外键约束，我们先禁用外键检查
    sql_content.append("SET FOREIGN_KEY_CHECKS = 0;")
    
    for table in Base.metadata.sorted_tables:
        sql_content.append(f"DROP TABLE IF EXISTS {table.name};")
    
    sql_content.append("SET FOREIGN_KEY_CHECKS = 1;\n")
    
    # 2. 创建表结构
    sql_content.append("-- 2. Create Tables")
    for table in Base.metadata.sorted_tables:
        create_table_sql = CreateTable(table).compile(compile_engine)
        sql_content.append(str(create_table_sql).strip() + ";\n")
        
    # 3. 插入初始数据
    sql_content.append("-- 3. Insert Initial Data")
    
    # 用户组
    sql_content.append("-- Default User Group")
    sql_content.append("INSERT INTO plugin_groups (name, comment) VALUES ('default', 'Default User Group');")
    
    # VIP 配置
    sql_content.append("-- VIP Config")
    sql_content.append("INSERT INTO vip_config (vip_type, name, price, daily_quota, points_multiplier) VALUES ('vip', 'VIP会员', 30.0, 20, 1.5);")
    sql_content.append("INSERT INTO vip_config (vip_type, name, price, daily_quota, points_multiplier) VALUES ('svip', 'SVIP会员', 88.0, -1, 2.0);")
    
    # 签到配置
    sql_content.append("-- Check-in Config")
    sql_content.append("INSERT INTO checkin_config (consecutive_days, base_points, bonus_points, total_points) VALUES (1, 10, 0, 10);")
    sql_content.append("INSERT INTO checkin_config (consecutive_days, base_points, bonus_points, total_points) VALUES (3, 10, 5, 15);")
    sql_content.append("INSERT INTO checkin_config (consecutive_days, base_points, bonus_points, total_points) VALUES (7, 10, 20, 30);")
    
    # 功能配置
    sql_content.append("-- Feature Config")
    sql_content.append("INSERT INTO feature_configs (feature_key, feature_name, points_cost, category) VALUES ('ai_remove_bg', '智能抠图', 10, 'ai');")
    
    # 4. 创建管理员
    sql_content.append("-- 4. Create Admin User (admin / password123)")
    # 计算密码哈希 (这里直接计算一次固定的，避免每次运行不一样)
    # password123 的 bcrypt hash (示例)
    # 为了准确，我们还是用 python 算一下
    admin_hash = get_password_hash("password123")
    
    # 获取 default group id (假设是 1，因为刚刚插入且是第一个)
    sql_content.append(f"""
INSERT INTO users (
    username, hashed_password, email, is_verified, permissions, 
    group_id, nickname, level, vip_type, vip_expire, 
    created_at, points, total_check_in_days, consecutive_check_in, vip_daily_quota
) VALUES (
    'admin', 
    '{admin_hash}', 
    'admin@example.com', 
    1, 
    'admin,vip,svip', 
    (SELECT id FROM plugin_groups WHERE name = 'default' LIMIT 1), 
    'Administrator', 
    999, 
    'svip', 
    '2099-12-31 23:59:59', 
    NOW(), 
    0, 0, 0, 0
);
""")

    # 写入文件
    output_file = "init_db.sql"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(sql_content))
        
    logger.info(f"✅ SQL 文件已生成: {output_file}")
    print(f"\nSQL 文件已生成: {os.path.abspath(output_file)}")
    print("您可以直接在 phpMyAdmin 中导入此文件来初始化数据库。")


def get_db_url():
    """获取数据库连接 URL"""
    # 优先使用 settings 中的配置
    # db_url = settings.DATABASE_URL
    
    # 用户指定的远程数据库
    # Host: 103.97.201.136
    # Port: 3388 (映射到了容器内的 3306)
    # User: designer_user
    # Pass: DesignerPass123!
    db_url = "mysql+pymysql://designer_user:DesignerPass123!@103.97.201.136:3388/designer_db"
    
    # 如果 settings 是默认的 sqlite，尝试构建 mysql 连接（用于本地开发时的强制覆盖）
    # if db_url.startswith("sqlite"):
    #     # 默认开发环境 Docker MySQL 配置
    #     db_url = "mysql+pymysql://designer_user:DesignerPass123!@localhost:3306/designer_db"
    #     logger.info(f"⚠️ 检测到 SQLite 配置，切换为默认 MySQL 配置: {db_url}")
        
    logger.info(f"🔌 使用数据库配置: {db_url}")
    return db_url

def recreate_database(engine, db_name):
    """重建数据库"""
    logger.info(f"🗑️  正在重建数据库: {db_name}...")
    
    # 获取 root 连接（连接到 mysql 系统库或不指定库）
    url = make_url(engine.url)
    root_url = url.set(database='mysql')
    
    # 使用 AUTOCOMMIT 隔离级别
    root_engine = create_engine(root_url, isolation_level="AUTOCOMMIT")
    
    with root_engine.connect() as conn:
        conn.execute(text(f"DROP DATABASE IF EXISTS {db_name}"))
        conn.execute(text(f"CREATE DATABASE {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
        logger.info(f"✅ 数据库 {db_name} 重建完成")

def seed_initial_data(session):
    """填充初始数据"""
    logger.info("🌱 正在填充初始数据...")
    
    # 1. 默认用户组
    if session.query(PluginGroup).filter(PluginGroup.name == "default").count() == 0:
        logger.info("  - 创建默认用户组 'default'")
        default_group = PluginGroup(name="default", comment="Default User Group")
        session.add(default_group)
    
    # 2. VIP 配置
    if session.query(VipConfig).count() == 0:
        logger.info("  - 创建 VIP 配置")
        session.add(VipConfig(vip_type="vip", name="VIP会员", price=30.0, daily_quota=20, points_multiplier=1.5))
        session.add(VipConfig(vip_type="svip", name="SVIP会员", price=88.0, daily_quota=-1, points_multiplier=2.0))

    # 3. 签到配置
    if session.query(CheckInConfig).count() == 0:
        logger.info("  - 创建签到配置")
        session.add(CheckInConfig(consecutive_days=1, base_points=10, bonus_points=0, total_points=10))
        session.add(CheckInConfig(consecutive_days=3, base_points=10, bonus_points=5, total_points=15))
        session.add(CheckInConfig(consecutive_days=7, base_points=10, bonus_points=20, total_points=30))

    # 4. 功能配置
    if session.query(FeatureConfig).count() == 0:
        logger.info("  - 创建功能配置")
        session.add(FeatureConfig(feature_key="ai_remove_bg", feature_name="智能抠图", points_cost=10, category="ai"))

    session.commit()
    logger.info("✅ 初始数据填充完成")

def create_admin_user(session):
    """创建管理员用户"""
    username = "admin"
    password = "123456"
    email = "admin@example.com"
    
    existing = session.query(User).filter(User.username == username).first()
    if existing:
        logger.info(f"ℹ️  管理员用户 '{username}' 已存在，跳过创建")
        return

    logger.info(f"👤 正在创建管理员用户: {username} ...")
    
    # 获取默认组
    default_group = session.query(PluginGroup).filter(PluginGroup.name == "default").first()
    group_id = default_group.id if default_group else None

    new_user = User(
        username=username,
        hashed_password=get_password_hash(password),
        email=email,
        is_verified=True,
        permissions="admin,vip,svip", # 赋予所有权限
        group_id=group_id,
        nickname="Administrator",
        level=999,
        vip_type="svip",
        vip_expire=datetime(2099, 12, 31)
    )
    
    session.add(new_user)
    session.commit()
    logger.info(f"✅ 管理员用户创建成功！(User: {username}, Pass: {password})")

def main():
    parser = argparse.ArgumentParser(description='Initialize DesignerCEP Database')
    parser.add_argument('--generate-sql', action='store_true', help='Generate init_db.sql file only')
    args = parser.parse_args()

    if args.generate_sql:
        generate_sql_file()
        return

    logger.info("🚀 开始全量数据库初始化流程")
    
    try:
        db_url = get_db_url()
        engine = create_engine(db_url)
        
        # 1. 重建数据库
        # 注意：这会删除现有数据！
        db_name = make_url(db_url).database
        recreate_database(engine, db_name)
        
        # 重新连接到新创建的数据库
        target_engine = create_engine(db_url)
        
        # 2. 创建表结构
        logger.info("🏗️  正在创建表结构...")
        Base.metadata.create_all(bind=target_engine)
        logger.info("✅ 表结构创建完成")
        
        # 3. 数据填充
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=target_engine)
        session = SessionLocal()
        
        try:
            seed_initial_data(session)
            create_admin_user(session)
        finally:
            session.close()
            
        logger.info("✨✨✨ 数据库初始化全部完成！ ✨✨✨")
        
    except Exception as e:
        logger.error(f"❌ 初始化失败: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
