# DesignerCEP 认证模块接口文档

本文档描述了后端新增的邮箱注册验证与密码重置相关接口。

## 1. 注册 (Register)

支持传入邮箱进行注册。如果传入邮箱，系统将发送验证码邮件。

- **URL**: `/api/v1/auth/register`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "username": "user1",
    "password": "password123",
    "confirm_password": "password123",
    "email": "user1@gmail.com", // [新增] 可选，推荐填写
    "device_id": "device_unique_id"
  }
  ```
- **Response**:
  - Success (200):
    ```json
    {
      "access_token": "eyJhbGciOiJIUzI1NiIsIn...",
      "token_type": "bearer",
      "username": "user1"
    }
    ```
  - Error (400): 用户名已存在 / 邮箱已存在 / 密码不一致

## 2. 验证邮箱 (Verify Email)

用户收到验证码邮件后，在前端输入验证码进行验证。

- **URL**: `/api/v1/auth/verify-email`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "username": "user1",
    "code": "123456" // 邮件中的6位数字验证码
  }
  ```
- **Response**:
  - Success (200):
    ```json
    {
      "detail": "验证成功"
    }
    ```
  - Error (400): 验证码错误

## 3. 忘记密码 (Forgot Password)

用户输入注册邮箱，请求重置密码。

- **URL**: `/api/v1/auth/forgot-password`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "email": "user1@gmail.com"
  }
  ```
- **Response**:
  - Success (200):
    ```json
    {
      "detail": "如果邮箱存在，重置邮件已发送"
    }
    ```

## 4. 重置密码 (Reset Password)

用户点击邮件中的链接（或手动输入Token），设置新密码。

- **URL**: `/api/v1/auth/reset-password`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "token": "reset_token_from_email",
    "new_password": "new_password123",
    "confirm_password": "new_password123"
  }
  ```
- **Response**:
  - Success (200):
    ```json
    {
      "detail": "密码重置成功"
    }
    ```
  - Error (400): Token 无效 / Token 已过期 / 密码不一致

## 流程说明

1. **注册流程**:
   - 用户填写注册信息（含邮箱）。
   - 提交 `/register`。
   - 如果成功，后端自动登录并返回 Token。
   - 如果填写了邮箱，后端会发送一封验证邮件。
   - 前端提示用户查收邮件并输入验证码。
   - 用户输入验证码，前端调用 `/verify-email`。

2. **找回密码流程**:
   - 用户点击“忘记密码”。
   - 输入邮箱，前端调用 `/forgot-password`。
   - 用户收到邮件，包含重置 Token。
   - 前端提供重置密码界面，用户输入新密码。
   - 前端调用 `/reset-password`（带上 Token 和新密码）。
   - 重置成功后，跳转至登录页。
