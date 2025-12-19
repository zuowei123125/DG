import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db import Base, get_db
from app.models.group import PluginGroup
from app.services.email_service import email_service
from unittest.mock import MagicMock

# Mock Email Service to avoid sending real emails
email_service.send_email = MagicMock()

# In-memory SQLite database for testing
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

def test_register_with_email():
    # 1. Register
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser_email",
            "password": "password123",
            "confirm_password": "password123",
            "email": "test@example.com",
            "device_id": "test_device"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["username"] == "testuser_email"
    
    # Check if verification email was "sent"
    assert email_service.send_email.called

def test_verify_email():
    # 1. Register first
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "verify_user",
            "password": "password123",
            "confirm_password": "password123",
            "email": "verify@example.com",
            "device_id": "test_device"
        },
    )
    
    # 2. Get code from DB (since we mocked email)
    db = TestingSessionLocal()
    from app.models.user import User
    user = db.query(User).filter(User.username == "verify_user").first()
    code = user.verification_code
    assert code is not None
    assert user.is_verified is False
    db.close()
    
    # 3. Verify
    response = client.post(
        "/api/v1/auth/verify-email",
        json={
            "username": "verify_user",
            "code": code
        }
    )
    assert response.status_code == 200
    assert response.json()["detail"] == "验证成功"
    
    # 4. Check DB status
    db = TestingSessionLocal()
    user = db.query(User).filter(User.username == "verify_user").first()
    assert user.is_verified is True
    db.close()

def test_forgot_password_flow():
    # 1. Register
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "reset_user",
            "password": "old_password",
            "confirm_password": "old_password",
            "email": "reset@example.com",
            "device_id": "test_device"
        },
    )
    
    # 2. Request password reset
    response = client.post(
        "/api/v1/auth/forgot-password",
        json={"email": "reset@example.com"}
    )
    assert response.status_code == 200
    
    # 3. Get token from DB
    db = TestingSessionLocal()
    from app.models.user import User
    user = db.query(User).filter(User.username == "reset_user").first()
    token = user.reset_token
    assert token is not None
    db.close()
    
    # 4. Reset password
    response = client.post(
        "/api/v1/auth/reset-password",
        json={
            "token": token,
            "new_password": "new_password",
            "confirm_password": "new_password"
        }
    )
    assert response.status_code == 200
    assert response.json()["detail"] == "密码重置成功"
    
    # 5. Verify login with new password
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "reset_user",
            "password": "new_password",
            "device_id": "test_device"
        }
    )
    assert response.status_code == 200
