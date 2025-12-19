from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserInfo(BaseModel):
    id: int
    username: str
    group_id: Optional[int] = None
    permissions: Optional[str] = None
    expire_date: Optional[datetime] = None

    class Config:
        from_attributes = True
