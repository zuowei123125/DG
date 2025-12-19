# DesignerCEP 后端 API 接口文档

本文档描述了 DesignerCEP 后端服务的 API 接口规范，包括客户端插件接口和后台管理接口。

## 1. 基础信息

- **Base URL**: `http://localhost:8000/api/v1`
- **文件下载 Base URL**: `http://localhost:8000/download/`
- **鉴权方式**:
  - **Client**: Bearer Token (JWT)
  - **Admin**: 简单 Token (Header `x-admin-token` 或 Form `token`) - *开发阶段*

## 2. 客户端接口 (Client)

用于 Photoshop 插件端的交互。

### 2.1 登录 (Login)

客户端登录，获取 Token、权限及过期时间。

- **URL**: `/client/login`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "username": "user1",
    "password": "password123",
    "device_id": "unique-device-id"
  }
  ```
- **Response**:
  ```json
  {
    "code": 200,
    "data": {
      "token": "eyJhbGciOiJIUzI1...",
      "username": "user1",
      "expire_date": "2025-12-31",
      "permissions": ["batch_process", "export"]
    },
    "message": "success"
  }
  ```

### 2.2 检查更新 (Check Update)

根据用户所在组检查是否有新版本。

- **URL**: `/client/check_update`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "username": "user1"
  }
  ```
- **Response**:
  ```json
  {
    "code": 200,
    "data": {
      "version": "v1.0",
      "download_url": "/download/plugin_v1.0.zip",
      "force_update": false,
      "is_expired": false
    },
    "message": "success"
  }
  ```
  - `is_expired`: 若为 `true`，表示用户授权已过期，客户端应限制功能。
  - `download_url`: 拼接 Base URL 使用。

---

## 3. 管理端接口 (Admin)

用于发布系统管理（CI/CD 或管理后台）。需在 Header 中携带 `x-admin-token: admin-secret-token` (默认开发Token)。

### 3.1 上传版本文件 (Upload Version)

上传插件 ZIP 包到服务器。

- **URL**: `/admin/upload_version`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Form Data**:
  - `file`: (Binary Zip File)
  - `token`: "admin-secret-token" (作为 Form 字段兼容脚本)
- **Response**:
  ```json
  {
    "code": 200,
    "message": "File 'plugin_v1.0.zip' uploaded successfully",
    "filename": "plugin_v1.0.zip"
  }
  ```

### 3.2 创建用户组 (Create Group)

- **URL**: `/admin/groups`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "name": "Dev Group",
    "current_version_file": "plugin_v1.0_beta.zip",
    "comment": "开发测试组"
  }
  ```
- **Response**: 返回创建的组对象。

### 3.3 更新用户组 (Update Group)

用于切换组的版本。

- **URL**: `/admin/groups/{group_id}`
- **Method**: `PUT`
- **Request Body**:
  ```json
  {
    "current_version_file": "plugin_v1.1_stable.zip"
  }
  ```

### 3.4 获取所有组 (List Groups)

- **URL**: `/admin/groups`
- **Method**: `GET`
- **Response**: 组列表数组。

### 3.5 修改用户所属组 (Update User Group)

- **URL**: `/admin/users/{user_id}/group`
- **Method**: `PUT`
- **Query Params**:
  - `group_id`: 目标组 ID
- **Response**:
  ```json
  {
    "code": 200,
    "message": "User group updated"
  }
  ```

---

## 4. 数据库模型说明

### PluginGroup (用户组)
- `id`: ID
- `name`: 组名 (Unique)
- `current_version_file`: 当前关联的 ZIP 文件名
- `comment`: 备注

### User (用户)
- `id`: ID
- `username`: 用户名
- `group_id`: 所属组 ID (Foreign Key)
- `permissions`: 权限列表 (逗号分隔字符串)
- `expire_date`: 过期时间
