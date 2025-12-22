# 📁 Server 目录说明

## 目录结构

```
Server/
├── app/                    ← 后端代码（FastAPI）
│   ├── api/               ← API 路由
│   ├── core/              ← 核心配置
│   ├── models/            ← 数据库模型
│   ├── schemas/           ← 数据验证
│   ├── services/          ← 业务逻辑
│   ├── main.py            ← 后端入口
│   └── db.py              ← 数据库连接
│
├── static/                 ← ⭐ 前端静态文件（重要！）
│   └── app/               ← 前端构建产物放这里
│       ├── index.html     ← 前端入口
│       ├── assets/        ← JS/CSS/图片
│       └── ...
│
├── archives/              ← Core 版本压缩包（历史版本）
│   ├── core-v1.0.0.zip
│   ├── core-v1.0.1.zip
│   └── ...
│
├── tests/                 ← 测试代码
├── routers/               ← 额外的路由（如果有）
│
├── docker-compose.yml     ← Docker 编排配置
├── Dockerfile             ← 后端镜像构建
├── requirements.txt       ← Python 依赖
├── mysql.cnf              ← MySQL 配置
├── .dockerignore          ← Docker 忽略文件
│
└── designercep.db         ← SQLite 数据库（本地开发用）
```

---

## ⭐ 前端文件应该放在这里

### 构建前端后，复制到这里：

```
Server/static/app/
├── index.html             ← 前端入口（重要！）
├── assets/                ← JS/CSS 等资源
│   ├── index-xxx.js
│   ├── index-xxx.css
│   └── ...
├── CSInterface.js         ← CEP 桥接文件
└── vite.svg              ← 图标等
```

### 操作步骤：

```bash
# 1. 构建前端（在 Designer 目录）
cd Designer
npm run build:core

# 2. 复制到 Server/static/app/
# Windows:
xcopy /E /Y dist_core\* ..\Server\static\app\

# Linux/Mac:
cp -r dist_core/* ../Server/static/app/
```

---

## 🐳 Docker 部署

### 启动服务

```bash
cd Server
docker-compose up -d
```

### 查看日志

```bash
docker-compose logs -f
```

### 停止服务

```bash
docker-compose down
```

---

## 📋 部署清单

- [ ] 前端文件已复制到 `static/app/`
- [ ] `.env` 文件已配置
- [ ] MySQL 密码已修改
- [ ] SECRET_KEY 已修改
- [ ] ALLOWED_ORIGINS 已配置
- [ ] Docker 服务已启动
- [ ] 访问 https://app.aidg168.uk/ 测试

---

**重要**：前端文件必须放在 `Server/static/app/` 目录！

