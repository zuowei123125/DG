import os
import sys
# 将 Server 目录加入 sys.path，方便导入 app 包
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.environ["DATABASE_URL"] = "sqlite:///./test_auth.db"

from fastapi.testclient import TestClient
from app.main import app
from app.db import init_db, Base, engine
from app.models.session import UserSession
from sqlalchemy.orm import Session as OrmSession
import time

client = TestClient(app)

def test_register_and_login_single_device():
    # 使用测试数据库，清理旧文件并初始化表结构
    # 为避免 Windows 文件锁问题，不直接删除文件，改为重建表
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    init_db()
    # 注册
    r = client.post("/api/v1/auth/register", json={"username": "alice", "password": "secret123", "confirm_password": "secret123"})
    assert r.status_code == 200
    data = r.json()
    assert "access_token" in data and data["token_type"] == "bearer" and data["username"] == "alice"
    # 登录设备A
    l = client.post("/api/v1/auth/login", json={"username": "alice", "password": "secret123", "device_id": "devA"})
    assert l.status_code == 200
    ldata = l.json()
    assert "access_token" in ldata and ldata["username"] == "alice"
    # 设备B尝试登录，因设备A已在线，应返回 403（中文错误信息）
    l2 = client.post("/api/v1/auth/login", json={"username": "alice", "password": "secret123", "device_id": "devB"})
    assert l2.status_code == 403
    assert l2.json()["detail"] == "该账号已在其他设备在线"
    # 设备A登出
    out = client.post("/api/v1/auth/logout", json={"username": "alice", "device_id": "devA"})
    assert out.status_code == 200
    assert out.json()["detail"] == "已退出登录"
    # 设备B再次登录，应成功
    l3 = client.post("/api/v1/auth/login", json={"username": "alice", "password": "secret123", "device_id": "devB"})
    assert l3.status_code == 200

def test_login_wrong_password_returns_chinese_error():
    # 初始化干净数据库（重建表避免文件锁）
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    init_db()
    # 注册
    r = client.post("/api/v1/auth/register", json={"username": "bob", "password": "secret123", "confirm_password": "secret123"})
    assert r.status_code == 200
    # 错误密码登录
    l = client.post("/api/v1/auth/login", json={"username": "bob", "password": "wrong", "device_id": "devX"})
    assert l.status_code == 401
    assert l.json()["detail"] == "用户名或密码错误"

def test_online_time_endpoint_and_duration_record():
    # 准备干净库
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    init_db()
    # 注册并登录
    r = client.post("/api/v1/auth/register", json={"username": "carol", "password": "p@ss", "confirm_password": "p@ss"})
    assert r.status_code == 200
    l = client.post("/api/v1/auth/login", json={"username": "carol", "password": "p@ss", "device_id": "D1"})
    assert l.status_code == 200
    # 查询在线时长（活跃会话应 >= 0）
    s1 = client.get("/api/v1/auth/online-time/carol")
    assert s1.status_code == 200
    body = s1.json()
    assert body["username"] == "carol"
    assert body["active_seconds"] >= 0
    # 登出后，累计时长应 >= 0，活跃时长为 0
    out = client.post("/api/v1/auth/logout", json={"username": "carol", "device_id": "D1"})
    assert out.status_code == 200
    s2 = client.get("/api/v1/auth/online-time/carol")
    assert s2.status_code == 200
    body2 = s2.json()
    assert body2["total_seconds"] >= 0
    assert body2["active_seconds"] == 0

def test_heartbeat_updates_active_seconds_without_logout():
    # 干净库
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    init_db()
    # 登录
    r = client.post("/api/v1/auth/register", json={"username": "dave", "password": "p@ss", "confirm_password": "p@ss"})
    assert r.status_code == 200
    l = client.post("/api/v1/auth/login", json={"username": "dave", "password": "p@ss", "device_id": "D1"})
    assert l.status_code == 200
    # 初次查询
    s1 = client.get("/api/v1/auth/online-time/dave")
    v1 = s1.json()["active_seconds"]
    time.sleep(1)
    # 心跳更新
    hb = client.post("/api/v1/auth/heartbeat", json={"username": "dave", "device_id": "D1"})
    assert hb.status_code == 200
    # 再次查询，活跃时长应增加
    s2 = client.get("/api/v1/auth/online-time/dave")
    v2 = s2.json()["active_seconds"]
    assert v2 >= v1 + 1
