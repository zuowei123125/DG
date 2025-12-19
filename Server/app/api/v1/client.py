from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.client import CheckUpdateRequest, CheckUpdateResponse, LoginResponse
from app.schemas.auth import UserLogin
from app.services.group_service import group_service
from app.services.auth_service import auth_service
from app.db import get_db

router = APIRouter()

@router.post("/check_update", response_model=CheckUpdateResponse)
async def check_update(request: CheckUpdateRequest, db: Session = Depends(get_db)):
    try:
        data = group_service.check_update(db, request.username)
        return CheckUpdateResponse(code=200, data=data, message="success")
    except HTTPException as e:
        # Wrap HTTPException to match response format if needed, or let global handler handle it.
        # Requirements imply specific format.
        # But usually 4xx/5xx are handled by exception handlers.
        # If I want to return 200 with code=404 in body (anti-pattern but possible), I should do it here.
        # The example shows code=200.
        # Let's assume standard HTTP status codes for errors, but if successful, return wrapped data.
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login", response_model=LoginResponse)
async def login(login_data: UserLogin, db: Session = Depends(get_db)):
    # Re-use UserLogin schema as it matches {username, password} + device_id (optional in spec but present in schema)
    # Spec says {username, password}, UserLogin has device_id.
    # If device_id is missing in request, validation fails.
    # Spec example doesn't show device_id in request, but "Backend Development Guidelines" 4.5 says "Must provide stable device_id".
    # So I will assume the client sends device_id.
    
    data = auth_service.client_login(db, login_data)
    return LoginResponse(code=200, data=data, message="success")
