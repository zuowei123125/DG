# 🚀 DesignerCEP 快速部署

## 📐 架构

```
app.aidg168.uk      → 前端（Caddy）
backend.aidg168.uk  → 后端 API（FastAPI + MySQL）
```

---

## 🎯 快速部署（3 步）

### 步骤 1：本地构建

```powershell
# 构建前端
cd Designer
npm run build:core

# 复制到 Server
cd ..
xcopy /E /Y Designer\dist_core\* Server\static\app\

# 打包 Server
Compress-Archive -Path Server\* -DestinationPath Server.zip -Force
```

### 步骤 2：上传到服务器

```powershell
# 上传文件
scp Server.zip root@103.97.201.136:/root/
scp Caddyfile root@103.97.201.136:/etc/caddy/Caddyfile
```

### 步骤 3：服务器部署

```bash
# SSH 登录
ssh root@103.97.201.136

# 解压
cd /root
unzip -o Server.zip -d server

# 启动服务
cd server
docker-compose up -d

# 查看日志
docker-compose logs -f
```

---

## ✅ 验证

访问：`https://app.aidg168.uk/`

---

## 📁 服务器目录结构

```
/root/server/
├── app/                  ← 后端代码
├── static/               ← 前端文件
│   └── app/             ← 前端构建产物
│       ├── index.html
│       └── assets/
├── docker-compose.yml
├── Dockerfile
└── .env
```

---

详细文档：查看 `Server/部署到服务器.md`

