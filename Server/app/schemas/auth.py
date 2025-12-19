from pydantic import BaseModel

class UserLogin(BaseModel):
    # 登录请求模型
    username: str
    password: str
    device_id: str  # 设备标识，用于限制单设备登录

class UserRegister(BaseModel):
    # 注册请求模型
    username: str
    password: str
    confirm_password: str
    email: str | None = None # Optional for backward compatibility, but required for verification
    code: str | None = None # 新增：验证码
    device_id: str = "unknown_device"  # 兼容旧前端，设为默认值，建议前端传入

class SendVerificationCodeRequest(BaseModel):
    email: str

class VerifyEmailRequest(BaseModel):
    username: str
    code: str

class ForgotPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    email: str # 新增：必须传 email 配合验证码
    token: str # 这里是 6 位数字验证码
    new_password: str
    confirm_password: str

class Token(BaseModel):
    # 登录/注册成功返回的令牌模型
    access_token: str
    token_type: str
    username: str

class UserLogout(BaseModel):
    # 登出请求模型
    username: str
    device_id: str

class UserHeartbeat(BaseModel):
    # 心跳请求模型（更新最近在线时间）
    username: str
    device_id: str

class VerifyRequest(BaseModel):
    """验证请求模型"""
    username: str
    device_id: str
    timestamp: int

class VerifyResponse(BaseModel):
    """验证响应模型"""
    valid: bool
    username: str | None = None
    expire_date: str | None = None
