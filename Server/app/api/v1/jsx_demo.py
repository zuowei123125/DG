"""
服务器端计算 Demo - 简单数学计算
演示：前端获取图层名称 → 后端计算数学表达式 → 返回结果
"""

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
import re
import logging
from datetime import datetime
from typing import Optional
from app.core.api_keys import validate_api_key, get_key_info

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

router = APIRouter()

class CalculateRequest(BaseModel):
    """计算请求"""
    expression: str  # 数学表达式，如 "87-98"

class CalculateResult(BaseModel):
    """计算结果"""
    success: bool
    expression: str
    result: float = None
    message: str

@router.post("/calculate", response_model=CalculateResult)
async def calculate_expression(
    request: CalculateRequest,
    x_api_key: Optional[str] = Header(None)  # 可选的 API Key 验证
):
    """
    🔒 服务器端数学计算（核心算法）
    客户端只能拿到计算结果，看不到算法
    
    示例：前端发送 "87-98" → 后端计算 → 返回 -11
    """
    
    # ==================== 📝 日志：打印请求 ====================
    logger.info("="*60)
    logger.info("📥 收到计算请求")
    logger.info(f"   时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"   表达式: {request.expression}")
    logger.info(f"   API Key: {x_api_key if x_api_key else '未提供'}")
    logger.info("="*60)
    
    # ==================== 🔐 API Key 验证 ====================
    if not validate_api_key(x_api_key):
        logger.warning(f"❌ API Key 验证失败: {x_api_key}")
        raise HTTPException(status_code=403, detail="无效的 API Key")
    
    # 获取 Key 信息
    key_info = get_key_info(x_api_key)
    logger.info(f"✅ API Key 验证通过 | 名称: {key_info['name']} | 权限: {key_info['permissions']}")
    
    try:
        # 🔒 核心算法在这里（客户端看不到）
        # 可以是复杂的数学模型、AI 推理等
        
        expression = request.expression.strip()
        
        # ==================== 🛡️ 安全检查 ====================
        logger.info(f"🛡️ 安全检查: 验证表达式格式...")
        
        # 只允许数字和基本运算符
        if not re.match(r'^[\d\s\+\-\*\/\(\)\.]+$', expression):
            logger.warning(f"❌ 表达式包含非法字符: {expression}")
            return CalculateResult(
                success=False,
                expression=expression,
                message="只支持基本数学运算（+、-、*、/）"
            )
        
        logger.info("✅ 表达式格式验证通过")
        
        # ==================== 🔒 核心算法执行 ====================
        logger.info("🔒 开始执行核心算法...")
        
        # 这里可以放你的核心算法
        # 示例：简单计算
        result = eval(expression)
        
        logger.info(f"✅ 计算完成: {expression} = {result}")
        
        # ==================== 📤 日志：打印输出 ====================
        response = CalculateResult(
            success=True,
            expression=expression,
            result=float(result),
            message=f"计算成功: {expression} = {result}"
        )
        
        logger.info("="*60)
        logger.info("📤 返回计算结果")
        logger.info(f"   成功: {response.success}")
        logger.info(f"   表达式: {response.expression}")
        logger.info(f"   结果: {response.result}")
        logger.info(f"   消息: {response.message}")
        logger.info("="*60)
        
        return response
        
    except Exception as e:
        logger.error(f"❌ 计算失败: {str(e)}")
        logger.error("="*60)
        
        return CalculateResult(
            success=False,
            expression=request.expression,
            message=f"计算失败: {str(e)}"
        )

