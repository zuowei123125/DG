import os
import sys
import datetime
from datetime import timezone, timedelta

# 将 Server 目录加入 sys.path，方便导入 app 包
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.environ["DATABASE_URL"] = "sqlite:///./test_verify.db"

from fastapi.testclient import TestClient
from app.main import app
from app.db import init_db, Base, engine, SessionLocal
from app.models.user import User

client = TestClient(app)

def test_verify_endpoint():
    # Setup
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    init_db()

    # 1. Register
    client.post("/api/v1/auth/register", json={"username": "eve", "password": "pass", "confirm_password": "pass"})
    
    # 2. Login
    resp = client.post("/api/v1/auth/login", json={"username": "eve", "password": "pass", "device_id": "dev1"})
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Verify Success
    verify_data = {
        "username": "eve",
        "device_id": "dev1",
        "timestamp": 1234567890
    }
    resp = client.post("/api/v1/auth/verify", json=verify_data, headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["valid"] == True
    assert data["username"] == "eve"

    # 4. Verify Fail - Session not found (wrong device_id)
    verify_data_bad_dev = {
        "username": "eve",
        "device_id": "dev2",
        "timestamp": 1234567890
    }
    resp = client.post("/api/v1/auth/verify", json=verify_data_bad_dev, headers=headers)
    assert resp.status_code == 404
    assert "会话不存在" in resp.json()["detail"]

    # 5. Verify Expiry
    # Hack DB to set expire_date
    db = SessionLocal()
    user = db.query(User).filter(User.username == "eve").first()
    # Expired yesterday
    user.expire_date = datetime.datetime.now(timezone.utc) - timedelta(days=1)
    db.commit()
    db.close()

    resp = client.post("/api/v1/auth/verify", json=verify_data, headers=headers)
    assert resp.status_code == 200 # It returns 200 but valid=False per requirements
    data = resp.json()
    assert data["valid"] == False
    assert data["expire_date"] is not None
    
    # 6. Verify Token Invalid (401)
    resp = client.post("/api/v1/auth/verify", json=verify_data, headers={"Authorization": "Bearer invalid_token"})
    assert resp.status_code == 401

if __name__ == "__main__":
    test_verify_endpoint()
    print("All tests passed!")
