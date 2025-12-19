from typing import Optional
from pydantic import BaseModel

class PluginGroupBase(BaseModel):
    name: str
    current_version_file: Optional[str] = None
    comment: Optional[str] = None

class PluginGroupCreate(PluginGroupBase):
    pass

class PluginGroupUpdate(PluginGroupBase):
    name: Optional[str] = None

class PluginGroup(PluginGroupBase):
    id: int

    class Config:
        from_attributes = True
