import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from unittest.mock import MagicMock
import sys
import os

# Add Server directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from app.db import Base, get_db
from app.models.group import PluginGroup
from app.models.user import User
from app.services.email_service import email_service

# Mock Email Service
email_service.send_email = MagicMock()

# In-memory SQLite database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    # Create default group
    db = TestingSessionLocal()
    if not db.query(PluginGroup).filter(PluginGroup.name == "default").first():
        default_group = PluginGroup(name="default", comment="Default Group")
        db.add(default_group)
        db.commit()
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)
    # Reset mock
    email_service.send_email.reset_mock()

def test_single_form_registration_flow():
    email = "newuser@example.com"
    password = "securepassword123"
    username = "realusername"

    # 1. Send verification code
    response = client.post(
        "/api/v1/auth/send-verification-code",
        json={"email": email}
    )
    assert response.status_code == 200
    assert response.json()["detail"] == "验证码已发送"
    assert email_service.send_email.called

    # 2. Retrieve code from DB
    db = TestingSessionLocal()
    temp_user = db.query(User).filter(User.email == email).first()
    assert temp_user is not None
    assert temp_user.verification_code is not None
    assert len(temp_user.verification_code) == 6
    code = temp_user.verification_code
    db.close()

    # 3. Try register with WRONG code
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": username,
            "password": password,
            "confirm_password": password,
            "email": email,
            "code": "000000",
            "device_id": "test_device"
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "验证码错误"

    # 4. Register with CORRECT code
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": username,
            "password": password,
            "confirm_password": password,
            "email": email,
            "code": code,
            "device_id": "test_device"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == username
    assert "access_token" in data

    # 5. Verify user status in DB
    db = TestingSessionLocal()
    user = db.query(User).filter(User.username == username).first()
    assert user is not None
    assert user.email == email
    assert user.is_verified is True
    # Ensure temp username is gone or updated (logic: update existing temp user)
    # The logic in auth_service.register finds the user by email (which was the temp user) 
    # and updates username and password.
    assert user.hashed_password != "temp_password_placeholder"
    db.close()

def test_reset_password_flow():
    # Setup: Create a verified user
    db = TestingSessionLocal()
    from app.core.security import get_password_hash
    user = User(
        username="resetuser",
        email="reset@example.com",
        hashed_password=get_password_hash("oldpassword"),
        is_verified=True
    )
    db.add(user)
    db.commit()
    db.close()

    email = "reset@example.com"
    new_password = "newpassword123"

    # 1. Request password reset (Forgot Password)
    response = client.post(
        "/api/v1/auth/forgot-password",
        json={"email": email}
    )
    assert response.status_code == 200
    assert email_service.send_email.called

    # 2. Retrieve reset token (6-digit code) from DB
    db = TestingSessionLocal()
    user = db.query(User).filter(User.email == email).first()
    assert user.reset_token is not None
    assert len(user.reset_token) == 6
    token = user.reset_token
    db.close()

    # 3. Reset password with code
    response = client.post(
        "/api/v1/auth/reset-password",
        json={
            "email": email,
            "token": token,
            "new_password": new_password,
            "confirm_password": new_password
        }
    )
    assert response.status_code == 200
    assert response.json()["detail"] == "密码重置成功"

    # 4. Login with new password
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "resetuser",
            "password": new_password,
            "device_id": "test_device"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

    # 5. Login with old password should fail
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "resetuser",
            "password": "oldpassword",
            "device_id": "test_device"
        }
    )
    assert response.status_code == 401
