"""
服务器端 JSX 执行器
关键业务逻辑在服务器执行，前端只能通过 API 调用
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.core.security import get_current_user
from app.db import get_db_session
import json

router = APIRouter()

# JSX 脚本模板库（服务器端存储）
JSX_TEMPLATES = {
    "create_layer": """
        (function(layerName) {
            try {
                if (app.documents.length === 0) {
                    return JSON.stringify({ error: '没有打开的文档' });
                }
                var doc = app.activeDocument;
                var layer = doc.artLayers.add();
                layer.name = layerName;
                return JSON.stringify({ 
                    success: true, 
                    layerName: layerName 
                });
            } catch (e) {
                return JSON.stringify({ error: e.toString() });
            }
        })('{layerName}')
    """,
    
    "create_layer_with_style": """
        (function(layerName, opacity, color) {
            try {
                if (app.documents.length === 0) {
                    return JSON.stringify({ error: '没有打开的文档' });
                }
                var doc = app.activeDocument;
                var layer = doc.artLayers.add();
                layer.name = layerName;
                layer.opacity = opacity;
                
                // 这里是你的核心算法
                // 客户端无法看到具体实现
                
                return JSON.stringify({ 
                    success: true, 
                    layerName: layerName,
                    applied: true
                });
            } catch (e) {
                return JSON.stringify({ error: e.toString() });
            }
        })('{layerName}', {opacity}, '{color}')
    """,
    
    # 更多核心功能...
}

class JSXExecuteRequest(BaseModel):
    template_name: str  # 模板名称（不是完整脚本）
    params: Dict[str, Any]  # 参数
    device_id: str

class JSXExecuteResponse(BaseModel):
    success: bool
    jsx_code: str  # 返回要执行的 JSX 代码
    message: Optional[str] = None

@router.post("/execute", response_model=JSXExecuteResponse)
async def execute_jsx(
    request: JSXExecuteRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    服务器端生成 JSX 代码
    客户端只能通过 API 获取，无法直接看到核心逻辑
    """
    try:
        username = current_user.get("username")
        
        # 1. 验证用户和设备
        # ... (从数据库检查用户是否有权限、设备是否绑定)
        
        # 2. 检查模板是否存在
        if request.template_name not in JSX_TEMPLATES:
            raise HTTPException(status_code=404, detail="模板不存在")
        
        # 3. 验证用户权限（某些高级功能需要付费）
        # ... (从数据库检查用户等级)
        
        # 4. 获取模板并填充参数
        template = JSX_TEMPLATES[request.template_name]
        
        # 参数安全过滤（防止注入）
        safe_params = {
            key: str(value).replace("'", "\\'").replace('"', '\\"')
            for key, value in request.params.items()
        }
        
        # 填充参数
        jsx_code = template.format(**safe_params)
        
        # 5. 记录操作日志
        # ... (记录谁在什么时候执行了什么操作)
        
        return JSXExecuteResponse(
            success=True,
            jsx_code=jsx_code,
            message="代码已生成"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/templates")
async def list_templates(current_user: dict = Depends(get_current_user)):
    """
    列出可用的 JSX 模板（不返回具体代码）
    """
    return {
        "templates": [
            {
                "name": "create_layer",
                "description": "创建图层",
                "params": ["layerName"]
            },
            {
                "name": "create_layer_with_style",
                "description": "创建带样式的图层（高级）",
                "params": ["layerName", "opacity", "color"],
                "premium": True  # 需要付费
            }
        ]
    }

