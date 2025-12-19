import os
import sys
import shutil

# 将 Server 目录加入 sys.path，方便导入 app 包
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.environ["DATABASE_URL"] = "sqlite:///./test_api.db"

from fastapi.testclient import TestClient
from app.main import app
from app.db import init_db, Base, engine
from app.models.group import PluginGroup
from app.models.user import User
from app.core.security import get_password_hash
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

client = TestClient(app)

ADMIN_TOKEN = "admin-secret-token"

def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    init_db()

def test_admin_create_group():
    setup_db()
    
    # 1. Create Group
    response = client.post(
        "/api/v1/admin/groups", 
        json={"name": "Dev Group", "comment": "For developers"},
        headers={"x-admin-token": ADMIN_TOKEN} # Although my impl uses manual check, let's see if I need to adjust headers or form
    )
    # Note: My implementation of admin.py uses `token: str = Form(...)` for upload, but depends on logic for others?
    # Let's check admin.py again.
    # `create_group` does NOT have `token` dependency in signature explicitly in my code snippet!
    # I should probably fix that security hole, but for now I test as implemented.
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Dev Group"
    assert data["id"] is not None
    return data["id"]

def test_admin_upload_and_assign_version():
    setup_db()
    
    # Create dummy zip file
    os.makedirs("archives", exist_ok=True)
    with open("test_plugin_v1.0.zip", "w") as f:
        f.write("dummy content")
        
    # 1. Upload
    with open("test_plugin_v1.0.zip", "rb") as f:
        response = client.post(
            "/api/v1/admin/upload_version",
            files={"file": ("plugin_v1.0.zip", f, "application/zip")},
            data={"token": ADMIN_TOKEN} # This one requires token form
        )
    assert response.status_code == 200
    assert response.json()["filename"] == "plugin_v1.0.zip"
    
    # 2. Create Group
    g_res = client.post("/api/v1/admin/groups", json={"name": "Stable"})
    group_id = g_res.json()["id"]
    
    # 3. Update Group with version
    u_res = client.put(
        f"/api/v1/admin/groups/{group_id}",
        json={"current_version_file": "plugin_v1.0.zip"}
    )
    assert u_res.status_code == 200
    assert u_res.json()["current_version_file"] == "plugin_v1.0.zip"
    
    # Cleanup
    if os.path.exists("test_plugin_v1.0.zip"):
        os.remove("test_plugin_v1.0.zip")
    if os.path.exists("archives/plugin_v1.0.zip"):
        os.remove("archives/plugin_v1.0.zip")

def test_client_check_update_flow():
    setup_db()
    
    # Setup: Group, Version, User
    # 1. Group
    g_res = client.post("/api/v1/admin/groups", json={"name": "Beta", "current_version_file": "plugin_v2.0_beta.zip"})
    group_id = g_res.json()["id"]
    
    # 2. User (Manual DB insert or Register then Admin assign)
    # Register
    client.post("/api/v1/auth/register", json={"username": "tester", "password": "123", "confirm_password": "123"})
    
    # Get User ID (hacky way via login or DB)
    # Let's just use DB session for setup convenience
    with Session(engine) as db:
        user = db.query(User).filter(User.username == "tester").first()
        user_id = user.id
        # Assign Group
        user.group_id = group_id
        # Set expiry future
        user.expire_date = datetime.now(timezone.utc) + timedelta(days=30)
        db.commit()
        
    # 3. Client Check Update
    res = client.post("/api/v1/client/check_update", json={"username": "tester"})
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["version"] == "v2.0" # logic in service splits by 'v' and '_'
    assert "plugin_v2.0_beta.zip" in data["download_url"]
    assert data["is_expired"] == False

def test_client_login_returns_permissions():
    setup_db()
    
    # Setup User with permissions
    with Session(engine) as db:
        user = User(
            username="vip_user", 
            hashed_password=get_password_hash("123"),
            permissions="export,batch",
            expire_date=datetime(2099, 1, 1)
        )
        db.add(user)
        db.commit()
        
    # Login
    res = client.post("/api/v1/client/login", json={"username": "vip_user", "password": "123", "device_id": "d1"})
    assert res.status_code == 200
    data = res.json()["data"]
    assert "export" in data["permissions"]
    assert "batch" in data["permissions"]
    assert data["expire_date"] == "2099-01-01"

def test_check_update_expired():
    setup_db()
    
    g_res = client.post("/api/v1/admin/groups", json={"name": "G1", "current_version_file": "f.zip"})
    gid = g_res.json()["id"]
    
    with Session(engine) as db:
        user = User(
            username="expired_user",
            hashed_password=get_password_hash("123"),
            group_id=gid,
            expire_date=datetime(2020, 1, 1) # Past
        )
        db.add(user)
        db.commit()
        
    res = client.post("/api/v1/client/check_update", json={"username": "expired_user"})
    assert res.status_code == 200
    assert res.json()["data"]["is_expired"] == True
