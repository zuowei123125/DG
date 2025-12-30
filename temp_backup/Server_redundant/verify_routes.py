import sys
import os
from fastapi.routing import APIRoute

# 添加 Server 目录到 Python 路径
sys.path.append(os.path.join(os.getcwd(), 'Server'))

try:
    from app.main import app
    
    print("="*60)
    print("🔍 DesignerCEP 后端路由表检查")
    print("="*60)
    
    routes = []
    for route in app.routes:
        if isinstance(route, APIRoute):
            methods = ",".join(route.methods)
            routes.append(f"{methods:<20} {route.path}")
    
    # 排序以便查看
    routes.sort(key=lambda x: x.split()[1])
    
    for r in routes:
        print(r)
        
    print("="*60)
    print(f"✅ 总计: {len(routes)} 个路由")

except Exception as e:
    print(f"❌ 加载应用失败: {e}")
    import traceback
    traceback.print_exc()
