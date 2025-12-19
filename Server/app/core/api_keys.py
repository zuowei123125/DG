"""
API Key 管理
用于验证客户端请求
"""

from datetime import datetime
from typing import Optional, Dict

class APIKeyManager:
    """API Key 管理器"""
    
    # 🔐 有效的 API Keys
    # 生产环境建议从环境变量或数据库读取
    VALID_KEYS: Dict[str, dict] = {
        "demo_key_123": {
            "name": "测试密钥",
            "created": "2024-12-16",
            "permissions": ["calculate"],
            "rate_limit": 100  # 每小时最多 100 次请求
        },
        "prod_key_xyz789abc": {
            "name": "生产密钥",
            "created": "2024-12-16",
            "permissions": ["calculate", "admin"],
            "rate_limit": 1000
        }
    }
    
    @classmethod
    def validate_key(cls, api_key: Optional[str]) -> bool:
        """验证 API Key 是否有效"""
        if not api_key:
            return False
        return api_key in cls.VALID_KEYS
    
    @classmethod
    def get_key_info(cls, api_key: str) -> Optional[dict]:
        """获取 API Key 信息"""
        return cls.VALID_KEYS.get(api_key)
    
    @classmethod
    def check_permission(cls, api_key: str, permission: str) -> bool:
        """检查 API Key 是否有指定权限"""
        key_info = cls.get_key_info(api_key)
        if not key_info:
            return False
        return permission in key_info.get("permissions", [])
    
    @classmethod
    def add_key(cls, api_key: str, name: str, permissions: list = None):
        """添加新的 API Key"""
        cls.VALID_KEYS[api_key] = {
            "name": name,
            "created": datetime.now().strftime("%Y-%m-%d"),
            "permissions": permissions or ["calculate"],
            "rate_limit": 100
        }
    
    @classmethod
    def remove_key(cls, api_key: str):
        """删除 API Key"""
        if api_key in cls.VALID_KEYS:
            del cls.VALID_KEYS[api_key]
    
    @classmethod
    def list_keys(cls) -> Dict[str, dict]:
        """列出所有 API Keys"""
        return cls.VALID_KEYS.copy()


# 快捷函数
def validate_api_key(api_key: Optional[str]) -> bool:
    """验证 API Key"""
    return APIKeyManager.validate_key(api_key)


def get_key_info(api_key: str) -> Optional[dict]:
    """获取 API Key 信息"""
    return APIKeyManager.get_key_info(api_key)

