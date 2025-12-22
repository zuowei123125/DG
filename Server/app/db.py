from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# 数据库连接字符串，默认使用 SQLite 本地文件
SQLALCHEMY_DATABASE_URL = getattr(settings, "DATABASE_URL", "sqlite:///./designercep.db")

# 创建数据库引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}
)

# 会话工厂与 ORM 基类
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    # FastAPI 依赖注入使用的数据库会话
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    # 初始化数据库（创建所有 ORM 映射的表）
    from app.models.user import User
    from app.models.group import PluginGroup
    from app.models.session import UserSession
    from app.models.business import FeatureConfig, VipConfig, CheckInConfig, CheckInRecord, PointsHistory
    Base.metadata.create_all(bind=engine)
    ensure_migrations()
    seed_data()

def seed_data():
    """Ensure default data exists"""
    from app.models.group import PluginGroup
    from app.models.business import FeatureConfig, VipConfig, CheckInConfig
    db = SessionLocal()
    try:
        # Seed Groups
        default_group = db.query(PluginGroup).filter(PluginGroup.name == "default").first()
        if not default_group:
            print("Creating 'default' group...")
            new_group = PluginGroup(name="default", comment="Default User Group")
            db.add(new_group)
            
        # Seed VIP Config
        if db.query(VipConfig).count() == 0:
            print("Seeding VIP Config...")
            db.add(VipConfig(vip_type="vip", name="VIP会员", price=30.0, daily_quota=20, points_multiplier=1.5))
            db.add(VipConfig(vip_type="svip", name="SVIP会员", price=88.0, daily_quota=-1, points_multiplier=2.0))
            
        # Seed Checkin Config
        if db.query(CheckInConfig).count() == 0:
            print("Seeding Checkin Config...")
            db.add(CheckInConfig(consecutive_days=1, base_points=10, bonus_points=0, total_points=10))
            db.add(CheckInConfig(consecutive_days=3, base_points=10, bonus_points=5, total_points=15))
            db.add(CheckInConfig(consecutive_days=7, base_points=10, bonus_points=20, total_points=30))
            
        # Seed Features
        if db.query(FeatureConfig).count() == 0:
            print("Seeding Features...")
            db.add(FeatureConfig(feature_key="ai_remove_bg", feature_name="智能抠图", points_cost=10, category="ai"))
            
        db.commit()
    except Exception as e:
        print(f"Error seeding data: {e}")
    finally:
        db.close()

def ensure_migrations():
    # 轻量级迁移：为 SQLite 动态添加缺失列
    if not SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
        return
    with engine.connect() as conn:
        def has_column(table: str, col: str) -> bool:
            try:
                rows = conn.exec_driver_sql(f"PRAGMA table_info('{table}')").fetchall()
                names = {r[1] for r in rows} if rows else set()
                return col in names
            except Exception:
                return False
                
        def add_col(table: str, col: str, type_sql: str):
            try:
                conn.exec_driver_sql(f"ALTER TABLE {table} ADD COLUMN {col} {type_sql}")
            except Exception as e:
                print(f"Migration error for {table}.{col}: {e}")

        # user_sessions 需要的列
        if not has_column("user_sessions", "login_at"):
            add_col("user_sessions", "login_at", "TIMESTAMP NULL")
        if not has_column("user_sessions", "logout_at"):
            add_col("user_sessions", "logout_at", "TIMESTAMP NULL")
        if not has_column("user_sessions", "duration_seconds"):
            add_col("user_sessions", "duration_seconds", "INTEGER NULL")
        if not has_column("user_sessions", "last_seen_at"):
            add_col("user_sessions", "last_seen_at", "TIMESTAMP NULL")

        # users 需要的列
        if not has_column("users", "group_id"):
            add_col("users", "group_id", "INTEGER NULL REFERENCES plugin_groups(id)")
        if not has_column("users", "permissions"):
            add_col("users", "permissions", "TEXT NULL")
        if not has_column("users", "expire_date"):
            add_col("users", "expire_date", "TIMESTAMP NULL")
            
        # users email & verification columns
        if not has_column("users", "email"):
            add_col("users", "email", "VARCHAR(255) NULL")
        if not has_column("users", "is_verified"):
            add_col("users", "is_verified", "BOOLEAN DEFAULT 0")
        if not has_column("users", "verification_code"):
            add_col("users", "verification_code", "VARCHAR(6) NULL")
        if not has_column("users", "reset_token"):
            add_col("users", "reset_token", "VARCHAR(128) NULL")
        if not has_column("users", "reset_token_expire"):
            add_col("users", "reset_token_expire", "TIMESTAMP NULL")

        # users profile & vip columns
        if not has_column("users", "nickname"):
            add_col("users", "nickname", "VARCHAR(50) NULL")
        if not has_column("users", "avatar"):
            add_col("users", "avatar", "VARCHAR(500) NULL")
        if not has_column("users", "points"):
            add_col("users", "points", "INTEGER DEFAULT 0")
        if not has_column("users", "level"):
            add_col("users", "level", "INTEGER DEFAULT 1")
        if not has_column("users", "vip_type"):
            add_col("users", "vip_type", "VARCHAR(20) DEFAULT 'none'")
        if not has_column("users", "vip_expire"):
            add_col("users", "vip_expire", "TIMESTAMP NULL")
        if not has_column("users", "vip_daily_quota"):
            add_col("users", "vip_daily_quota", "INTEGER DEFAULT 0")
        if not has_column("users", "vip_quota_reset_date"):
            add_col("users", "vip_quota_reset_date", "DATE NULL")
        if not has_column("users", "total_check_in_days"):
            add_col("users", "total_check_in_days", "INTEGER DEFAULT 0")
        if not has_column("users", "consecutive_check_in"):
            add_col("users", "consecutive_check_in", "INTEGER DEFAULT 0")
        if not has_column("users", "last_check_in_date"):
            add_col("users", "last_check_in_date", "DATE NULL")
