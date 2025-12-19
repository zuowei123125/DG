# API Key 使用指南

## ✅ 已启用 API Key 验证

现在所有对 `/api/v1/jsx_demo/calculate` 的请求都需要提供有效的 API Key。

---

## 🔑 当前可用的 API Keys

### 1. 测试密钥（开发使用）
```
API Key: demo_key_123
名称: 测试密钥
权限: calculate
限制: 100次/小时
```

### 2. 生产密钥（生产环境）
```
API Key: prod_key_xyz789abc
名称: 生产密钥
权限: calculate, admin
限制: 1000次/小时
```

---

## 📝 日志示例

启用 API Key 后，后端日志会显示：

```
============================================================
📥 收到计算请求
   时间: 2024-12-16 15:30:45
   表达式: 87-98
   API Key: demo_key_123
============================================================
✅ API Key 验证通过 | 名称: 测试密钥 | 权限: ['calculate']
🛡️ 安全检查: 验证表达式格式...
✅ 表达式格式验证通过
🔒 开始执行核心算法...
✅ 计算完成: 87-98 = -11
============================================================
```

### 如果 API Key 无效：

```
============================================================
📥 收到计算请求
   时间: 2024-12-16 15:30:45
   表达式: 87-98
   API Key: invalid_key_xxx
============================================================
❌ API Key 验证失败: invalid_key_xxx
```

**前端会收到：** `403 Forbidden: 无效的 API Key`

---

## 🔧 管理 API Keys

### 查看所有 Keys

打开 `Server/app/core/api_keys.py`：

```python
VALID_KEYS: Dict[str, dict] = {
    "demo_key_123": {
        "name": "测试密钥",
        "created": "2024-12-16",
        "permissions": ["calculate"],
        "rate_limit": 100
    },
    # ... 更多 keys
}
```

### 添加新的 API Key

**方法 1：直接编辑配置文件**

在 `api_keys.py` 中添加：

```python
"your_new_key_456": {
    "name": "客户A的密钥",
    "created": "2024-12-16",
    "permissions": ["calculate"],
    "rate_limit": 200
}
```

**方法 2：使用 Python 代码**

```python
from app.core.api_keys import APIKeyManager

# 添加新 Key
APIKeyManager.add_key(
    api_key="customer_key_789",
    name="客户B的密钥",
    permissions=["calculate", "export"]
)
```

### 删除 API Key

```python
from app.core.api_keys import APIKeyManager

# 删除 Key
APIKeyManager.remove_key("old_key_123")
```

### 检查权限

```python
from app.core.api_keys import APIKeyManager

# 检查是否有权限
has_permission = APIKeyManager.check_permission("demo_key_123", "calculate")
```

---

## 🔒 前端配置

### 当前配置（已设置）

`Designer/src/api/jsxApi/inline/hybrid-demo.ts`：

```typescript
const response = await fetch(`${config.apiBaseUrl}/jsx_demo/calculate`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-API-Key': 'demo_key_123'  // 🔐 使用测试密钥
    },
    body: JSON.stringify({
        expression: layerName
    })
});
```

### 切换到生产密钥

修改 API Key：

```typescript
'X-API-Key': 'prod_key_xyz789abc'  // 使用生产密钥
```

### 从配置文件读取（推荐）

创建 `Designer/src/config/apiKeys.ts`：

```typescript
export const API_KEYS = {
    development: 'demo_key_123',
    production: 'prod_key_xyz789abc'
};

// 根据环境自动选择
export const getCurrentApiKey = () => {
    return import.meta.env.DEV 
        ? API_KEYS.development 
        : API_KEYS.production;
};
```

然后在 `hybrid-demo.ts` 中使用：

```typescript
import { getCurrentApiKey } from '@/config/apiKeys';

const response = await fetch(`${config.apiBaseUrl}/jsx_demo/calculate`, {
    headers: {
        'X-API-Key': getCurrentApiKey()  // 自动选择正确的 Key
    }
});
```

---

## 🧪 测试 API Key 验证

### 测试 1：使用有效的 Key

1. 创建图层名称：`87-98`
2. 点击"智能配色"
3. **预期结果：** ✅ 成功计算

**后端日志：**
```
✅ API Key 验证通过 | 名称: 测试密钥
```

---

### 测试 2：使用无效的 Key

临时修改前端，使用错误的 Key：

```typescript
'X-API-Key': 'wrong_key_xxx'
```

**预期结果：** ❌ 403 错误

**后端日志：**
```
❌ API Key 验证失败: wrong_key_xxx
```

**前端错误：**
```
Message.error('无效的 API Key')
```

---

### 测试 3：不提供 Key

注释掉 API Key：

```typescript
// 'X-API-Key': 'demo_key_123'
```

**预期结果：** ❌ 403 错误

**后端日志：**
```
❌ API Key 验证失败: None
```

---

## 🛡️ 安全最佳实践

### ✅ 应该做的

1. **不同环境使用不同的 Key**
   - 开发环境：`demo_key_123`
   - 生产环境：`prod_key_xyz789abc`

2. **定期更换 Key**
   ```python
   # 每季度更新一次
   "new_key_2024_q1": {...}
   ```

3. **使用环境变量**
   ```python
   import os
   API_KEY = os.getenv('DESIGNER_API_KEY', 'demo_key_123')
   ```

4. **记录所有请求**
   - 已实现：所有请求都会记录 API Key

5. **限制调用频率**
   - 已配置：每个 Key 都有 rate_limit

### ❌ 不应该做的

1. ❌ 把 Key 硬编码在公开的代码中
2. ❌ 在 Git 中提交包含生产 Key 的文件
3. ❌ 多个客户共用同一个 Key
4. ❌ 永远不更换 Key

---

## 🚀 进一步加强

### 1. 数据库存储 API Keys

```python
# models/api_key.py
class APIKey(Base):
    __tablename__ = "api_keys"
    
    key = Column(String, primary_key=True)
    name = Column(String)
    permissions = Column(JSON)
    rate_limit = Column(Integer)
    created_at = Column(DateTime)
    expires_at = Column(DateTime)
    is_active = Column(Boolean, default=True)
```

### 2. Key 过期时间

```python
"demo_key_123": {
    "expires": "2025-12-31",  # Key 会过期
}
```

### 3. 使用量统计

```python
"demo_key_123": {
    "usage_count": 0,
    "last_used": None,
}
```

### 4. IP 绑定

```python
"demo_key_123": {
    "allowed_ips": ["192.168.1.100", "127.0.0.1"]
}
```

---

## 📊 总结

| 功能 | 状态 | 说明 |
|------|------|------|
| API Key 验证 | ✅ 已启用 | 所有请求必须提供有效 Key |
| 多 Key 支持 | ✅ 已实现 | 可配置多个不同权限的 Key |
| 权限控制 | ✅ 已实现 | 每个 Key 可配置不同权限 |
| 日志记录 | ✅ 已实现 | 记录所有 Key 使用情况 |
| Key 管理器 | ✅ 已实现 | 提供增删改查 API |
| 限流配置 | 🔧 已配置 | 待实现实际限流逻辑 |
| 数据库存储 | ⚠️ 未实现 | 当前使用配置文件 |
| Key 过期 | ⚠️ 未实现 | 可以扩展 |

---

**当前 API Key 已启用！所有请求都会被验证和记录！**

