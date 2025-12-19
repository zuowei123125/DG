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
    Base.metadata.create_all(bind=engine)
    ensure_migrations()
    seed_data()

def seed_data():
    """Ensure default data exists"""
    from app.models.group import PluginGroup
    db = SessionLocal()
    try:
        default_group = db.query(PluginGroup).filter(PluginGroup.name == "default").first()
        if not default_group:
            print("Creating 'default' group...")
            new_group = PluginGroup(name="default", comment="Default User Group")
            db.add(new_group)
            db.commit()
            print("Default group created.")
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
