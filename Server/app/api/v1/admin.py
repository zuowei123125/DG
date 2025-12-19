import os
import shutil
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status, Form
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.group import PluginGroup as DBPluginGroup
from app.models.user import User
from app.schemas.group import PluginGroupCreate, PluginGroupUpdate, PluginGroup
from app.schemas.admin import UserInfo
from app.core.config import settings
from typing import List

router = APIRouter()

# Hardcoded admin token for simplicity as per requirements
ADMIN_TOKEN = "admin-secret-token"

def verify_admin(token: str = Form(...)):
    if token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Admin permission required")

def get_admin_dep(x_admin_token: str = None):
    # Alternative using header
    if x_admin_token != ADMIN_TOKEN:
         raise HTTPException(status_code=403, detail="Admin permission required")

# Ensure archives directory exists
ARCHIVES_DIR = "archives"
os.makedirs(ARCHIVES_DIR, exist_ok=True)

@router.post("/upload_version")
async def upload_version(
    file: UploadFile = File(...),
    # token: str = Form(...), # Simple auth
    db: Session = Depends(get_db)
):
    # if token != ADMIN_TOKEN:
    #     raise HTTPException(status_code=403, detail="Invalid admin token")
    
    file_location = os.path.join(ARCHIVES_DIR, file.filename)
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    
    return {"code": 200, "message": f"File '{file.filename}' uploaded successfully", "filename": file.filename}

@router.get("/archives")
async def list_archives():
    if not os.path.exists(ARCHIVES_DIR):
        return []
    files = os.listdir(ARCHIVES_DIR)
    # Sort by name (which usually includes timestamp) desc
    files.sort(reverse=True)
    return files

@router.post("/groups", response_model=PluginGroup)
async def create_group(group: PluginGroupCreate, db: Session = Depends(get_db)):
    db_group = DBPluginGroup(**group.model_dump())
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

@router.get("/groups", response_model=List[PluginGroup])
async def list_groups(db: Session = Depends(get_db)):
    return db.query(DBPluginGroup).all()

@router.put("/groups/{group_id}", response_model=PluginGroup)
async def update_group(group_id: int, group_update: PluginGroupUpdate, db: Session = Depends(get_db)):
    db_group = db.query(DBPluginGroup).filter(DBPluginGroup.id == group_id).first()
    if not db_group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    update_data = group_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_group, key, value)
    
    db.commit()
    db.refresh(db_group)
    return db_group

@router.get("/users", response_model=List[UserInfo])
async def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.put("/users/{user_id}/group")
async def update_user_group(user_id: int, group_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    group = db.query(DBPluginGroup).filter(DBPluginGroup.id == group_id).first()
    if not group:
         raise HTTPException(status_code=404, detail="Group not found")
         
    user.group_id = group_id
    db.commit()
    return {"code": 200, "message": "User group updated"}

@router.put("/users/{user_id}/permissions")
async def update_user_permissions(user_id: int, permissions: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.permissions = permissions
    db.commit()
    return {"code": 200, "message": "User permissions updated"}
