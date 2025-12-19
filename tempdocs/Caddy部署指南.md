# 🚀 DesignerCEP Caddy 部署指南

## 为什么选择 Caddy？

✅ **自动 HTTPS**：无需手动申请证书，自动从 Let's Encrypt 获取并续期  
✅ **配置简单**：比 Nginx 简单 10 倍，一看就懂  
✅ **开箱即用**：自动处理 HTTP/2, GZIP 压缩  
✅ **完美支持 Cloudflare**：自动识别并配置  

---

## 📦 1. 安装 Caddy

### Ubuntu/Debian

```bash
# 安装依赖
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https

# 添加 Caddy 官方仓库
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list

# 更新并安装
sudo apt update
sudo apt install caddy

# 验证安装
caddy version
```

### CentOS/RHEL

```bash
# 添加 Caddy 官方仓库
dnf install 'dnf-command(copr)'
dnf copr enable @caddy/caddy
dnf install caddy

# 启动服务
sudo systemctl enable caddy
sudo systemctl start caddy
```

---

## 📁 2. 准备项目目录

```bash
# 创建项目目录
sudo mkdir -p /var/www/DesignerCEP/Server/static/{shell,core,downloads}

# 设置权限
sudo chown -R $USER:$USER /var/www/DesignerCEP
chmod -R 755 /var/www/DesignerCEP
```

---

## ⚙️ 3. 配置 Caddy

### 方案 A: 标准部署（Let's Encrypt 自动证书）

**适用于**：独立域名，不使用 Cloudflare 代理

```bash
# 创建 Caddyfile
sudo nano /etc/caddy/Caddyfile
```

```caddy
# /etc/caddy/Caddyfile

# ========== 主站配置 ==========
your-domain.com, www.your-domain.com {
    # ✅ Caddy 会自动处理 HTTPS 证书

    # ========== API 请求 → FastAPI ==========
    handle /api/* {
        reverse_proxy localhost:8000 {
            # 传递真实 IP
            header_up X-Real-IP {remote_host}
            header_up X-Forwarded-For {remote_host}
            header_up X-Forwarded-Proto {scheme}
        }
    }

    # ========== Shell 在线登录页 ==========
    handle /shell/* {
        root * /var/www/DesignerCEP/Server/static/shell
        try_files {path} {path}/ /shell/index.html
        file_server

        # HTML 不缓存
        @html {
            path *.html
        }
        header @html Cache-Control "no-cache, no-store, must-revalidate"

        # JS/CSS 长期缓存
        @assets {
            path *.js *.css
        }
        header @assets Cache-Control "public, max-age=31536000, immutable"
    }

    # ========== Core 核心应用 ==========
    handle /core/* {
        root * /var/www/DesignerCEP/Server/static/core
        file_server

        # HTML 不缓存
        @html {
            path *.html
        }
        header @html Cache-Control "no-cache, no-store, must-revalidate"

        # JS/CSS 长期缓存
        @assets {
            path *.js *.css
        }
        header @assets Cache-Control "public, max-age=31536000, immutable"
    }

    # ========== 下载文件 ==========
    handle /downloads/* {
        root * /var/www/DesignerCEP/Server/static/downloads
        file_server

        # 启用断点续传
        header Accept-Ranges bytes
        
        # 缓存 1 天
        header Cache-Control "public, max-age=86400"
    }

    # ========== 根路径重定向 ==========
    handle / {
        redir /shell/ permanent
    }

    # ========== 通用配置 ==========
    # 自动 GZIP 压缩
    encode gzip zstd

    # 安全头
    header {
        X-Frame-Options "SAMEORIGIN"
        X-Content-Type-Options "nosniff"
        X-XSS-Protection "1; mode=block"
        -Server  # 隐藏服务器信息
    }

    # 日志
    log {
        output file /var/log/caddy/designer-cep.log {
            roll_size 100mb
            roll_keep 10
        }
    }
}
```

### 方案 B: Cloudflare 代理部署（推荐）

**适用于**：域名使用 Cloudflare 橙云代理

```bash
sudo nano /etc/caddy/Caddyfile
```

```caddy
# /etc/caddy/Caddyfile (Cloudflare 版本)

{
    # ✅ 关闭自动 HTTPS（Cloudflare 已经提供）
    auto_https off
    
    # 或者使用内部证书
    # auto_https disable_redirects
}

# ========== HTTP 配置（Cloudflare 会加 HTTPS）==========
http://your-domain.com, http://www.your-domain.com {
    
    # ========== API 请求 → FastAPI ==========
    handle /api/* {
        reverse_proxy localhost:8000 {
            # ✅ 从 Cloudflare 获取真实 IP
            header_up X-Real-IP {header.CF-Connecting-IP}
            header_up X-Forwarded-For {header.CF-Connecting-IP}
            header_up X-Forwarded-Proto https
        }
    }

    # ========== Shell 在线登录页 ==========
    handle /shell/* {
        root * /var/www/DesignerCEP/Server/static/shell
        try_files {path} {path}/ /shell/index.html
        file_server

        @html path *.html
        header @html Cache-Control "no-cache, no-store, must-revalidate"

        @assets path *.js *.css
        header @assets Cache-Control "public, max-age=31536000, immutable"
    }

    # ========== Core 核心应用 ==========
    handle /core/* {
        root * /var/www/DesignerCEP/Server/static/core
        file_server

        @html path *.html
        header @html Cache-Control "no-cache, no-store, must-revalidate"

        @assets path *.js *.css
        header @assets Cache-Control "public, max-age=31536000, immutable"
    }

    # ========== 下载文件 ==========
    handle /downloads/* {
        root * /var/www/DesignerCEP/Server/static/downloads
        file_server
        header Accept-Ranges bytes
        header Cache-Control "public, max-age=86400"
    }

    # ========== 根路径重定向 ==========
    handle / {
        redir /shell/ permanent
    }

    # ========== 通用配置 ==========
    encode gzip zstd

    header {
        X-Frame-Options "SAMEORIGIN"
        X-Content-Type-Options "nosniff"
        X-XSS-Protection "1; mode=block"
        -Server
    }

    log {
        output file /var/log/caddy/designer-cep.log {
            roll_size 100mb
            roll_keep 10
        }
    }
}
```

---

## 🔧 4. 修改后端代码（支持 CEP 环境）

### 4.1 修改 FastAPI 的 CORS 配置

```python
# Server/app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title=settings.PROJECT_NAME)

# 环境判断
IS_DEV = os.getenv("ENV", "development") == "development"

# ========== CORS 配置 ==========
if IS_DEV:
    # 开发环境：宽松配置
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    # 生产环境：严格配置
    allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )
    
    # ✅ 特殊处理 CEP 环境（Origin: null）
    @app.middleware("http")
    async def cep_cors_middleware(request: Request, call_next):
        origin = request.headers.get("origin")
        
        # CEP 环境的 Origin 是 null 或 cep://
        if origin in ["null", None] or (origin and origin.startswith("cep://")):
            response = await call_next(request)
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "*"
            return response
        
        return await call_next(request)

# ========== API 路由（保持不变）==========
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["authentication"])
app.include_router(client.router, prefix=f"{settings.API_V1_STR}/client", tags=["client"])
app.include_router(admin.router, prefix=f"{settings.API_V1_STR}/admin", tags=["admin"])
app.include_router(analytics.router, prefix=f"{settings.API_V1_STR}/analytics", tags=["analytics"])
app.include_router(jsx_demo.router, prefix=f"{settings.API_V1_STR}/jsx_demo", tags=["jsx_demo"])

# ❌ 删除静态文件挂载（交给 Caddy 处理）
# app.mount("/download", ...)  # 删除
# app.mount("/shell", ...)     # 删除
# app.mount("/core", ...)      # 删除

@app.get("/")
def read_root():
    return {"message": "DesignerCEP API Server", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.on_event("startup")
def on_startup():
    init_db()
```

### 4.2 配置环境变量

```bash
# Server/.env
ENV=production
PROJECT_NAME=DesignerCEP
API_V1_STR=/api/v1
SECRET_KEY=your-secret-key-here
DATABASE_URL=mysql://user:password@localhost:3306/designer_cep

# 生产环境允许的来源
ALLOWED_ORIGINS=https://your-domain.com,https://www.your-domain.com

# 是否由 FastAPI 提供静态文件（生产环境设为 false）
SERVE_STATIC=false
```

---

## 🚀 5. 部署 FastAPI 服务

### 5.1 使用 Systemd 管理服务

```bash
# 创建服务文件
sudo nano /etc/systemd/system/designer-cep.service
```

```ini
[Unit]
Description=DesignerCEP FastAPI Application
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/DesignerCEP/Server
Environment="PATH=/var/www/DesignerCEP/Server/venv/bin"
ExecStart=/var/www/DesignerCEP/Server/venv/bin/gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 127.0.0.1:8000

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 5.2 安装依赖并启动

```bash
# 1. 创建虚拟环境
cd /var/www/DesignerCEP/Server
python3 -m venv venv
source venv/bin/activate

# 2. 安装依赖
pip install -r requirements.txt
pip install gunicorn uvicorn[standard]

# 3. 测试运行
uvicorn app.main:app --host 127.0.0.1 --port 8000

# 4. 启动服务
sudo systemctl daemon-reload
sudo systemctl enable designer-cep
sudo systemctl start designer-cep

# 5. 检查状态
sudo systemctl status designer-cep
```

---

## 📤 6. 部署前端文件

### 6.1 配置前端环境

```bash
# Designer/.env.production
VITE_API_SERVER=https://your-domain.com
```

### 6.2 构建前端

```bash
cd Designer
npm install
npm run build
```

### 6.3 上传到服务器

#### 方法 A: 手动上传

```bash
# 在本地执行
cd Designer/dist

# 上传 Shell
scp -r Shell/* user@your-server:/var/www/DesignerCEP/Server/static/shell/

# 上传 Core
scp -r Designer/* user@your-server:/var/www/DesignerCEP/Server/static/core/1.0.6/

# 打包并上传 Shell.zip
zip -r shell-1.0.6.zip Shell/
scp shell-1.0.6.zip user@your-server:/var/www/DesignerCEP/Server/static/downloads/
```

#### 方法 B: 使用自动化脚本

```bash
# 在项目根目录执行
cd AdminTool

# 首次配置
python auto_deploy_core.py --version 1.0.6 --setup

# 输入配置信息:
# - 服务器地址: your-domain.com
# - SSH 端口: 22
# - 用户名: root
# - 密码: ******
# - 远程路径: /var/www/DesignerCEP/Server/static

# 部署
python auto_deploy_core.py --version 1.0.6 --deploy --update-db
```

---

## ✅ 7. 启动 Caddy

```bash
# 检查配置语法
sudo caddy validate --config /etc/caddy/Caddyfile

# 重启 Caddy
sudo systemctl restart caddy

# 查看状态
sudo systemctl status caddy

# 查看日志
sudo journalctl -u caddy -f
```

---

## 🧪 8. 测试部署

### 8.1 测试静态文件

```bash
# 测试 Shell
curl -I https://your-domain.com/shell/

# 期望输出：
# HTTP/2 200
# content-type: text/html

# 测试 Core
curl -I https://your-domain.com/core/1.0.6/

# 测试下载
curl -I https://your-domain.com/downloads/shell-1.0.6.zip
```

### 8.2 测试 API

```bash
# 测试健康检查
curl https://your-domain.com/api/v1/health

# 期望输出：
# {"status":"healthy"}

# 测试登录接口
curl -X POST https://your-domain.com/api/v1/client/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test","device_id":"test-device"}'
```

### 8.3 测试 CEP CORS

```bash
# 模拟 CEP 环境的预检请求
curl -X OPTIONS https://your-domain.com/api/v1/client/login \
  -H "Origin: null" \
  -H "Access-Control-Request-Method: POST" \
  -v

# 期望输出：
# Access-Control-Allow-Origin: *
# Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
```

### 8.4 浏览器测试

1. 打开 `https://your-domain.com/shell/`
2. 输入用户名密码登录
3. 按 F12 打开开发者工具
4. 查看 Network 标签：
   - ✅ 所有请求都是 HTTPS
   - ✅ API 请求有 `Authorization: Bearer xxx`
   - ✅ 没有 CORS 错误

---

## 🔍 9. 常见问题

### Q1: Caddy 自动证书失败

**原因**：域名 DNS 没有解析到服务器

**解决**：
```bash
# 检查 DNS 解析
nslookup your-domain.com

# 确保 A 记录指向服务器 IP
dig your-domain.com
```

### Q2: API 请求 502 Bad Gateway

**原因**：FastAPI 服务没有启动

**解决**：
```bash
# 检查 FastAPI 状态
sudo systemctl status designer-cep

# 查看日志
sudo journalctl -u designer-cep -f

# 重启服务
sudo systemctl restart designer-cep
```

### Q3: 静态文件 404

**原因**：文件路径不对

**解决**：
```bash
# 检查文件是否存在
ls -la /var/www/DesignerCEP/Server/static/shell/
ls -la /var/www/DesignerCEP/Server/static/core/1.0.6/

# 检查权限
sudo chown -R www-data:www-data /var/www/DesignerCEP
sudo chmod -R 755 /var/www/DesignerCEP
```

### Q4: Cloudflare 无限重定向

**原因**：Cloudflare SSL 模式设置错误

**解决**：
1. 进入 Cloudflare 控制台
2. SSL/TLS → Overview
3. 选择 **"Flexible"** 模式（因为 Caddy 配置的是 HTTP）

或者修改 Caddyfile 使用 HTTPS：

```caddy
# 方法 1: 自签名证书
your-domain.com {
    tls internal
    # ... 其他配置
}

# 方法 2: Cloudflare Origin Certificate
your-domain.com {
    tls /etc/caddy/certs/cloudflare-origin.pem /etc/caddy/certs/cloudflare-origin.key
    # ... 其他配置
}
```

---

## 🎯 10. Cloudflare 最佳实践

### 10.1 SSL/TLS 配置

```
Cloudflare 控制台 → SSL/TLS → Overview

选择模式：
- ❌ Off - 不使用 HTTPS
- ✅ Flexible - Cloudflare ←HTTPS→ 用户，Cloudflare ←HTTP→ 源站（推荐简单部署）
- ⚠️ Full - 双向 HTTPS，但不验证源站证书
- ✅ Full (Strict) - 双向 HTTPS，验证证书（推荐生产环境）
```

**推荐方案**：

#### Flexible 模式（最简单）

```caddy
# Caddyfile
{
    auto_https off
}

http://your-domain.com {
    # ... 配置
}
```

Cloudflare 设置：`Flexible`

#### Full (Strict) 模式（最安全）

1. 生成 Cloudflare Origin Certificate：
```
Cloudflare 控制台 → SSL/TLS → Origin Server → Create Certificate
```

2. 下载证书并上传到服务器：
```bash
sudo mkdir -p /etc/caddy/certs
sudo nano /etc/caddy/certs/cloudflare-origin.pem  # 粘贴证书
sudo nano /etc/caddy/certs/cloudflare-origin.key  # 粘贴私钥
sudo chmod 600 /etc/caddy/certs/*
```

3. 修改 Caddyfile：
```caddy
your-domain.com {
    tls /etc/caddy/certs/cloudflare-origin.pem /etc/caddy/certs/cloudflare-origin.key
    
    # ... 其他配置
}
```

4. Cloudflare 设置：`Full (Strict)`

### 10.2 性能优化

```
Cloudflare 控制台设置：

1. Speed → Optimization
   - ✅ Auto Minify: HTML, CSS, JS
   - ✅ Brotli 压缩

2. Caching → Configuration
   - ✅ Caching Level: Standard
   - ✅ Browser Cache TTL: Respect Existing Headers

3. Network
   - ✅ HTTP/2
   - ✅ HTTP/3 (QUIC)
```

---

## 📊 11. 监控和日志

### 查看 Caddy 日志

```bash
# 实时日志
sudo journalctl -u caddy -f

# 访问日志
sudo tail -f /var/log/caddy/designer-cep.log

# 错误日志
sudo journalctl -u caddy --since "1 hour ago" | grep -i error
```

### 查看 FastAPI 日志

```bash
# 实时日志
sudo journalctl -u designer-cep -f

# 最近的错误
sudo journalctl -u designer-cep --since "1 hour ago" | grep -i error
```

### 性能监控

```bash
# 检查服务器资源
htop

# 检查端口监听
sudo netstat -tlnp | grep -E '(8000|80|443)'

# 检查 Caddy 进程
ps aux | grep caddy
```

---

## 🔄 12. 更新部署

### 更新前端

```bash
# 方法 A: 手动
cd Designer
npm run build
scp -r dist/Shell/* user@server:/var/www/DesignerCEP/Server/static/shell/
scp -r dist/Designer/* user@server:/var/www/DesignerCEP/Server/static/core/1.0.7/

# 方法 B: 自动化
cd AdminTool
python auto_deploy_core.py --version 1.0.7 --deploy --update-db
```

### 更新后端

```bash
# 1. SSH 到服务器
ssh user@your-server

# 2. 拉取最新代码
cd /var/www/DesignerCEP/Server
git pull

# 3. 更新依赖
source venv/bin/activate
pip install -r requirements.txt

# 4. 重启服务
sudo systemctl restart designer-cep

# 5. 检查状态
sudo systemctl status designer-cep
```

### 更新 Caddy 配置

```bash
# 1. 修改配置
sudo nano /etc/caddy/Caddyfile

# 2. 验证配置
sudo caddy validate --config /etc/caddy/Caddyfile

# 3. 重新加载（不中断服务）
sudo systemctl reload caddy
```

---

## 🎉 完成！

访问地址：
- **Shell 登录页**：`https://your-domain.com/shell/`
- **Core 应用**：`https://your-domain.com/core/1.0.6/`
- **API 文档**：`https://your-domain.com/api/v1/docs`

---

## 📋 部署检查清单

- [ ] Caddy 已安装并启动
- [ ] Caddyfile 配置正确
- [ ] FastAPI 服务运行正常
- [ ] 前端文件已上传
- [ ] 环境变量配置正确
- [ ] CORS 支持 CEP 环境
- [ ] MySQL 数据库已更新
- [ ] HTTPS 证书正常
- [ ] 静态文件缓存正确
- [ ] API 请求正常
- [ ] CEP 扩展测试通过
- [ ] 浏览器访问正常

---

**Caddy 的优势总结**：
- ✅ 配置只有 Nginx 的 1/3 长度
- ✅ 自动 HTTPS，无需 Certbot
- ✅ 自动续期证书
- ✅ 内置 GZIP/Brotli 压缩
- ✅ 配置更直观易懂
- ✅ 错误提示更友好

**下一步**：运行 `python auto_deploy_core.py --version 1.0.6 --deploy --update-db` 一键部署！

