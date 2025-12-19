from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.group import PluginGroup
from app.schemas.client import CheckUpdateData
from datetime import datetime, timezone

class GroupService:
    def check_update(self, db: Session, username: str) -> CheckUpdateData:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")

        # Check expiration
        is_expired = False
        if user.expire_date:
            now = datetime.now(timezone.utc)
            expire_date = user.expire_date
            if expire_date.tzinfo is None:
                 expire_date = expire_date.replace(tzinfo=timezone.utc)
            if now > expire_date:
                is_expired = True

        # Get group and version
        if not user.group_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户未分配组")
        
        group = db.query(PluginGroup).filter(PluginGroup.id == user.group_id).first()
        if not group:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户所属组不存在")

        if not group.current_version_file:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="当前组无可用版本")

        # Construct download URL (assuming base URL or relative path)
        # In a real scenario, this might be from config
        download_url = f"/download/{group.current_version_file}"
        
        # Extract version from filename roughly or use file metadata if available
        # Assuming filename format: plugin_v1.0.2.zip
        version = "unknown"
        filename = group.current_version_file
        if "v" in filename:
            try:
                # Simple extraction logic, can be improved
                parts = filename.split("v")
                if len(parts) > 1:
                    version_part = parts[1]
                    version = "v" + version_part.split(".zip")[0].split("_")[0]
            except:
                pass

        return CheckUpdateData(
            version=version,
            download_url=download_url,
            force_update=False,
            is_expired=is_expired
        )

group_service = GroupService()
