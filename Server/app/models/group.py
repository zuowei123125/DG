from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db import Base

class PluginGroup(Base):
    __tablename__ = "plugin_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), unique=True, index=True, nullable=False)
    current_version_file = Column(String(255), nullable=True)  # Name of the zip file
    comment = Column(Text, nullable=True)

    users = relationship("User", back_populates="group")
