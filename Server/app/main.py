from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path
from app.core.config import settings
from app.api.v1 import auth, client, admin, analytics, jsx_demo, admin_config, feature, checkin, user_profile, stats
from app.db import init_db
from datetime import datetime

app = FastAPI(title=settings.PROJECT_NAME)

# Ensure archives directory exists
os.makedirs("archives", exist_ok=True)

# ========== CORS 配置 ==========
IS_DEV = os.getenv("ENV", "development") == "development"

if IS_DEV:
    # 开发环境：保持宽松
    print("⚠️  Running in Development Mode: CORS allows *")
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
    print(f"🔒 Running in Production Mode: CORS allowed origins: {allowed_origins}")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )
    
    # ✅ CEP 环境特殊处理 (Origin: null or cep://)
    @app.middleware("http")
    async def cep_cors_middleware(request: Request, call_next):
        origin = request.headers.get("origin")
        
        # CEP 的 Origin 是 null 或 cep://
        if origin in ["null", None] or (origin and origin.startswith("cep://")):
            response = await call_next(request)
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "*"
            return response
        
        return await call_next(request)

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["authentication"])
app.include_router(client.router, prefix=f"{settings.API_V1_STR}/client", tags=["client"])
app.include_router(admin.router, prefix=f"{settings.API_V1_STR}/admin", tags=["admin"])
app.include_router(analytics.router, prefix=f"{settings.API_V1_STR}/analytics", tags=["analytics"])
app.include_router(jsx_demo.router, prefix=f"{settings.API_V1_STR}/jsx_demo", tags=["jsx_demo"])

# 新增路由
app.include_router(admin_config.router, prefix=settings.API_V1_STR, tags=["admin-config"])
app.include_router(feature.router, prefix=settings.API_V1_STR, tags=["feature"])
app.include_router(checkin.router, prefix=settings.API_V1_STR, tags=["checkin"])
app.include_router(user_profile.router, prefix=settings.API_V1_STR, tags=["user-profile"])
app.include_router(stats.router, prefix=settings.API_V1_STR, tags=["stats"])

# Health Check
@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat(), "env": "development" if IS_DEV else "production"}

# ========== Static Files (Development Only) ==========
if IS_DEV:
    # Mount archives directory for download
    app.mount("/download", StaticFiles(directory="archives"), name="download")

    # Mount Shell directory (登录页面)
    shell_dir = Path(__file__).parent.parent / "Designer"
    if shell_dir.exists():
        app.mount("/shell", StaticFiles(directory=str(shell_dir), html=True), name="shell")
        print(f"✓ Shell 已挂载 (Dev): {shell_dir}")
    else:
        print(f"⚠️ Shell 目录不存在: {shell_dir}")
        print("  请先运行: cd Designer && npm run build:shell")

    # Mount DesignerCache directory to serve Core application files
    designer_cache = Path.home() / "AppData" / "Roaming" / "DesignerCache"
    if designer_cache.exists():
        app.mount("/core", StaticFiles(directory=str(designer_cache), html=True), name="core")
        print(f"✓ Core 已挂载 (Dev): {designer_cache}")
    else:
        # Create directory if it doesn't exist
        designer_cache.mkdir(parents=True, exist_ok=True)
        app.mount("/core", StaticFiles(directory=str(designer_cache), html=True), name="core")
else:
    print("ℹ️  Production Mode: Static files are NOT mounted by FastAPI (handled by Caddy/Nginx).")

@app.get("/")
def read_root():
    from fastapi.responses import RedirectResponse
    if IS_DEV:
        # 重定向到 Shell 登录页
        return RedirectResponse(url="/shell/index.html")
    return {"message": "DesignerCEP API is running"}

@app.on_event("startup")
def on_startup():
    # 应用启动时初始化数据库（创建表）
    init_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
