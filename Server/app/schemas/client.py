from typing import List, Optional
from pydantic import BaseModel
from datetime import date, datetime

class CheckUpdateData(BaseModel):
    version: str
    download_url: str
    force_update: bool
    is_expired: bool

class CheckUpdateResponse(BaseModel):
    code: int
    data: CheckUpdateData
    message: str

class LoginData(BaseModel):
    token: str
    username: str
    expire_date: Optional[str] # YYYY-MM-DD
    permissions: List[str]

class LoginResponse(BaseModel):
    code: int
    data: LoginData
    message: str

class CheckUpdateRequest(BaseModel):
    username: str
